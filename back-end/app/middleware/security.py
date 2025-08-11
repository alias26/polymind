from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
import time
import uuid

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    보안 헤더 추가 미들웨어
    """
    async def dispatch(self, request: Request, call_next):
        # 요청 ID 생성 (로깅용)
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # 보안 헤더 추가
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # 개발환경에서만 처리 시간 헤더 추가
        if settings.debug:
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
        
        return response

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    요청 로깅 미들웨어 (보안 고려)
    """
    async def dispatch(self, request: Request, call_next):
        if not settings.debug:
            # 프로덕션에서는 로깅 최소화
            return await call_next(request)
        
        # 개발환경에서만 상세 로깅
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # 민감한 경로는 로깅하지 않음
        sensitive_paths = ["/auth/login", "/auth/register", "/api-keys"]
        if any(path in str(request.url) for path in sensitive_paths):
            return response
        
        print(f"[{request.state.request_id if hasattr(request.state, 'request_id') else 'REQ'}] "
              f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
        
        return response