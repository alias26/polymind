from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user
from app.crud.api_key_crud import (
    create_or_update_api_key, 
    get_api_key, 
    get_all_user_api_keys,
    delete_api_key,
    delete_all_user_api_keys
)
from app.schemas.api_key_schemas import (
    ApiKeyCreate, 
    ApiKeyResponse, 
    ApiKeyValidate, 
    ApiKeyValidationResult
)
from app.models.user import User

router = APIRouter(prefix="/api/v1/api-keys", tags=["api-keys"])

@router.post("/", response_model=ApiKeyResponse)
def save_api_key(
    api_key_data: ApiKeyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # provider 유효성 검사 및 정규화
    valid_providers = ["openai", "anthropic", "google"]
    provider_aliases = {
        "gpt": "openai",
        "chatgpt": "openai",
        "openai": "openai",
        "anthropic": "anthropic",
        "claude": "anthropic",
        "google": "google",
        "gemini": "google"
    }
    
    normalized_provider = provider_aliases.get(api_key_data.provider.lower())
    if not normalized_provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid provider. Supported providers: {list(provider_aliases.keys())}"
        )
    
    # API 키 형식 검증
    api_key = api_key_data.apiKey.strip()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="API key cannot be empty"
        )
    
    # 각 provider별 형식 검증 (실제 형식에 맞춤)
    is_valid = False
    if normalized_provider == "openai":
        # OpenAI: sk- 시작, 최소 48자 또는 sk-proj- 시작, 최소 56자
        is_valid = (api_key.startswith("sk-") and len(api_key) >= 48) or \
                   (api_key.startswith("sk-proj-") and len(api_key) >= 56)
    elif normalized_provider == "anthropic":
        # Anthropic: sk-ant- 시작, 최소 80자
        is_valid = api_key.startswith("sk-ant-") and len(api_key) >= 80
    elif normalized_provider == "google":
        # Google: AIza 시작, 정확히 39자
        is_valid = api_key.startswith("AIza") and len(api_key) == 39
    
    if not is_valid:
        provider_formats = {
            "openai": "sk-... (최소 48자) 또는 sk-proj-... (최소 56자)",
            "anthropic": "sk-ant-... (최소 80자)",
            "google": "AIza... (정확히 39자)"
        }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid API key format for {normalized_provider}. Expected format: {provider_formats[normalized_provider]}"
        )
    
    # 정규화된 provider로 새 객체 생성
    normalized_api_key_data = ApiKeyCreate(
        provider=normalized_provider,
        apiKey=api_key
    )
    
    db_api_key = create_or_update_api_key(db, current_user.id, normalized_api_key_data)
    return db_api_key

@router.get("/", response_model=List[ApiKeyResponse])
def get_all_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_user_api_keys(db, current_user.id)

@router.get("/{provider}", response_model=ApiKeyResponse)
def get_api_key_by_provider(
    provider: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    api_key = get_api_key(db, current_user.id, provider)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    return api_key

@router.get("/{provider}/decrypted")
def get_decrypted_api_key(
    provider: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """복호화된 API 키 반환 (보안상 주의해서 사용)"""
    from app.crud.api_key_crud import decrypt_api_key
    
    
    api_key = get_api_key(db, current_user.id, provider)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    
    try:
        decrypted_key = decrypt_api_key(api_key.encrypted_key)
        return {
            "provider": api_key.provider,
            "api_key": decrypted_key,
            "is_active": api_key.is_active
        }
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to decrypt API key: {str(e)}"
        )

@router.delete("/{provider}")
def delete_api_key_by_provider(
    provider: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = delete_api_key(db, current_user.id, provider)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    return {"message": "API key deleted successfully"}

@router.delete("/")
def delete_all_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    count = delete_all_user_api_keys(db, current_user.id)
    return {"message": f"{count} API keys deleted successfully"}

@router.post("/validate", response_model=ApiKeyValidationResult)
def validate_api_key(
    validation_data: ApiKeyValidate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 기본 형식 검증
    provider = validation_data.provider
    api_key = validation_data.apiKey
    
    is_valid = False
    message = "Invalid API key format"
    
    try:
        if provider == "openai":
            if (api_key.startswith("sk-") and len(api_key) >= 48) or \
               (api_key.startswith("sk-proj-") and len(api_key) >= 56):
                is_valid = True
                message = "Valid OpenAI API key format"
        elif provider == "anthropic":
            if api_key.startswith("sk-ant-") and len(api_key) >= 80:
                is_valid = True
                message = "Valid Anthropic API key format"
        elif provider == "google":
            if api_key.startswith("AIza") and len(api_key) == 39:
                is_valid = True
                message = "Valid Google API key format"
        
        # 실제 API 호출로 검증하는 로직은 여기에 추가 가능
        
    except Exception as e:
        is_valid = False
        message = f"Validation error: {str(e)}"
    
    return ApiKeyValidationResult(
        provider=provider,
        is_valid=is_valid,
        message=message
    )