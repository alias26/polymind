import logging
from app.core.config import settings

def setup_logger(name: str) -> logging.Logger:
    """
    보안을 고려한 로거 설정
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # 중복 핸들러 방지
        handler = logging.StreamHandler()
        
        if settings.environment == "production":
            # 프로덕션: 최소한의 로깅
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            logger.setLevel(logging.WARNING)
        else:
            # 개발환경: 상세 로깅
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            logger.setLevel(logging.INFO if settings.debug else logging.WARNING)
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def log_secure(logger: logging.Logger, level: str, message: str, sensitive_data: dict = None):
    """
    민감한 정보를 안전하게 로깅
    """
    if settings.environment == "production":
        # 프로덕션에서는 민감한 정보 완전 제거
        safe_message = message.replace("API key", "API key [REDACTED]")
        getattr(logger, level.lower())(safe_message)
    else:
        # 개발환경에서는 일부 정보만 마스킹
        if sensitive_data:
            for key, value in sensitive_data.items():
                if isinstance(value, str) and len(value) > 10:
                    masked_value = f"{value[:6]}...{value[-4:]}"
                    message = message.replace(str(value), masked_value)
        
        getattr(logger, level.lower())(message)