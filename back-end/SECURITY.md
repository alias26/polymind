# 🔒 보안 설정 가이드

## JWT 보안 설정

### 1. SECRET_KEY 설정

**개발 환경:**
```bash
# 안전한 키 생성
python3 generate_keys.py

# .env 파일에 복사
SECRET_KEY=생성된_키_값
```

**프로덕션 환경:**
```bash
# 환경변수로 직접 설정 (권장)
export SECRET_KEY="your-production-secret-key"
export ENCRYPTION_KEY="your-production-encryption-key"
```

### 2. 키 생성 방법

```python
# JWT SECRET_KEY
import secrets
secret_key = secrets.token_urlsafe(32)

# API 키 암호화용 ENCRYPTION_KEY  
from cryptography.fernet import Fernet
encryption_key = Fernet.generate_key().decode()
```

### 3. 보안 체크리스트

- [x] SECRET_KEY를 환경변수로 관리
- [x] API 키 암호화 저장
- [x] JWT 토큰 만료 시간 설정
- [ ] 토큰 블랙리스트 구현
- [ ] Rate Limiting 적용
- [ ] HTTPS 강제화
- [ ] 보안 로깅 구현

### 4. 프로덕션 환경 권장 사항

1. **SECRET_KEY는 절대 코드에 하드코딩하지 마세요**
2. **정기적으로 키를 교체하세요**
3. **환경변수나 시크릿 매니저 사용**
4. **로그에 민감한 정보가 기록되지 않도록 주의**

### 5. 현재 보안 수준

✅ **구현된 보안 기능:**
- JWT 기반 인증
- 사용자별 데이터 격리  
- API 키 암호화 저장
- 환경변수 기반 설정

⚠️ **추가 보안 강화 필요:**
- 토큰 블랙리스트
- Rate Limiting
- 보안 모니터링
- HTTPS 강제화