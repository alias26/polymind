from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ApiKeyCreate(BaseModel):
    provider: str
    apiKey: str

class ApiKeyResponse(BaseModel):
    provider: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ApiKeyValidate(BaseModel):
    provider: str
    apiKey: str

class ApiKeyValidationResult(BaseModel):
    provider: str
    is_valid: bool
    message: Optional[str] = None