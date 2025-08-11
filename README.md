# PolyMind 🤖

**다중 AI 서비스 통합 웹 애플리케이션**

OpenAI GPT, Anthropic Claude, Google Gemini 등 여러 AI 모델을 하나의 인터페이스에서 사용할 수 있는 풀스택 웹 애플리케이션입니다. 사용자 인증 시스템과 실시간 스트리밍 채팅 기능을 포함합니다. Claude COde를 사용해서 바이브 코딩해서 개발한 프로젝트입니다.

## 📸 실행 화면
### 🎥 데모 영상
![PolyMind 데모](./assets/PolyMind%20-%20AI%20Chat%20Assistant.gif)

### 첫 화면 인터페이스
![PolyMind 메인 화면](./assets/introduction.png)

### 새 채팅 생성
![새 채팅 화면](./assets/new_chat.png)

### 사용자 설정
#### API 키 설정
![API 키 관리](./assets/api_key.png)

#### 사용자 기본 프리셋 설정
![사용자 설정](./assets/preset.png)

#### 사용자 기본 프롬프트 관리
![프롬프트 관리](./assets/prompt.png)

### 개별 채팅 설정
![개별 채팅 프롬프트](./assets/independent_chat_prompt.png)

![개별 채팅 설정](./assets/independent_chat_setting.png)

## ✨ 주요 특징

### 🤖 **다중 AI 모델 지원**
- **OpenAI**: GPT-4.1/Mini/Nano, GPT-4o/Mini, GPT-3.5 Turbo, o3/o4-mini
- **Anthropic**: Claude Opus 4.1/4, Claude Sonnet 4/3.7/3.5, Claude Haiku 3.5/3
- **Google**: Gemini 2.5 Pro/Flash (최대 200만 토큰)
- **실시간 스트리밍**: 모든 모델 응답 실시간 표시
- **모델별 최적화**: 각 AI 모델에 특화된 파라미터 설정

### 🔐 **인증 시스템**
- **회원가입/로그인**: 이메일 또는 사용자 ID 지원
- **이메일 인증**: 6자리 인증 코드 (개발환경 콘솔 출력)
- **비밀번호 관리**: 안전한 재설정, 강도 검증, 재사용 방지
- **아이디 찾기**: 이메일을 통한 사용자 ID 찾기
- **JWT 보안**: Access + Refresh Token, 자동 갱신

### 💬 **채팅 기능**
- **다중 채팅방**: 독립적인 채팅 세션 관리
- **마크다운 지원**: 코드 하이라이팅, 수학 공식, 테이블
- **시스템 프롬프트**: 채팅별 커스텀 지시사항 설정
- **이미지 분석**: 멀티모달 AI 모델 지원
- **채팅 히스토리**: 대화 기록 저장

### 🛡️ **보안 기능**
- **API 키 암호화**: Fernet 암호화를 통한 안전한 저장
- **Rate Limiting**: API 요청 제한
- **XSS/CSRF 방지**: 기본 보안 조치 적용
- **데이터 검증**: 입력 데이터 검증


## 🏗️ 기술 스택

### Backend (FastAPI)
```
🔧 FastAPI + SQLAlchemy + PostgreSQL
🔐 JWT 인증 + Refresh Token
🤖 OpenAI + Anthropic + Google AI 통합
🛡️ Rate Limiting + API 키 암호화
⚡ 비동기 처리 + 스트리밍 응답
🐳 Docker 컨테이너화
```

### Frontend (Vue.js 3)
```
⚡ Vue 3 Composition API + Pinia
🎨 반응형 디자인 + FontAwesome
📝 Markdown-it + DOMPurify
🔌 Axios 인터셉터 + 자동 토큰 관리
🚀 Vue CLI + Webpack 최적화
📱 PWA 지원
```

### Infrastructure
```
🐳 Docker + Docker Compose
🌐 Nginx (프론트엔드 서빙)
🗄️ PostgreSQL 15
☁️ Railway/Vercel 배포 지원
🔒 Let's Encrypt SSL
```

## 🚀 빠른 시작

### 📋 필수 요구사항
- **Docker & Docker Compose** (권장)
- **Node.js** 18+ (수동 설치 시)
- **Python** 3.8+ (수동 설치 시)  
- **PostgreSQL** 12+ (수동 설치 시)

### ⚡ 원클릭 실행 (Docker)
```bash
# 저장소 클론
git clone https://github.com/alias26/polymind.git
cd polymind

# 전체 스택 실행 (백엔드 + 프론트엔드 + 데이터베이스)
docker-compose up -d

# 브라우저에서 접속
# 프론트엔드: http://localhost:3000
# 백엔드 API: http://localhost:8000
# API 문서: http://localhost:8000/docs
```

### 🛠️ 수동 설치 (개발환경)

<details>
<summary>📂 상세 설치 가이드 보기</summary>

#### 1. 백엔드 설정
```bash
cd back-end

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
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

#### 2. 프론트엔드 설정
```bash
cd front-end

# 의존성 설치
npm install

# 환경 변수 설정 (선택사항)
echo "VUE_APP_API_BASE_URL=http://localhost:8000" > .env

# 개발 서버 실행
npm run serve
```

#### 3. 데이터베이스 설정
```bash
# PostgreSQL 설치 및 실행
# Ubuntu/Debian
sudo apt update && sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql && brew services start postgresql

# 데이터베이스 생성
sudo -u postgres createdb polymind
```

</details>

### 🔑 API 키 설정 (선택사항)

AI 모델을 사용하려면 해당 서비스의 API 키가 필요합니다:

- **OpenAI**: [platform.openai.com](https://platform.openai.com) → API Keys
- **Anthropic**: [console.anthropic.com](https://console.anthropic.com) → API Keys  
- **Google**: [ai.google.dev](https://ai.google.dev) → Get API Key

> 💡 **팁**: API 키는 애플리케이션 내에서 안전하게 암호화되어 저장됩니다.

## 📁 프로젝트 구조

```
polymind/
├── 📄 README.md                 # 이 파일
├── 📄 docker-compose.yml        # Docker 전체 스택 설정
├── 📄 .gitignore                # Git 무시 파일
├── 📁 screenshots/              # 실행 화면 이미지
├── 📁 demo/                     # 데모 영상
├── 📁 back-end/                 # FastAPI 백엔드
│   ├── 📄 README.md            # 백엔드 상세 문서
│   ├── 📄 main.py              # API 서버 진입점
│   ├── 📄 requirements.txt     # Python 의존성
│   ├── 📄 Dockerfile           # 백엔드 Docker 설정
│   └── 📁 app/                 # 애플리케이션 코드
│       ├── 📁 api/             # REST API 엔드포인트
│       ├── 📁 core/            # 핵심 설정 (인증, DB 등)
│       ├── 📁 models/          # 데이터베이스 모델
│       ├── 📁 services/        # AI 서비스 통합
│       └── 📁 schemas/         # API 스키마
└── 📁 front-end/               # Vue.js 프론트엔드
    ├── 📄 README.md           # 프론트엔드 상세 문서
    ├── 📄 package.json        # Node.js 의존성
    ├── 📄 Dockerfile          # 프론트엔드 Docker 설정
    └── 📁 src/                # Vue.js 소스코드
        ├── 📁 views/          # 페이지 컴포넌트
        ├── 📁 components/     # 재사용 컴포넌트
        ├── 📁 store/          # Pinia 상태관리
        └── 📁 apis/           # API 통신 레이어
```

## 🎯 사용법

### 1️⃣ 회원가입 및 로그인
1. **회원가입**: 이메일과 원하는 사용자 ID로 가입
2. **이메일 인증**: 콘솔에 출력된 6자리 코드로 인증 (개발환경)
3. **로그인**: 이메일 또는 사용자 ID로 로그인

### 2️⃣ API 키 설정
1. **프로필 설정** → **API 키 관리**
2. 원하는 AI 서비스의 API 키 입력 및 저장
3. API 키 유효성 자동 검증

### 3️⃣ AI 채팅 시작
1. **새 채팅** 버튼으로 채팅방 생성
2. **모델 선택**: OpenAI, Anthropic, Google 중 선택
3. **파라미터 조정**: Temperature, Max Tokens 설정
4. **채팅 시작**: 실시간 스트리밍으로 AI 응답 확인

### 4️⃣ 추가 기능 활용
- **시스템 프롬프트**: 채팅별 역할 지정
- **이미지 업로드**: 멀티모달 모델로 이미지 분석
- **마크다운**: 코드, 수학 공식, 테이블 자동 렌더링
- **채팅 관리**: 제목 변경, 삭제, 히스토리 검색

## 🙏 사용된 기술

PolyMind는 다음 오픈소스 기술들로 구현되었습니다:

- [FastAPI](https://fastapi.tiangolo.com/) - Python 웹 프레임워크
- [Vue.js](https://vuejs.org/) - JavaScript 프론트엔드 프레임워크
- [PostgreSQL](https://www.postgresql.org/) - 관계형 데이터베이스
- [OpenAI](https://openai.com/), [Anthropic](https://anthropic.com/), [Google AI](https://ai.google/) - AI 모델 API

---

<div align="center">

**Made with ❤️ by [Your Name]**

</div>
