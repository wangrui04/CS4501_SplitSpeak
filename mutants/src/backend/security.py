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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_sanitize_message__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_sanitize_message__mutmut)
def sanitize_message(text: str) -> str:
    return _CONTROL_CHARS.sub("", text).strip()


def x_sanitize_message__mutmut_orig(text: str) -> str:
    return _CONTROL_CHARS.sub("", text).strip()


def x_sanitize_message__mutmut_1(text: str) -> str:
    return _CONTROL_CHARS.sub(None, text).strip()


def x_sanitize_message__mutmut_2(text: str) -> str:
    return _CONTROL_CHARS.sub("", None).strip()


def x_sanitize_message__mutmut_3(text: str) -> str:
    return _CONTROL_CHARS.sub(text).strip()


def x_sanitize_message__mutmut_4(text: str) -> str:
    return _CONTROL_CHARS.sub("", ).strip()


def x_sanitize_message__mutmut_5(text: str) -> str:
    return _CONTROL_CHARS.sub("XXXX", text).strip()

mutants_x_sanitize_message__mutmut['_mutmut_orig'] = x_sanitize_message__mutmut_orig # type: ignore # mutmut generated
mutants_x_sanitize_message__mutmut['x_sanitize_message__mutmut_1'] = x_sanitize_message__mutmut_1 # type: ignore # mutmut generated
mutants_x_sanitize_message__mutmut['x_sanitize_message__mutmut_2'] = x_sanitize_message__mutmut_2 # type: ignore # mutmut generated
mutants_x_sanitize_message__mutmut['x_sanitize_message__mutmut_3'] = x_sanitize_message__mutmut_3 # type: ignore # mutmut generated
mutants_x_sanitize_message__mutmut['x_sanitize_message__mutmut_4'] = x_sanitize_message__mutmut_4 # type: ignore # mutmut generated
mutants_x_sanitize_message__mutmut['x_sanitize_message__mutmut_5'] = x_sanitize_message__mutmut_5 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁRateLimiterǁallow__mutmut: MutantDict = {}  # type: ignore


class RateLimiter:
    """Sliding-window limit of `limit` requests per key per window."""

    @_mutmut_mutated(mutants_xǁRateLimiterǁ__init____mutmut)
    def __init__(self, limit, window_seconds=60, clock=time.monotonic):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self.hits = defaultdict(deque)

    def xǁRateLimiterǁ__init____mutmut_orig(self, limit, window_seconds=60, clock=time.monotonic):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self.hits = defaultdict(deque)

    def xǁRateLimiterǁ__init____mutmut_1(self, limit, window_seconds=61, clock=time.monotonic):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self.hits = defaultdict(deque)

    def xǁRateLimiterǁ__init____mutmut_2(self, limit, window_seconds=60, clock=time.monotonic):
        self.limit = None
        self.window_seconds = window_seconds
        self.clock = clock
        self.hits = defaultdict(deque)

    def xǁRateLimiterǁ__init____mutmut_3(self, limit, window_seconds=60, clock=time.monotonic):
        self.limit = limit
        self.window_seconds = None
        self.clock = clock
        self.hits = defaultdict(deque)

    def xǁRateLimiterǁ__init____mutmut_4(self, limit, window_seconds=60, clock=time.monotonic):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = None
        self.hits = defaultdict(deque)

    def xǁRateLimiterǁ__init____mutmut_5(self, limit, window_seconds=60, clock=time.monotonic):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self.hits = None

    def xǁRateLimiterǁ__init____mutmut_6(self, limit, window_seconds=60, clock=time.monotonic):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock
        self.hits = defaultdict(None)

    @_mutmut_mutated(mutants_xǁRateLimiterǁallow__mutmut)
    def allow(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_orig(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_1(self, key) -> bool:
        now = None
        hits = self.hits[key]

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_2(self, key) -> bool:
        now = self.clock()
        hits = None

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_3(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits or now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_4(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now + hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_5(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[1] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_6(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_7(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) > self.limit:
            return False

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_8(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return True

        hits.append(now)
        return True

    def xǁRateLimiterǁallow__mutmut_9(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(None)
        return True

    def xǁRateLimiterǁallow__mutmut_10(self, key) -> bool:
        now = self.clock()
        hits = self.hits[key]

        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return False

mutants_xǁRateLimiterǁ__init____mutmut['_mutmut_orig'] = RateLimiter.xǁRateLimiterǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁRateLimiterǁ__init____mutmut['xǁRateLimiterǁ__init____mutmut_1'] = RateLimiter.xǁRateLimiterǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁ__init____mutmut['xǁRateLimiterǁ__init____mutmut_2'] = RateLimiter.xǁRateLimiterǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁ__init____mutmut['xǁRateLimiterǁ__init____mutmut_3'] = RateLimiter.xǁRateLimiterǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁ__init____mutmut['xǁRateLimiterǁ__init____mutmut_4'] = RateLimiter.xǁRateLimiterǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁ__init____mutmut['xǁRateLimiterǁ__init____mutmut_5'] = RateLimiter.xǁRateLimiterǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁ__init____mutmut['xǁRateLimiterǁ__init____mutmut_6'] = RateLimiter.xǁRateLimiterǁ__init____mutmut_6 # type: ignore # mutmut generated

mutants_xǁRateLimiterǁallow__mutmut['_mutmut_orig'] = RateLimiter.xǁRateLimiterǁallow__mutmut_orig # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_1'] = RateLimiter.xǁRateLimiterǁallow__mutmut_1 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_2'] = RateLimiter.xǁRateLimiterǁallow__mutmut_2 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_3'] = RateLimiter.xǁRateLimiterǁallow__mutmut_3 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_4'] = RateLimiter.xǁRateLimiterǁallow__mutmut_4 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_5'] = RateLimiter.xǁRateLimiterǁallow__mutmut_5 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_6'] = RateLimiter.xǁRateLimiterǁallow__mutmut_6 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_7'] = RateLimiter.xǁRateLimiterǁallow__mutmut_7 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_8'] = RateLimiter.xǁRateLimiterǁallow__mutmut_8 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_9'] = RateLimiter.xǁRateLimiterǁallow__mutmut_9 # type: ignore # mutmut generated
mutants_xǁRateLimiterǁallow__mutmut['xǁRateLimiterǁallow__mutmut_10'] = RateLimiter.xǁRateLimiterǁallow__mutmut_10 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut: MutantDict = {}  # type: ignore


class SecretRedactionFilter(logging.Filter):
    """Replace secret values from the environment in log records.

    Records without a secret are left untouched: rewriting msg/args on
    every record breaks formatters that unpack args, such as uvicorn's
    access log.
    """

    @_mutmut_mutated(mutants_xǁSecretRedactionFilterǁfilter__mutmut)
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

    def xǁSecretRedactionFilterǁfilter__mutmut_orig(self, record):
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

    def xǁSecretRedactionFilterǁfilter__mutmut_1(self, record):
        secrets = None
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

    def xǁSecretRedactionFilterǁfilter__mutmut_2(self, record):
        secrets = [
            value for name in SECRET_ENV_VARS
            if (value := os.environ.get(None))
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

    def xǁSecretRedactionFilterǁfilter__mutmut_3(self, record):
        secrets = [
            value for name in SECRET_ENV_VARS
            if (value := os.environ.get(name))
        ]
        if secrets:
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

    def xǁSecretRedactionFilterǁfilter__mutmut_4(self, record):
        secrets = [
            value for name in SECRET_ENV_VARS
            if (value := os.environ.get(name))
        ]
        if not secrets:
            return False

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

    def xǁSecretRedactionFilterǁfilter__mutmut_5(self, record):
        secrets = [
            value for name in SECRET_ENV_VARS
            if (value := os.environ.get(name))
        ]
        if not secrets:
            return True

        try:
            message = None
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

    def xǁSecretRedactionFilterǁfilter__mutmut_6(self, record):
        secrets = [
            value for name in SECRET_ENV_VARS
            if (value := os.environ.get(name))
        ]
        if not secrets:
            return True

        try:
            message = record.getMessage()
        except Exception:
            return False
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

    def xǁSecretRedactionFilterǁfilter__mutmut_7(self, record):
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
        if any(secret in message for secret in secrets):
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

    def xǁSecretRedactionFilterǁfilter__mutmut_8(self, record):
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
        if not any(None):
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

    def xǁSecretRedactionFilterǁfilter__mutmut_9(self, record):
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
        if not any(secret not in message for secret in secrets):
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

    def xǁSecretRedactionFilterǁfilter__mutmut_10(self, record):
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
            return False

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

    def xǁSecretRedactionFilterǁfilter__mutmut_11(self, record):
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
            if isinstance(value, str):
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

    def xǁSecretRedactionFilterǁfilter__mutmut_12(self, record):
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
                value = None
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

    def xǁSecretRedactionFilterǁfilter__mutmut_13(self, record):
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
                value = value.replace(None, "[REDACTED]")
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

    def xǁSecretRedactionFilterǁfilter__mutmut_14(self, record):
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
                value = value.replace(secret, None)
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

    def xǁSecretRedactionFilterǁfilter__mutmut_15(self, record):
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
                value = value.replace("[REDACTED]")
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

    def xǁSecretRedactionFilterǁfilter__mutmut_16(self, record):
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
                value = value.replace(secret, )
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

    def xǁSecretRedactionFilterǁfilter__mutmut_17(self, record):
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
                value = value.replace(secret, "XX[REDACTED]XX")
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

    def xǁSecretRedactionFilterǁfilter__mutmut_18(self, record):
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
                value = value.replace(secret, "[redacted]")
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

    def xǁSecretRedactionFilterǁfilter__mutmut_19(self, record):
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
        record.msg = None
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

    def xǁSecretRedactionFilterǁfilter__mutmut_20(self, record):
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
        record.msg = redact(None)
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

    def xǁSecretRedactionFilterǁfilter__mutmut_21(self, record):
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
            record.args = None
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

    def xǁSecretRedactionFilterǁfilter__mutmut_22(self, record):
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
            record.args = tuple(None)
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

    def xǁSecretRedactionFilterǁfilter__mutmut_23(self, record):
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
            record.args = tuple(redact(None) for arg in record.args)
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

    def xǁSecretRedactionFilterǁfilter__mutmut_24(self, record):
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
            record.args = None

        # A secret inside a non-string arg: fall back to the full text.
        if any(secret in record.getMessage() for secret in secrets):
            message = record.getMessage()
            for secret in secrets:
                message = message.replace(secret, "[REDACTED]")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_25(self, record):
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
            record.args = {key: redact(None) for key, arg in record.args.items()}

        # A secret inside a non-string arg: fall back to the full text.
        if any(secret in record.getMessage() for secret in secrets):
            message = record.getMessage()
            for secret in secrets:
                message = message.replace(secret, "[REDACTED]")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_26(self, record):
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
        if any(None):
            message = record.getMessage()
            for secret in secrets:
                message = message.replace(secret, "[REDACTED]")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_27(self, record):
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
        if any(secret not in record.getMessage() for secret in secrets):
            message = record.getMessage()
            for secret in secrets:
                message = message.replace(secret, "[REDACTED]")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_28(self, record):
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
            message = None
            for secret in secrets:
                message = message.replace(secret, "[REDACTED]")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_29(self, record):
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
                message = None
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_30(self, record):
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
                message = message.replace(None, "[REDACTED]")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_31(self, record):
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
                message = message.replace(secret, None)
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_32(self, record):
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
                message = message.replace("[REDACTED]")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_33(self, record):
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
                message = message.replace(secret, )
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_34(self, record):
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
                message = message.replace(secret, "XX[REDACTED]XX")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_35(self, record):
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
                message = message.replace(secret, "[redacted]")
            record.msg = message
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_36(self, record):
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
            record.msg = None
            record.args = ()
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_37(self, record):
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
            record.args = None
        return True

    def xǁSecretRedactionFilterǁfilter__mutmut_38(self, record):
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
        return False

mutants_xǁSecretRedactionFilterǁfilter__mutmut['_mutmut_orig'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_1'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_1 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_2'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_2 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_3'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_3 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_4'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_4 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_5'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_5 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_6'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_6 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_7'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_7 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_8'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_8 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_9'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_9 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_10'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_10 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_11'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_11 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_12'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_12 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_13'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_13 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_14'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_14 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_15'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_15 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_16'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_16 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_17'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_17 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_18'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_18 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_19'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_19 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_20'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_20 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_21'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_21 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_22'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_22 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_23'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_23 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_24'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_24 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_25'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_25 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_26'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_26 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_27'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_27 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_28'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_28 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_29'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_29 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_30'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_30 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_31'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_31 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_32'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_32 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_33'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_33 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_34'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_34 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_35'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_35 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_36'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_36 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_37'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_37 # type: ignore # mutmut generated
mutants_xǁSecretRedactionFilterǁfilter__mutmut['xǁSecretRedactionFilterǁfilter__mutmut_38'] = SecretRedactionFilter.xǁSecretRedactionFilterǁfilter__mutmut_38 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_install_secret_redaction__mutmut)
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


def x_install_secret_redaction__mutmut_orig(*loggers):
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


def x_install_secret_redaction__mutmut_1(*loggers):
    targets = None
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_2(*loggers):
    targets = loggers and (
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


def x_install_secret_redaction__mutmut_3(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger(None),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_4(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("XXuvicornXX"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_5(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("UVICORN"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_6(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger(None),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_7(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("XXuvicorn.errorXX"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_8(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("UVICORN.ERROR"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_9(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger(None),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_10(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("XXuvicorn.accessXX"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_11(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("UVICORN.ACCESS"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_12(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger(None),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_13(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("XXanthropicXX"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_14(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("ANTHROPIC"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_15(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger(None),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_16(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("XXhttpxXX"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_17(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("HTTPX"),
    )
    for logger in targets:
        if not any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_18(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if any(isinstance(f, SecretRedactionFilter) for f in logger.filters):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_19(*loggers):
    targets = loggers or (
        logging.getLogger(),
        logging.getLogger("uvicorn"),
        logging.getLogger("uvicorn.error"),
        logging.getLogger("uvicorn.access"),
        logging.getLogger("anthropic"),
        logging.getLogger("httpx"),
    )
    for logger in targets:
        if not any(None):
            logger.addFilter(SecretRedactionFilter())


def x_install_secret_redaction__mutmut_20(*loggers):
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
            logger.addFilter(None)

mutants_x_install_secret_redaction__mutmut['_mutmut_orig'] = x_install_secret_redaction__mutmut_orig # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_1'] = x_install_secret_redaction__mutmut_1 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_2'] = x_install_secret_redaction__mutmut_2 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_3'] = x_install_secret_redaction__mutmut_3 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_4'] = x_install_secret_redaction__mutmut_4 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_5'] = x_install_secret_redaction__mutmut_5 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_6'] = x_install_secret_redaction__mutmut_6 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_7'] = x_install_secret_redaction__mutmut_7 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_8'] = x_install_secret_redaction__mutmut_8 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_9'] = x_install_secret_redaction__mutmut_9 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_10'] = x_install_secret_redaction__mutmut_10 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_11'] = x_install_secret_redaction__mutmut_11 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_12'] = x_install_secret_redaction__mutmut_12 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_13'] = x_install_secret_redaction__mutmut_13 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_14'] = x_install_secret_redaction__mutmut_14 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_15'] = x_install_secret_redaction__mutmut_15 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_16'] = x_install_secret_redaction__mutmut_16 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_17'] = x_install_secret_redaction__mutmut_17 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_18'] = x_install_secret_redaction__mutmut_18 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_19'] = x_install_secret_redaction__mutmut_19 # type: ignore # mutmut generated
mutants_x_install_secret_redaction__mutmut['x_install_secret_redaction__mutmut_20'] = x_install_secret_redaction__mutmut_20 # type: ignore # mutmut generated
