"""Rate limiting, input sanitizing, response headers, and log redaction."""

from __future__ import annotations

import logging
import os
import re
import time
from collections import defaultdict, deque

# Control characters except tab and newline (and carriage return).
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
}

SECRET_ENV_VARS = (
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "GROQ_API_KEY",
    "SESSION_SECRET",
)


def sanitize_message(text: str) -> str:
    return _CONTROL_CHARS.sub("", text).strip()


class RateLimiter:
    """Sliding-window limit of `limit` requests per key per window."""

    def __init__(self, limit, window_seconds=60, clock=time.monotonic):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self.hits = defaultdict(deque)

    def allow(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True


class SecretRedactionFilter(logging.Filter):
    """Replace secret values from the environment in log records.

    Records without a secret are left untouched: rewriting msg/args on
    every record breaks formatters that unpack args, such as uvicorn's
    access log.
    """

    def filter(self, record):
        secrets = [
            value for name in SECRET_ENV_VARS
            if (value := os.environ.get(name))
        ]
        if not secrets:
            return True

        try:
            message = record.getMessage()
        except Exception:
            return True
        if not any(secret in message for secret in secrets):
            return True

        def redact(value):
            if not isinstance(value, str):
                return value
            for secret in secrets:
                value = value.replace(secret, "[REDACTED]")
            return value

        # Redact in place so the args keep their shape for formatters.
        record.msg = redact(record.msg)
        if isinstance(record.args, tuple):
            record.args = tuple(redact(arg) for arg in record.args)
        elif isinstance(record.args, dict):
            record.args = {key: redact(arg) for key, arg in record.args.items()}

        # A secret inside a non-string arg: fall back to the full text.
        if any(secret in record.getMessage() for secret in secrets):
            message = record.getMessage()
            for secret in secrets:
                message = message.replace(secret, "[REDACTED]")
            record.msg = message
            record.args = ()
        return True


def install_secret_redaction(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())
