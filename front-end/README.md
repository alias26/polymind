# PolyMind Frontend

PolyMind의 Vue.js 3 기반 프론트엔드 웹 애플리케이션입니다. 다중 AI 모델과의 실시간 채팅, 사용자 인증 시스템, 반응형 UI를 제공합니다.

## 🏗️ 기술 스택 & 특징

- **프레임워크**: Vue.js 3 (Composition API)
- **상태관리**: Pinia 3.0.3
- **라우팅**: Vue Router 4.0.3 (인증 가드 포함)
- **HTTP 클라이언트**: Axios 1.10.0 (인터셉터, 토큰 관리)
- **마크다운**: markdown-it + DOMPurify (XSS 방지)
- **UI/UX**: 반응형 디자인, FontAwesome 아이콘
- **빌드**: Vue CLI 5.0.0, Webpack 최적화

## 📁 프로젝트 구조

```
front-end/
├── package.json              # 의존성 및 스크립트
├── vue.config.js             # Vue CLI 설정
├── Dockerfile                # Docker 이미지 빌드
├── nginx.conf                # 프로덕션 Nginx 설정
├── public/
│   ├── index.html           # HTML 템플릿
│   ├── favicon.svg          # 파비콘
│   └── manifest.json        # PWA 설정
├── src/
│   ├── main.js              # Vue 앱 엔트리포인트
│   ├── App.vue              # 루트 컴포넌트 (네비게이션 제어)
│   ├── router/
│   │   └── index.js         # 라우팅 설정 (인증 가드)
│   ├── store/               # Pinia 상태관리
│   │   ├── auth.js          # 사용자 인증 상태
│   │   ├── chatStore.js     # 채팅 관리 상태
│   │   ├── apiKeys.js       # API 키 관리
│   │   └── loading.js       # 로딩 상태
│   ├── views/               # 페이지 컴포넌트
│   │   ├── LandingView.vue  # 랜딩 페이지
│   │   ├── LoginView.vue    # 로그인 페이지
│   │   ├── SignUpView.vue   # 회원가입 페이지
│   │   ├── ResetPasswordView.vue # 비밀번호 재설정
│   │   ├── ChatView.vue     # 메인 채팅 인터페이스
│   │   └── ProfileView.vue  # 사용자 프로필 설정
│   ├── components/          # 재사용 컴포넌트
│   │   ├── chat/           # 채팅 관련
│   │   │   ├── ChatMainArea.vue    # 채팅 메시지 영역
│   │   │   ├── ChatSidebar.vue     # 채팅방 목록
│   │   │   ├── ChatSettings.vue    # 채팅 설정 모달
│   │   │   ├── EmptyChat.vue       # 빈 채팅 상태
│   │   │   └── NewChatModal.vue    # 새 채팅 생성
│   │   ├── common/         # 공통 컴포넌트
│   │   │   ├── NavigationBar.vue   # 네비게이션 바
│   │   │   ├── MarkdownRenderer.vue # 마크다운 렌더링
│   │   │   └── ToastNotification.vue # 토스트 알림
│   │   ├── login/          # 인증 관련
│   │   │   ├── FindIdModal.vue     # 아이디 찾기 모달
│   │   │   └── FindPasswordModal.vue # 비밀번호 찾기 모달
│   │   └── profile/        # 프로필 관련
│   │       └── ProfileSidebar.vue  # 프로필 사이드바
│   ├── apis/               # API 통신 레이어
│   │   ├── axiosConfig.js  # Axios 설정 (인터셉터)
│   │   ├── authApi.js      # 인증 API
│   │   ├── chatApi.js      # 채팅 API
│   │   ├── aiApi.js        # AI 서비스 API
│   │   └── apiKeyApi.js    # API 키 관리 API
│   ├── config/
│   │   └── modelSettings.js # AI 모델 설정 및 파라미터
│   ├── utils/              # 유틸리티 함수
│   │   ├── toastService.js # 토스트 알림 서비스
│   │   ├── userUtils.js    # 사용자 관련 유틸리티
│   │   └── performance.js  # 성능 최적화 도구
│   └── assets/             # 정적 자원
│       ├── buttons.css     # 버튼 스타일
│       ├── z-index.css     # z-index 관리
│       └── logo.png        # 로고 이미지
└── start.sh               # 개발 서버 실행 스크립트
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
npm install

# 환경 변수 설정 (선택사항)
# .env 파일 생성
VUE_APP_API_BASE_URL=http://localhost:8000

# 개발 서버 실행
npm run serve
# 또는
./start.sh

# 빌드 (프로덕션)
npm run build
```

## 🎯 주요 기능

### 🔐 사용자 인증 시스템

- **회원가입/로그인**: 이메일 또는 사용자 ID 지원
- **이메일 인증**: 회원가입 시 6자리 인증 코드
- **비밀번호 관리**: 재설정, 변경, 강도 검증
- **아이디 찾기**: 이메일을 통한 사용자 ID 찾기
- **JWT 토큰 관리**: 자동 갱신, 만료 시 자동 로그아웃

### 💬 실시간 AI 채팅

- **다중 채팅방**: 독립적인 채팅 세션 관리
- **스트리밍 응답**: AI 응답 실시간 표시
- **마크다운 지원**: 코드 하이라이팅, 수학 공식, 테이블
- **시스템 프롬프트**: 채팅별 커스텀 지시사항 설정
- **이미지 업로드**: 멀티모달 AI 모델 지원
- **채팅 히스토리**: 무제한 대화 기록 저장

### 🤖 AI 모델 관리

- **모델 선택**: OpenAI, Anthropic, Google 모델 선택
- **파라미터 조정**: Temperature, Max Tokens 실시간 조정
- **API 키 관리**: 안전한 개인 API 키 저장 및 검증
- **모델별 최적화**: 각 모델에 특화된 설정값 제공

### 👤 사용자 설정

- **프로필 관리**: 개인정보 수정, 비밀번호 변경
- **채팅 설정**: 기본 모델, 파라미터 설정
- **프리셋 관리**: 자주 사용하는 프롬프트 저장
- **사용자 선호도**: 개인화된 설정 저장

## 🎨 UI/UX 특징

### 반응형 디자인

- **모바일 우선**: 모든 화면 크기 최적화
- **유연한 레이아웃**: CSS Grid + Flexbox
- **터치 친화적**: 모바일 터치 인터페이스 최적화

### 사용자 경험

- **실시간 피드백**: 스트리밍 텍스트, 타이핑 인디케이터
- **직관적 네비게이션**: 명확한 정보 구조
- **키보드 지원**: 접근성 및 효율성 고려
- **로딩 상태**: 명확한 로딩 인디케이터

## 🔒 보안 기능

### 클라이언트 보안

- **XSS 방지**: DOMPurify를 통한 마크다운 콘텐츠 정화
- **라우트 가드**: 인증 기반 페이지 접근 제어
- **토큰 보안**: 자동 갱신, 안전한 저장
- **HTTPS 강제**: 프로덕션 환경 SSL 설정

### 데이터 보호

- **민감정보 보호**: API 키 클라이언트 측 검증
- **세션 관리**: 안전한 로그인 상태 유지
- **입력 검증**: 클라이언트/서버 이중 검증

## 📊 상태 관리 구조

### Pinia Store

```javascript
// 인증 상태 (auth.js)
- user: 현재 사용자 정보
- isAuthenticated: 로그인 상태
- tokens: JWT 토큰 관리
- login(), logout(), refreshToken()

// 채팅 상태 (chatStore.js)
- currentChat: 현재 활성 채팅
- chatList: 채팅방 목록
- messages: 메시지 배열
- isStreaming: 스트리밍 상태
- sendMessage(), createChat(), deleteChat()

// API 키 관리 (apiKeys.js)
- keys: 사용자 API 키 목록
- verification: 키 검증 상태
- saveKey(), verifyKey(), deleteKey()
```

## 🔌 API 통신

### Axios 인터셉터

- **요청 인터셉터**: JWT 토큰 자동 추가
- **응답 인터셉터**: 401 에러 시 자동 토큰 갱신
- **에러 처리**: 통합 에러 상태 관리

### API 레이어

- **authApi.js**: 인증 관련 API 호출
- **chatApi.js**: 채팅 CRUD 작업
- **aiApi.js**: AI 모델 통신 (스트리밍)
- **apiKeyApi.js**: API 키 관리

---
