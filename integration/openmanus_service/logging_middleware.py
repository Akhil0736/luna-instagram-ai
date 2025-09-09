import logging
import time
import uuid
from typing import Awaitable, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger("luna.middleware")
SLOW_THRESHOLD_SECONDS = 2.0

class RequestIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        req_id = str(uuid.uuid4())[:8]
        request.state.request_id = req_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response

class HttpLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start = time.perf_counter()
        method = request.method
        url = str(request.url)
        req_id = getattr(request.state, "request_id", "-")

        logger.info("🚀 Luna REQUEST START | id=%s | %s %s", req_id, method, url)

        try:
            response = await call_next(request)
        except Exception as e:
            duration = time.perf_counter() - start
            logger.exception("❌ Luna REQUEST ERROR | id=%s | %s %s | duration=%.3fs | error=%s",
                             req_id, method, url, duration, repr(e))
            raise

        duration = time.perf_counter() - start
        if duration > SLOW_THRESHOLD_SECONDS:
            logger.warning("🐌 Luna SLOW REQUEST | id=%s | %s %s | status=%s | duration=%.3fs",
                           req_id, method, url, response.status_code, duration)
        else:
            logger.info("✅ Luna REQUEST DONE | id=%s | %s %s | status=%s | duration=%.3fs",
                        req_id, method, url, response.status_code, duration)

        return response
