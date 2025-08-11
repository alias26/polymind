from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserPreferencesCreate(BaseModel):
    default_system_prompt: Optional[str] = None

class UserPreferencesUpdate(BaseModel):
    default_system_prompt: Optional[str] = None

class UserPreferencesResponse(BaseModel):
    user_id: str
    default_system_prompt: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True