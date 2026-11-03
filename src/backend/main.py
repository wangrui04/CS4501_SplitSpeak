
import os
import time

from fastapi import Body, FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from itsdangerous import TimestampSigner, BadSignature

from backend.repository import (
    list_groups,
    get_group,
    create_conversation,
    get_conversation,
    update_conversation,
    add_conversation_message,
    list_conversations,
    confirm_conversation_expense,
    get_group_balances,
    list_expenses,
    save_expense,
)
from backend.manual import ManualEntryError, build_manual_expense
from backend.group_management import router as group_management_router
from backend.config import (
    CHAT_RATE_LIMIT_PER_MINUTE,
    DEFAULT_GEMINI_MODEL,
    DEFAULT_GROQ_MODEL,
    DEFAULT_LLM_MODEL,
    DEFAULT_WEB_ORIGINS,
    MAX_MESSAGE_LENGTH,
    MAX_PROMPTS_PER_CONVERSATION,
)
from backend.security import (
    SECURITY_HEADERS,
    RateLimiter,
    install_secret_redaction,
    sanitize_message,
)
from backend.pipeline import parse_turn
from backend.settlement import compute_settlement, member_balances
from backend.schemas import (
    ChatRequest,
    ChatResponse,
    ConfirmRequest,
    ConfirmResponse,
)


class Login(BaseModel):
    name: str


def create_app(
    db,
    session_secret,
    llm=None,
    clock=time.monotonic,
    web_origins=DEFAULT_WEB_ORIGINS,
):
    app = FastAPI()
    app.state.llm = llm
    app.state.db = db

    chat_limiter = RateLimiter(
        limit=CHAT_RATE_LIMIT_PER_MINUTE,
        window_seconds=60,
        clock=clock or time.monotonic,
    )

    install_secret_redaction()

    def known_names():
        names = []

        for group in list_groups(db):
            details = get_group(db, group["id"])

            for name in details["members"]:
                if name not in names:
                    names.append(name)

        return names

    signer = TimestampSigner(str(session_secret))

    def session_cookie_is_valid(request: Request):
        cookie = request.cookies.get("session")

        if not cookie:
            return False

        try:
            signer.unsign(
                cookie,
                max_age=14 * 24 * 60 * 60,
            )
            return True

        except (BadSignature, ValueError, UnicodeError):
            return False

    @app.middleware("http")
    async def protect(request: Request, call_next):
        path = request.url.path

        public_routes = {
            "/health",
            "/api/session/names",
            "/api/session",
        }

        requires_session = (
            path.startswith("/api/")
            and path not in public_routes
        )

        if path == "/api/session":
            requires_session = False

        if requires_session:
            if not session_cookie_is_valid(request):
                return JSONResponse(
                    status_code=401,
                    content={
                        "detail": "Invalid or missing session"
                    },
                )

            name = request.session.get("name")

            if name not in known_names():
                return JSONResponse(
                    status_code=401,
                    content={
                        "detail": "Sign in required"
                    },
                )

        return await call_next(request)

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)

        for name, value in SECURITY_HEADERS.items():
            response.headers.setdefault(name, value)

        return response

    app.add_middleware(
        SessionMiddleware,
        secret_key=session_secret,
        same_site="lax",
        https_only=False,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(web_origins),
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["Content-Type"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/api/session/names")
    def names():
        return known_names()

    @app.post("/api/session")
    def login(payload: Login, request: Request):
        if payload.name not in known_names():
            raise HTTPException(
                status_code=400,
                detail="Unknown name",
            )

        request.session.clear()
        request.session["name"] = payload.name

        return {"name": payload.name}

    @app.get("/api/session")
    def session(request: Request):
        name = request.session.get("name")

        if name not in known_names():
            raise HTTPException(
                status_code=401,
                detail="Not signed in",
            )

        return {"name": name}

    @app.delete("/api/session")
    def logout(request: Request):
        request.session.clear()
        return {"ok": True}

    @app.get("/api/groups")
    def groups(request: Request):
        current_user = request.session.get("name")

        results = []

        for group_record in list_groups(db):
            details = get_group(db, group_record["id"])

            if current_user in details["members"]:
                results.append(details)

        return results

    # Group creation and membership routes.
    app.include_router(group_management_router)

    def member_group_or_error(group_id, request):
        group_data = get_group(db, group_id)

        if group_data is None:
            raise HTTPException(
                status_code=404,
                detail="Group not found",
            )

        if request.session.get("name") not in group_data["members"]:
            raise HTTPException(
                status_code=403,
                detail="Not a member of this group",
            )

        return group_data

    @app.get("/api/groups/{group_id}")
    def group(group_id: int, request: Request):
        result = member_group_or_error(group_id, request)

        settlement = compute_settlement(
            list_expenses(db, group_id),
            result["members"],
        )

        relative = member_balances(
            settlement,
            request.session.get("name"),
            result["members"],
        )

        return {
            **result,
            "nets": settlement["nets"],
            "transfers": settlement["transfers"],
            "balances": relative["balances"],
            "summary": relative["summary"],
        }

    @app.get("/api/groups/{group_id}/expenses")
    def group_expenses(group_id: int, request: Request):
        member_group_or_error(group_id, request)

        return list(reversed(list_expenses(db, group_id)))

    @app.post("/api/groups/{group_id}/expenses/manual")
    def manual_expense(
        group_id: int,
        request: Request,
        payload: dict = Body(...),
    ):
        group_data = member_group_or_error(group_id, request)

        try:
            expense = build_manual_expense(
                payload,
                group_data["members"],
            )

            saved = save_expense(
                db,
                {
                    **expense,
                    "groupId": group_id,
                    "createdBy": request.session.get("name"),
                },
            )
        except ManualEntryError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            )

        return {"ok": True, "expenseId": saved["id"]}

    def get_llm():
        active_llm = getattr(app.state, "llm", None)

        if active_llm is not None:
            return active_llm

        api_key = os.environ.get("ANTHROPIC_API_KEY")

        if api_key:
            from backend.llm import ClaudeLlmClient

            return ClaudeLlmClient(
                api_key=api_key,
                model=(
                    os.environ.get("LLM_MODEL")
                    or DEFAULT_LLM_MODEL
                ),
            )

        raise HTTPException(
            status_code=500,
            detail="LLM client not configured",
        )

    @app.post("/api/chat")
    def chat(payload: ChatRequest, request: Request):
        current_user = request.session.get("name")

        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Sign in required",
            )

        if not chat_limiter.allow(current_user):
            raise HTTPException(
                status_code=429,
                detail="Too many messages. Try again in a minute.",
            )

        message_text = sanitize_message(payload.message)

        if not message_text:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty",
            )

        if len(message_text) > MAX_MESSAGE_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Message is too long "
                    f"(maximum {MAX_MESSAGE_LENGTH} characters)"
                ),
            )

        group_id = payload.group_id
        conversation_id = payload.conversation_id

        if conversation_id is not None:
            conv = get_conversation(db, conversation_id)

            if conv is None:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found",
                )

            if conv["status"] in ("confirmed", "unsuccessful"):
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "This conversation is closed. "
                        "Start a new one."
                    ),
                )

            if (
                group_id is not None
                and conv["groupId"] != group_id
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Conversation group mismatch",
                )

            group_id = conv["groupId"]

        else:
            if group_id is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "groupId is required for a new conversation"
                    ),
                )

            conv = None

        group_data = get_group(db, group_id)

        if group_data is None:
            raise HTTPException(
                status_code=404,
                detail="Group not found",
            )

        if current_user not in group_data["members"]:
            raise HTTPException(
                status_code=403,
                detail="Not a member of this group",
            )

        if conv is None:
            prompt_count = 1

            conv_record = create_conversation(
                db,
                {
                    "groupId": group_id,
                    "userName": current_user,
                    "promptCount": prompt_count,
                    "status": "pending",
                },
            )

            conversation_id = conv_record["id"]
            existing_messages = []

        else:
            prompt_count = conv["promptCount"] + 1

            update_conversation(
                db,
                conversation_id,
                {"promptCount": prompt_count},
            )

            existing_messages = conv["messages"]

        add_conversation_message(
            db,
            conversation_id,
            "user",
            message_text,
        )

        if prompt_count > MAX_PROMPTS_PER_CONVERSATION:
            reason = (
                f"Prompt limit exceeded "
                f"(maximum {MAX_PROMPTS_PER_CONVERSATION} prompts). "
                "Please enter this expense manually."
            )

            add_conversation_message(
                db,
                conversation_id,
                "assistant",
                reason,
            )

            update_conversation(
                db,
                conversation_id,
                {"status": "unsuccessful"},
            )

            return {
                "type": "unresolved",
                "reason": reason,
                "conversationId": conversation_id,
                "promptCount": prompt_count,
                "status": "unsuccessful",
                "fallback": "manual",
            }

        full_messages = existing_messages + [
            {"role": "user", "content": message_text}
        ]

        active_llm = get_llm()

        result = parse_turn(
            llm=active_llm,
            conversation=full_messages,
            roster=group_data["members"],
            current_user=current_user,
        )

        res_type = result.get("type")

        if res_type == "question":
            question_text = result["question"]

            add_conversation_message(
                db,
                conversation_id,
                "assistant",
                question_text,
            )

            update_conversation(
                db,
                conversation_id,
                {"status": "pending"},
            )

            return {
                "type": "question",
                "question": question_text,
                "conversationId": conversation_id,
                "promptCount": prompt_count,
                "status": "pending",
            }

        elif res_type == "preview":
            preview = result["preview"]

            add_conversation_message(
                db,
                conversation_id,
                "assistant",
                "Validated preview generated.",
            )

            update_conversation(
                db,
                conversation_id,
                {
                    "status": "preview",
                    "finalPreview": preview,
                },
            )

            return {
                "type": "preview",
                "preview": preview,
                "conversationId": conversation_id,
                "promptCount": prompt_count,
                "status": "preview",
            }

        elif res_type == "unresolved":
            reason = result.get(
                "reason",
                "Unable to parse expense.",
            )

            add_conversation_message(
                db,
                conversation_id,
                "assistant",
                reason,
            )

            update_conversation(
                db,
                conversation_id,
                {"status": "unresolved"},
            )

            return {
                "type": "unresolved",
                "reason": reason,
                "conversationId": conversation_id,
                "promptCount": prompt_count,
                "status": "unresolved",
                "fallback": "manual",
            }

        else:
            err_msg = result.get(
                "message",
                "Unexpected error processing expense.",
            )

            add_conversation_message(
                db,
                conversation_id,
                "assistant",
                err_msg,
            )

            return {
                "type": "error",
                "message": err_msg,
                "conversationId": conversation_id,
                "promptCount": prompt_count,
                "status": "error",
            }

    @app.post("/api/groups/{group_id}/chat")
    def group_chat(
        group_id: int,
        payload: ChatRequest,
        request: Request,
    ):
        if payload.group_id is None:
            payload.group_id = group_id

        elif payload.group_id != group_id:
            raise HTTPException(
                status_code=400,
                detail="Path and body group_id mismatch",
            )

        return chat(payload, request)

    @app.post("/api/conversations")
    def create_conv(payload: dict, request: Request):
        current_user = request.session.get("name")
        group_id = (
            payload.get("groupId")
            or payload.get("group_id")
        )

        if group_id is None:
            raise HTTPException(
                status_code=400,
                detail="groupId is required",
            )

        group_data = get_group(db, group_id)

        if group_data is None:
            raise HTTPException(
                status_code=404,
                detail="Group not found",
            )

        if current_user not in group_data["members"]:
            raise HTTPException(
                status_code=403,
                detail="Not a member of this group",
            )

        record = create_conversation(
            db,
            {
                "groupId": group_id,
                "userName": current_user,
                "promptCount": 0,
                "status": "pending",
            },
        )

        return get_conversation(db, record["id"])

    @app.get("/api/conversations/{conversation_id}")
    @app.get("/api/chat/{conversation_id}")
    def get_conv(
        conversation_id: int,
        request: Request,
    ):
        conv = get_conversation(db, conversation_id)

        if conv is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        current_user = request.session.get("name")
        group_data = get_group(db, conv["groupId"])

        if (
            group_data is None
            or current_user not in group_data["members"]
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "Not authorized to access this conversation"
                ),
            )

        return conv

    @app.get("/api/groups/{group_id}/conversations")
    def group_conversations(
        group_id: int,
        request: Request,
    ):
        group_data = get_group(db, group_id)

        if group_data is None:
            raise HTTPException(
                status_code=404,
                detail="Group not found",
            )

        current_user = request.session.get("name")

        if current_user not in group_data["members"]:
            raise HTTPException(
                status_code=403,
                detail="Not a member of this group",
            )

        return list_conversations(db, group_id)

    @app.post("/api/conversations/{conversation_id}/confirm")
    @app.post("/api/chat/{conversation_id}/confirm")
    @app.post("/api/drafts/{conversation_id}/confirm")
    def confirm_conversation(
        conversation_id: int,
        request: Request,
    ):
        current_user = request.session.get("name")

        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Sign in required",
            )

        conv = get_conversation(db, conversation_id)

        if conv is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        group_data = get_group(db, conv["groupId"])

        if (
            group_data is None
            or current_user not in group_data["members"]
        ):
            raise HTTPException(
                status_code=403,
                detail="Not authorized to confirm this expense",
            )

        try:
            result = confirm_conversation_expense(
                db=db,
                conversation_id=conversation_id,
                confirmed_by=current_user,
            )

            return {
                "ok": True,
                **result,
            }

        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            )

    @app.post("/api/expenses/confirm")
    def confirm_expense_body(
        payload: ConfirmRequest,
        request: Request,
    ):
        if payload.conversation_id is None:
            raise HTTPException(
                status_code=400,
                detail="conversationId is required",
            )

        return confirm_conversation(
            payload.conversation_id,
            request,
        )

    @app.get("/api/groups/{group_id}/balances")
    def group_balances(
        group_id: int,
        request: Request,
    ):
        group_data = get_group(db, group_id)

        if group_data is None:
            raise HTTPException(
                status_code=404,
                detail="Group not found",
            )

        current_user = request.session.get("name")

        if current_user not in group_data["members"]:
            raise HTTPException(
                status_code=403,
                detail="Not a member of this group",
            )

        return get_group_balances(db, group_id)

    return app


def select_llm(env):
    """Select the configured LLM client."""
    provider = (
        env.get("LLM_PROVIDER") or ""
    ).strip().lower()

    if provider == "groq":
        from backend.llm import GroqLlmClient

        return GroqLlmClient(
            api_key=env.get("GROQ_API_KEY"),
            model=env.get("GROQ_MODEL") or DEFAULT_GROQ_MODEL,
        )

    if provider == "gemini":
        from backend.llm import GeminiLlmClient

        return GeminiLlmClient(
            api_key=env.get("GEMINI_API_KEY"),
            model=env.get("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL,
        )

    if provider == "fake":
        from backend.llm import FixtureLlmClient

        return FixtureLlmClient()

    if provider == "claude":
        return None

    if (
        provider == "demo"
        or not env.get("ANTHROPIC_API_KEY")
    ):
        from backend.llm import DemoLlmClient

        return DemoLlmClient()

    return None


def get_app():
    from backend.database import (
        create_database,
        seed_database,
    )

    db_path = os.environ.get("DB_PATH", ":memory:")
    db = create_database(db_path)
    seed_database(db)

    session_secret = os.environ.get(
        "SESSION_SECRET",
        "development-session-secret-key-at-least-32-chars",
    )

    llm = select_llm(os.environ)

    web_origins = [
        origin.strip()
        for origin in os.environ.get(
            "WEB_ORIGINS", ""
        ).split(",")
        if origin.strip()
    ] or DEFAULT_WEB_ORIGINS

    return create_app(
        db,
        session_secret,
        llm=llm,
        web_origins=web_origins,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        get_app(),
        host="127.0.0.1",
        port=8000,
    )
