<template>
  <div class="login-container">
    <!-- 뒤로가기 버튼 -->
    <button class="btn-base btn-icon back-button" @click="goBack">
      <i class="fas fa-arrow-left"></i>
      <span>뒤로가기</span>
    </button>

    <div class="login-card">
      <!-- 로고 영역 -->
      <div class="logo-section">
        <div class="logo">
          <h1>PolyMind</h1>
          <p class="tagline">다양한 AI와 함께하는 지능형 대화 플랫폼</p>
        </div>
      </div>

      <!-- 로그인 폼 -->
      <div class="login-form">
        <h2>로그인</h2>

        <form @submit.prevent="handleLogin">
          <!-- 이메일/아이디 입력 -->
          <div class="input-group">
            <label for="identifier" class="input-label"
              >이메일 또는 아이디</label
            >
            <input
              id="identifier"
              v-model="loginForm.identifier"
              type="text"
              class="input-field"
              placeholder="이메일 또는 아이디를 입력하세요"
              required
            />
          </div>

          <!-- 비밀번호 입력 -->
          <div class="input-group">
            <label for="password" class="input-label">비밀번호</label>
            <div class="password-input-wrapper">
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="input-field password-field"
                placeholder="비밀번호를 입력하세요"
                required
              />
              <button
                type="button"
                class="password-toggle"
                @click="togglePassword"
              >
                <i
                  :class="showPassword ? 'fas fa-eye' : 'fas fa-eye-slash'"
                ></i>
              </button>
            </div>
          </div>

          <!-- 로그인 옵션 -->
          <div class="login-options">
            <label class="checkbox-wrapper">
              <input
                v-model="loginForm.rememberMe"
                type="checkbox"
                class="checkbox"
              />
              <span class="checkbox-label">로그인 상태 유지</span>
            </label>
          </div>

          <!-- 로그인 버튼 -->
          <button
            type="submit"
            class="btn-base btn-primary btn-full"
            :class="{ 'btn-loading': isLoading }"
            :disabled="isLoading"
          >
            {{ isLoading ? '로그인 중...' : '로그인' }}
          </button>

          <!-- 에러 메시지 -->
          <div v-if="errorMessage" class="error-message">
            <i class="fas fa-exclamation-triangle"></i>
            {{ errorMessage }}
          </div>
        </form>

        <!-- 하단 링크들 -->
        <div class="bottom-links">
          <button class="btn-base btn-link" @click="findId">
            <i class="fas fa-user"></i>
            아이디 찾기
          </button>
          <span class="divider">|</span>
          <button class="btn-base btn-link" @click="findPassword">
            <i class="fas fa-key"></i>
            비밀번호 찾기
          </button>
        </div>

        <!-- 회원가입 링크 -->
        <div class="signup-section">
          <p>계정이 없으신가요?</p>
          <button class="btn-base btn-secondary" @click="goToSignup">
            회원가입
          </button>
        </div>
      </div>
    </div>

    <!-- 아이디 찾기 모달 -->
    <FindIdModal :show="showFindIdModal" @close="closeFindIdModal" />

    <!-- 비밀번호 찾기 모달 -->
    <FindPasswordModal
      :show="showFindPasswordModal"
      @close="closeFindPasswordModal"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useLoadingStore } from '@/store/loading'
import { useAuthStore } from '@/store/auth'
import FindIdModal from '@/components/login/FindIdModal.vue'
import FindPasswordModal from '@/components/login/FindPasswordModal.vue'

const router = useRouter()
const loadingStore = useLoadingStore()
const authStore = useAuthStore()

// 폼 데이터
const loginForm = reactive({
  identifier: '', // email -> identifier로 변경
  password: '',
  rememberMe: false,
})

// 상태 관리
const showPassword = ref(false)
const errorMessage = ref('')
const showFindIdModal = ref(false)
const showFindPasswordModal = ref(false)

// 로딩 상태는 전역 스토어에서 가져옴
const isLoading = computed(() => loadingStore.isOperationLoading('login'))

// 비밀번호 표시/숨김 토글
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// 로그인 처리
const handleLogin = async () => {
  if (isLoading.value) return

  errorMessage.value = ''
  loadingStore.startOperation('login', '로그인 중...')

  try {
    // 백엔드 API 호출
    const { authApi } = await import('@/apis/authApi')
    const response = await authApi.login({
      identifier: loginForm.identifier,
      password: loginForm.password,
    })

    // 인증 스토어를 통한 로그인 처리
    if (response.access_token) {
      // auth store의 login 메소드 사용
      authStore.login(response)

      // 사용자 정보를 별도로 가져오기
      try {
        const { authApi } = await import('@/apis/authApi')
        const userInfo = await authApi.getUserInfo()
        authStore.updateUser(userInfo)
      } catch (error) {
        console.error('사용자 정보 가져오기 실패:', error)
      }

      // 로그인 상태 유지 옵션 처리
      if (loginForm.rememberMe) {
        localStorage.setItem('remember_me', 'true')
      }

      // 성공 메시지 (선택사항)

      // Vue의 반응성 업데이트를 기다린 후 리다이렉트
      await nextTick()
      router.push('/chat')
    }
  } catch (error) {
    console.error('로그인 오류:', error)
    if (error.message.includes('401') || error.message.includes('Incorrect')) {
      errorMessage.value = 'ID/이메일 또는 비밀번호가 올바르지 않습니다.'
    } else if (
      error.message.includes('network') ||
      error.message.includes('연결')
    ) {
      errorMessage.value = '네트워크 연결을 확인해주세요.'
    } else {
      errorMessage.value = '로그인 중 오류가 발생했습니다. 다시 시도해주세요.'
    }
  } finally {
    loadingStore.stopOperation('login')
  }
}

// 아이디 찾기
const findId = () => {
  showFindIdModal.value = true
}

const closeFindIdModal = () => {
  showFindIdModal.value = false
}

// 비밀번호 찾기
const findPassword = () => {
  showFindPasswordModal.value = true
}

const closeFindPasswordModal = () => {
  showFindPasswordModal.value = false
}

// 회원가입 페이지로 이동
const goToSignup = () => {
  router.push('/signup')
}

// 뒤로가기
const goBack = () => {
  // 브라우저 히스토리에서 이전 페이지로 이동
  // 히스토리가 없거나 외부 사이트에서 직접 접근한 경우 홈페이지로 이동
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7fafc;
  padding: 20px;
  position: relative;
}

.back-button {
  position: absolute;
  top: 30px;
  left: 30px;
  background: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.back-button:hover {
  transform: translateX(-2px);
}

.login-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  width: 100%;
  max-width: 400px;
  overflow: hidden;
}

.logo-section {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  padding: 40px 30px;
  text-align: center;
  color: white;
}

.logo h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.tagline {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.4;
}

.login-form {
  padding: 30px 30px 30px;
}

.login-form h2 {
  margin: 0 0 30px 0;
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
}

.input-group {
  margin-bottom: 20px;
}

.input-label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.input-field {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  background: #ffffff;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.password-input-wrapper {
  position: relative;
}

.password-field {
  padding-right: 50px;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #374151;
}

.login-options {
  margin-bottom: 30px;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox {
  margin-right: 8px;
  width: 16px;
  height: 16px;
  accent-color: #6366f1;
}

.checkbox-label {
  font-size: 14px;
  color: #6b7280;
}

/* 로그인 버튼은 공통 스타일 사용 */

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  margin-bottom: 20px;
}

.bottom-links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

/* 링크 버튼과 회원가입 버튼은 공통 스타일 사용 */

.divider {
  color: #d1d5db;
  font-size: 14px;
}

.signup-section {
  text-align: center;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.signup-section p {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #6b7280;
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }

  .back-button {
    top: 20px;
    left: 20px;
  }

  .login-card {
    max-width: none;
  }

  .logo-section {
    padding: 30px 20px;
  }

  .login-form {
    padding: 30px 20px 20px;
  }

  .bottom-links {
    flex-direction: column;
    gap: 8px;
  }

  .divider {
    display: none;
  }
}
</style>
