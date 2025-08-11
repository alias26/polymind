# PolyMind Backend API

PolyMind의 FastAPI 기반 백엔드 서버입니다. 다중 AI 서비스 통합, 사용자 인증 시스템, 채팅 관리 등의 핵심 기능을 제공합니다.

## 🏗️ 기술 스택 & 특징

- **웹 프레임워크**: FastAPI + SQLAlchemy ORM + PostgreSQL
- **인증**: JWT (Access + Refresh Token) + 이메일 인증 시스템
- **AI 통합**: OpenAI GPT, Anthropic Claude, Google Gemini
- **보안**: API 키 암호화 저장, Rate Limiting, CORS 설정
- **실시간**: 스트리밍 응답, 비동기 처리
- **배포**: Docker 컨테이너화 지원

## 📁 프로젝트 구조

```
back-end/
├── main.py                    # FastAPI 애플리케이션 진입점
├── requirements.txt           # Python 의존성
├── Dockerfile                 # Docker 이미지 빌드
├── alembic/                   # DB 마이그레이션
├── app/
│   ├── api/                   # REST API 엔드포인트
│   │   ├── auth_routes.py     # 사용자 인증 (로그인/회원가입/이메일인증)
│   │   ├── chat_routes.py     # 채팅방 관리
│   │   ├── ai_routes.py       # AI 서비스 통합 API
│   │   ├── api_key_routes.py  # API 키 관리 (암호화 저장)
│   │   └── user_preferences_routes.py # 사용자 설정
│   ├── core/                  # 핵심 설정 및 유틸리티
│   │   ├── config.py          # 환경 설정 (JWT, CORS, DB)
│   │   ├── database.py        # DB 연결 및 세션 관리
│   │   ├── auth.py            # JWT 토큰 생성/검증
│   │   └── rate_limiter.py    # API 요청 제한
│   ├── models/                # SQLAlchemy 데이터베이스 모델
│   │   ├── user.py            # 사용자 모델
│   │   ├── chat.py            # 채팅방 모델
│   │   ├── message.py         # 메시지 모델
│   │   ├── api_key.py         # API 키 모델 (암호화)
│   │   ├── email_verification.py # 이메일 인증 토큰
│   │   └── user_preferences.py # 사용자 설정
│   ├── services/              # 비즈니스 로직 및 외부 서비스
│   │   ├── ai_manager.py      # AI 서비스 통합 관리
│   │   ├── openai_service.py  # OpenAI GPT 연동
│   │   ├── anthropic_service.py # Anthropic Claude 연동
│   │   ├── gemini_service.py  # Google Gemini 연동
│   │   └── email_service.py   # 이메일 서비스 (개발용 콘솔)
│   ├── crud/                  # 데이터베이스 CRUD 작업
│   ├── schemas/               # Pydantic 스키마 (데이터 검증)
│   └── middleware/            # 커스텀 미들웨어
└── start_server.sh           # 개발 서버 실행 스크립트
```

## 🚀 빠른 시작

### Docker로 실행 (권장)
```bash
# 루트 디렉토리에서 전체 스택 실행
cd ..
docker-compose up -d
```

### 수동 실행
```bash
# 의존성 설치
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일 생성)
DATABASE_URL=postgresql://username:password@localhost:5432/polymind
JWT_SECRET_KEY=your-super-secret-jwt-key-here
ENCRYPTION_KEY=your-fernet-encryption-key-here

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
./start_server.sh
```

## 🔌 주요 API 엔드포인트

### 인증 시스템 (`/api/v1/auth`)
- **회원가입/로그인**: 이메일 또는 ID 지원
- **JWT 토큰 관리**: Access + Refresh Token
- **이메일 인증**: 회원가입 시 이메일 인증 (개발환경 콘솔 출력)
- **비밀번호 재설정**: 이메일을 통한 안전한 재설정
- **아이디 찾기**: 이메일로 사용자 ID 찾기

### 채팅 관리 (`/api/v1/chat`)
- **채팅방 CRUD**: 생성, 조회, 삭제, 제목 변경
- **메시지 관리**: 채팅 메시지 저장 및 조회
- **시스템 프롬프트**: 채팅별 커스텀 프롬프트 설정

### AI 서비스 (`/api/v1/ai`)
- **통합 채팅 API**: 모든 AI 모델 통합 인터페이스
- **스트리밍 응답**: 실시간 응답 스트리밍
- **이미지 분석**: 멀티모달 AI 모델 지원
- **모델 목록**: 사용 가능한 AI 모델 조회

### API 키 관리 (`/api/v1/api-keys`)
- **암호화 저장**: Fernet 암호화를 통한 안전한 저장
- **키 검증**: API 키 유효성 실시간 확인
- **다중 제공업체**: OpenAI, Anthropic, Google 개별 관리

## 🤖 지원 AI 모델

### OpenAI
- **GPT-5 시리즈**: GPT-5, GPT-5 Mini, GPT-5 Nano, GPT-5 Chat
- **GPT-4.1 시리즈**: GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano
- **GPT-4o 시리즈**: GPT-4o, GPT-4o Mini (멀티모달)
- **추론 모델**: o3, o4-mini
- **GPT-3.5**: GPT-3.5 Turbo

### Anthropic Claude
- **Claude 4 시리즈**: Opus 4.1, Opus 4, Sonnet 4
- **Claude 3.7**: Sonnet 3.7
- **Claude 3.5**: Sonnet 3.5, Haiku 3.5
- **Claude 3**: Haiku 3

### Google Gemini
- **Gemini 2.5**: Pro, Flash (최대 200만 토큰)

## 🔒 보안 기능

### 인증 보안
- **JWT 토큰**: Access Token (2시간) + Refresh Token (7일)
- **토큰 블랙리스트**: 로그아웃 시 토큰 무효화
- **비밀번호 보안**: bcrypt 해싱, 직전 비밀번호 재사용 방지
- **이메일 인증**: 회원가입 시 이메일 검증

### API 보안
- **API 키 암호화**: 사용자 API 키 Fernet 암호화 저장
- **Rate Limiting**: 엔드포인트별 요청 제한
- **CORS 설정**: 도메인별 접근 제어
- **보안 헤더**: XSS, CSRF 방지 헤더 설정

## 📊 데이터베이스 스키마

### ER 다이어그램
```mermaid
erDiagram
    Users {
        varchar id PK
        varchar email UK
        varchar password
        varchar name
        boolean is_email_verified
        timestamp created_at
        timestamp updated_at
    }
    
    Chats {
        uuid id PK
        varchar user_id FK
        varchar title
        text system_prompt
        timestamp created_at
        timestamp updated_at
    }
    
    Messages {
        uuid id PK
        uuid chat_id FK
        varchar role
        text content
        integer order_index
        timestamp created_at
    }
    
    ApiKeys {
        uuid id PK
        varchar user_id FK
        varchar provider
        text encrypted_key
        boolean is_active
        timestamp created_at
    }
    
    EmailVerification {
        uuid id PK
        varchar user_id FK
        varchar code
        timestamp expires_at
        boolean is_used
        timestamp created_at
    }
    
    PasswordResetTokens {
        uuid id PK
        varchar user_id FK
        uuid token
        timestamp expires_at
        boolean is_used
        timestamp created_at
    }
    
    UserPreferences {
        uuid id PK
        varchar user_id FK
        json preferences
        timestamp created_at
        timestamp updated_at
    }

    Users ||--o{ Chats : "has many"
    Users ||--o{ ApiKeys : "has many"
    Users ||--o{ EmailVerification : "has many"
    Users ||--o{ PasswordResetTokens : "has many"
    Users ||--|| UserPreferences : "has one"
    Chats ||--o{ Messages : "contains"
```

### 주요 테이블 설명
- **Users**: 사용자 정보 (이메일 인증 포함)
- **Chats**: 채팅방 정보 (시스템 프롬프트 포함)
- **Messages**: 채팅 메시지 (사용자/AI 구분, 순서 보장)
- **ApiKeys**: 암호화된 사용자 API 키 (제공업체별)
- **EmailVerification**: 이메일 인증 6자리 코드
- **PasswordResetTokens**: 비밀번호 재설정 UUID 토큰
- **UserPreferences**: 사용자 설정 (JSON 형태)

---
