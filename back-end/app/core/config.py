from pydantic_settings import BaseSettings
from typing import Optional, List
import secrets

class Settings(BaseSettings):
    database_url: str
    debug: bool = False
    
    # JWT Settings
    secret_key: Optional[str] = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    refresh_token_expire_days: int = 7
    
    # Encryption key for API keys
    encryption_key: Optional[str] = None
    
    # CORS settings
    allowed_origins: List[str] = ["http://localhost:8080", "http://localhost:3000"]
    
    # Production settings
    environment: str = "development"  # development, production
    
    class Config:
        env_file = ".env"
    
    def get_secret_key(self) -> str:
        """환경변수에서 SECRET_KEY를 가져오거나 안전한 키를 생성"""
        if self.secret_key:
            return self.secret_key
        
        # 프로덕션에서는 SECRET_KEY가 필수
        if self.environment == "production":
            raise ValueError("SECRET_KEY must be set in production environment")
        
        # 개발환경에서만 경고 후 임시 키 생성
        if self.debug:
            print("⚠️  WARNING: Using runtime SECRET_KEY (development only)")
        
        return secrets.token_urlsafe(32)

settings = Settings()