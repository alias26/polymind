from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
import logging
from app.api import auth_router, api_key_router, chat_router, ai_router
from app.api.user_preferences_routes import router as user_preferences_router
from app.api.rate_limit_test import router as rate_limit_test_router
from app.core.rate_limiter import limiter, rate_limit_exceeded_handler
from app.core.config import settings
from slowapi.errors import RateLimitExceeded

# 로깅 설정
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 프로덕션에서는 민감한 정보 로깅 비활성화
if not settings.debug:
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    # 민감한 API 로깅도 비활성화
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger("anthropic").setLevel(logging.ERROR)
    logging.getLogger("google").setLevel(logging.ERROR)

app = FastAPI(
    title="AI Chat Backend API", 
    version="1.0.0",
    # 프로덕션에서는 API 문서 비활성화 (보안)
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Rate Limiter 등록
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# 422 에러 핸들러 - 보안 강화
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 디버그 모드에서만 상세 로그 출력
    if settings.debug:
        logger.warning(f"Validation error: {request.method} {request.url}")
        logger.warning(f"Validation errors: {exc.errors()}")
        try:
            body = await request.body()
            logger.warning(f"Request body: {body.decode('utf-8')}")
        except:
            logger.warning("Could not decode request body")
    
    # 프로덕션에서는 간단한 에러 메시지만 반환
    if settings.environment == "production":
        return JSONResponse(
            status_code=422,
            content={"detail": "Invalid request data"}
        )
    
    # 개발환경에서는 상세 에러 정보 제공
    error_details = []
    for error in exc.errors():
        safe_error = {
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
            "type": error.get("type", "")
        }
        error_details.append(safe_error)
    
    return JSONResponse(
        status_code=422,
        content={"detail": error_details}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router)
app.include_router(api_key_router)
app.include_router(chat_router)
app.include_router(ai_router)
app.include_router(user_preferences_router)
# 테스트 라우터는 개발환경에서만 사용
if settings.debug:
    app.include_router(rate_limit_test_router)

@app.get("/")
async def root():
    return {
        "message": "AI Chat Backend API", 
        "version": "1.0.0",
        "status": "running",
        "environment": settings.environment
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.debug,  # 프로덕션에서는 reload=False
        access_log=settings.debug  # 프로덕션에서는 access_log 최소화
    )