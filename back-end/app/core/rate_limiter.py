"""
Rate Limiting 모듈
API 호출 제한을 통한 보안 강화 및 서버 리소스 보호
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import logging

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# 로거 설정
logger = logging.getLogger(__name__)

def get_client_ip(request: Request) -> str:
    """
    클라이언트 IP 주소 추출
    프록시나 로드밸런서를 고려한 실제 IP 추출
    """
    # X-Forwarded-For 헤더 확인 (프록시/로드밸런서용)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # 첫 번째 IP가 실제 클라이언트 IP
        return forwarded_for.split(",")[0].strip()
    
    # X-Real-IP 헤더 확인 (nginx용)
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    
    # 기본 클라이언트 IP
    return get_remote_address(request)

# Rate Limiter 초기화
try:
    if REDIS_AVAILABLE:
        # Redis를 사용한 분산 환경 지원 (선택사항)
        # limiter = Limiter(key_func=get_client_ip, storage_uri="redis://localhost:6379/1")
        # 개발 환경에서는 메모리 기반 사용
        limiter = Limiter(
            key_func=get_client_ip,
            default_limits=["1000/hour"]  # 기본 제한: 시간당 1000회
        )
        logger.info("✅ Rate Limiter initialized (Redis available but using memory)")
    else:
        # 메모리 기반 (단일 서버용)
        limiter = Limiter(
            key_func=get_client_ip,
            default_limits=["1000/hour"]  # 기본 제한: 시간당 1000회
        )
        logger.info("✅ Rate Limiter initialized (memory-based)")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize Rate Limiter: {e}")
    # Fallback: 제한 없는 더미 limiter
    limiter = Limiter(key_func=get_client_ip)

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """
    Rate Limit 초과 시 커스텀 응답
    """
    client_ip = get_client_ip(request)
    endpoint = request.url.path
    
    # 보안 로그 기록
    logger.warning(f"🚨 Rate limit exceeded - IP: {client_ip}, Endpoint: {endpoint}")
    
    response = JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later.",
            "retry_after": exc.retry_after if hasattr(exc, 'retry_after') else 60
        }
    )
    
    # Retry-After 헤더 추가
    if hasattr(exc, 'retry_after'):
        response.headers["Retry-After"] = str(exc.retry_after)
    
    return response

# Rate Limit 설정 상수
class RateLimits:
    """Rate Limiting 설정 상수 클래스"""
    
    # 인증 관련 (보안 중요)
    AUTH_LOGIN = "5/minute"        # 로그인: 분당 5회
    AUTH_REGISTER = "3/minute"     # 회원가입: 분당 3회
    AUTH_PASSWORD_CHANGE = "3/minute"  # 비밀번호 변경: 분당 3회
    
    # API 키 관련
    API_KEY_SAVE = "10/minute"     # API 키 저장: 분당 10회
    API_KEY_DELETE = "5/minute"    # API 키 삭제: 분당 5회
    
    # AI 생성 관련 (리소스 집약적)
    AI_GENERATE = "30/minute"      # AI 생성: 분당 30회
    AI_GENERATE_MULTI = "15/minute"  # 다중 AI 생성: 분당 15회 (더 제한적)
    AI_CHAT = "60/minute"          # 채팅: 분당 60회
    
    # 일반 CRUD
    CHAT_CREATE = "20/minute"      # 채팅 생성: 분당 20회
    CHAT_DELETE = "10/minute"      # 채팅 삭제: 분당 10회
    MESSAGE_SEND = "100/minute"    # 메시지 전송: 분당 100회
    
    # 파일 업로드 (리소스 집약적)
    FILE_UPLOAD = "10/minute"      # 파일 업로드: 분당 10회
    
    # 일반 조회 (관대하게)
    GENERAL_READ = "200/minute"    # 일반 조회: 분당 200회

def get_authenticated_user_id(request: Request) -> str:
    """
    인증된 사용자의 ID를 키로 사용 (IP 기반보다 정확)
    토큰에서 사용자 ID 추출
    """
    try:
        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return get_client_ip(request)
        
        token = auth_header.split(" ")[1]
        
        # JWT 토큰 검증 및 사용자 ID 추출
        from app.core.auth import verify_token
        token_data = verify_token(token)
        
        if token_data and token_data.user_id:
            return f"user:{token_data.user_id}"
        else:
            return get_client_ip(request)
    
    except Exception as e:
        logger.debug(f"Failed to extract user ID from token: {e}")
        return get_client_ip(request)

# 사용자 기반 Rate Limiter (인증된 요청용)
user_limiter = Limiter(
    key_func=get_authenticated_user_id,
    default_limits=["500/hour"]
)