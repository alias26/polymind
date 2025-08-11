<template>
  <div class="signup-container">
    <!-- 뒤로가기 버튼 -->
    <button class="btn-base btn-icon back-button" @click="goBack">
      <i class="fas fa-arrow-left"></i>
      <span>뒤로가기</span>
    </button>
    
    <div class="signup-card">
      <!-- 로고 영역 -->
      <div class="logo-section">
        <div class="logo">
          <h1>PolyMind</h1>
          <p class="tagline">다양한 AI와 함께하는 지능형 대화 플랫폼</p>
        </div>
      </div>

      <!-- 회원가입 폼 -->
      <div class="signup-form">
        <h2>회원가입</h2>
        
        <form @submit.prevent="handleSignup">
          <!-- 사용자 ID 입력 -->
          <div class="input-group">
            <label for="userId" class="input-label">사용자 ID</label>
            <input
              id="userId"
              v-model="signupForm.id"
              type="text"
              class="input-field"
              :class="{ 'error': errors.id }"
              placeholder="사용자 ID를 입력하세요"
              required
              @blur="validateUserId"
            />
            <div v-if="errors.id" class="error-text">{{ errors.id }}</div>
          </div>

          <!-- 이름 입력 -->
          <div class="input-group">
            <label for="name" class="input-label">이름</label>
            <input
              id="name"
              v-model="signupForm.name"
              type="text"
              class="input-field"
              :class="{ 'error': errors.name }"
              placeholder="이름을 입력하세요"
              required
              @blur="validateName"
            />
            <div v-if="errors.name" class="error-text">{{ errors.name }}</div>
          </div>

          <!-- 이메일 입력 -->
          <div class="input-group">
            <label for="email" class="input-label">이메일</label>
            <div class="email-input-wrapper">
              <input
                id="email"
                v-model="signupForm.email"
                type="email"
                class="input-field"
                :class="{ 'error': errors.email, 'verified': emailVerified }"
                placeholder="이메일을 입력하세요"
                required
                @blur="validateEmail"
                :disabled="emailVerified"
              />
              <button
                type="button"
                class="verify-btn"
                @click="sendVerificationCode"
                :disabled="!isValidEmail || isVerificationSent || emailVerified"
              >
                {{ emailVerified ? '인증완료' : isVerificationSent ? '재전송' : '인증코드 전송' }}
              </button>
            </div>
            <div v-if="errors.email" class="error-text">{{ errors.email }}</div>
          </div>

          <!-- 이메일 인증 코드 -->
          <div class="input-group">
            <label for="verificationCode" class="input-label">인증 코드</label>
            <div class="verification-wrapper">
              <input
                id="verificationCode"
                v-model="signupForm.verificationCode"
                type="text"
                class="input-field"
                :class="{ 'error': errors.verificationCode }"
                placeholder="인증코드 전송 후 입력하세요"
                maxlength="6"
                :disabled="!isVerificationSent || emailVerified"
              />
              <button
                type="button"
                class="verify-code-btn"
                @click="verifyEmail"
                :disabled="signupForm.verificationCode.length !== 6 || emailVerified || !isVerificationSent"
              >
                인증하기
              </button>
            </div>
            <div v-if="errors.verificationCode" class="error-text">{{ errors.verificationCode }}</div>
            <div v-if="verificationTimer > 0" class="timer-text">
              남은 시간: {{ Math.floor(verificationTimer / 60) }}:{{ String(verificationTimer % 60).padStart(2, '0') }}
            </div>
          </div>

          <!-- 비밀번호 입력 -->
          <div class="input-group">
            <label for="password" class="input-label">비밀번호</label>
            <div class="password-input-wrapper">
              <input
                id="password"
                v-model="signupForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="input-field password-field"
                :class="{ 'error': errors.password }"
                placeholder="비밀번호를 입력하세요"
                required
                @blur="validatePassword"
              />
              <button
                type="button"
                class="password-toggle"
                @click="togglePassword"
              >
                <i :class="showPassword ? 'fas fa-eye' : 'fas fa-eye-slash'"></i>
              </button>
            </div>
            <div v-if="errors.password" class="error-text">{{ errors.password }}</div>
            <div class="password-requirements">
              <div class="requirement" :class="{ 'met': passwordRequirements.length }">
                <i class="fas fa-check"></i> 8자 이상
              </div>
              <div class="requirement" :class="{ 'met': passwordRequirements.uppercase }">
                <i class="fas fa-check"></i> 대문자 포함
              </div>
              <div class="requirement" :class="{ 'met': passwordRequirements.lowercase }">
                <i class="fas fa-check"></i> 소문자 포함
              </div>
              <div class="requirement" :class="{ 'met': passwordRequirements.number }">
                <i class="fas fa-check"></i> 숫자 포함
              </div>
              <div class="requirement" :class="{ 'met': passwordRequirements.special }">
                <i class="fas fa-check"></i> 특수문자 포함
              </div>
            </div>
          </div>

          <!-- 비밀번호 확인 -->
          <div class="input-group">
            <label for="confirmPassword" class="input-label">비밀번호 확인</label>
            <input
              id="confirmPassword"
              v-model="signupForm.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              class="input-field"
              :class="{ 'error': errors.confirmPassword }"
              placeholder="비밀번호를 다시 입력하세요"
              required
              @blur="validateConfirmPassword"
            />
            <div v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</div>
          </div>

          <!-- 회원가입 버튼 -->
          <button
            type="submit"
            class="signup-button"
            :disabled="!isFormValid || isLoading"
          >
            <span v-if="isLoading" class="loading-spinner"></span>
            {{ isLoading ? '회원가입 중...' : '회원가입' }}
          </button>

          <!-- 에러 메시지 -->
          <div v-if="errorMessage" class="error-message">
            <i class="fas fa-exclamation-triangle"></i>
            {{ errorMessage }}
          </div>
        </form>

        <!-- 로그인 링크 -->
        <div class="login-section">
          <p>이미 계정이 있으신가요?</p>
          <button class="btn-base btn-secondary" @click="goToLogin">
            로그인
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useLoadingStore } from '@/store/loading'
import { toastService } from '@/utils/toastService'

const router = useRouter()
const loadingStore = useLoadingStore()

// 폼 데이터
const signupForm = reactive({
  id: '',
  name: '',
  email: '',
  verificationCode: '',
  password: '',
  confirmPassword: ''
})

// 에러 상태
const errors = reactive({
  id: '',
  name: '',
  email: '',
  verificationCode: '',
  password: '',
  confirmPassword: ''
})

// 상태 관리
// 로딩 상태는 전역 스토어에서 가져옴
const isLoading = computed(() => loadingStore.isOperationLoading('signup'))
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const errorMessage = ref('')
const isVerificationSent = ref(false)
const emailVerified = ref(false)
const verificationTimer = ref(0)

// 비밀번호 표시/숨김 토글
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// 이메일 유효성 검사
const isValidEmail = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(signupForm.email)
})

// 비밀번호 요구사항 체크
const passwordRequirements = computed(() => {
  const password = signupForm.password
  return {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /[0-9]/.test(password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
  }
})

// 폼 유효성 검사
const isFormValid = computed(() => {
  return signupForm.id.trim() !== '' &&
         signupForm.name.trim() !== '' &&
         isValidEmail.value &&
         emailVerified.value &&
         Object.values(passwordRequirements.value).every(req => req) &&
         signupForm.password === signupForm.confirmPassword &&
         !Object.values(errors).some(error => error !== '')
})

// 사용자 ID 검증
const validateUserId = () => {
  if (signupForm.id.length < 3) {
    errors.id = '사용자 ID는 3자 이상이어야 합니다.'
  } else if (signupForm.id.length > 50) {
    errors.id = '사용자 ID는 50자 이하여야 합니다.'
  } else if (!/^[a-zA-Z0-9_]+$/.test(signupForm.id)) {
    errors.id = '사용자 ID는 영문, 숫자, 언더스코어(_)만 사용 가능합니다.'
  } else {
    errors.id = ''
  }
}

// 이름 검증
const validateName = () => {
  if (!signupForm.name || !signupForm.name.trim()) {
    errors.name = '이름을 입력해주세요.'
  } else if (signupForm.name.trim().length < 1) {
    errors.name = '이름은 최소 1자 이상이어야 합니다.'
  } else if (signupForm.name.trim().length > 100) {
    errors.name = '이름은 최대 100자까지 가능합니다.'
  } else if (!/^[가-힣a-zA-Z\s]+$/.test(signupForm.name.trim())) {
    errors.name = '이름은 한글, 영문, 공백만 사용 가능합니다.'
  } else {
    errors.name = ''
  }
}

// 이메일 검증
const validateEmail = () => {
  if (!isValidEmail.value) {
    errors.email = '올바른 이메일 형식을 입력해주세요.'
  } else {
    errors.email = ''
  }
}

// 비밀번호 검증
const validatePassword = () => {
  if (!Object.values(passwordRequirements.value).every(req => req)) {
    errors.password = '비밀번호 요구사항을 만족해야 합니다.'
  } else {
    errors.password = ''
  }
}

// 비밀번호 확인 검증
const validateConfirmPassword = () => {
  if (signupForm.password !== signupForm.confirmPassword) {
    errors.confirmPassword = '비밀번호가 일치하지 않습니다.'
  } else {
    errors.confirmPassword = ''
  }
}

// 인증 코드 전송
const sendVerificationCode = async () => {
  if (!isValidEmail.value) return
  
  try {
    // TODO: 실제 이메일 인증 API 연동
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    isVerificationSent.value = true
    verificationTimer.value = 300 // 5분
    startTimer()
    
    toastService.emailVerificationSent()
  } catch (error) {
    errorMessage.value = '인증 코드 전송에 실패했습니다.'
  }
}

// 이메일 인증
const verifyEmail = async () => {
  if (signupForm.verificationCode.length !== 6) return
  
  try {
    // TODO: 실제 이메일 인증 확인 API 연동
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 임시로 '123456'을 올바른 코드로 설정
    if (signupForm.verificationCode === '123456') {
      emailVerified.value = true
      verificationTimer.value = 0
      errors.verificationCode = ''
      toastService.emailVerificationComplete()
    } else {
      errors.verificationCode = '잘못된 인증 코드입니다.'
    }
  } catch (error) {
    errors.verificationCode = '인증 확인에 실패했습니다.'
  }
}

// 타이머 시작
const startTimer = () => {
  const interval = setInterval(() => {
    verificationTimer.value--
    if (verificationTimer.value <= 0) {
      clearInterval(interval)
      isVerificationSent.value = false
    }
  }, 1000)
}

// 회원가입 처리
const handleSignup = async () => {
  if (!isFormValid.value || isLoading.value) return
  
  errorMessage.value = ''
  loadingStore.startOperation('signup', '회원가입 중...')
  
  try {
    // 백엔드 회원가입 API 호출
    const { authApi } = await import('@/apis/authApi')
    const response = await authApi.register({
      id: signupForm.id,
      name: signupForm.name,
      email: signupForm.email,
      password: signupForm.password
    })
    
    toastService.signUpSuccess()
    router.push('/login')
  } catch (error) {
    console.error('회원가입 오류:', error)
    if (error.message.includes('409') || error.message.includes('already exists')) {
      errorMessage.value = '이미 존재하는 사용자 ID 또는 이메일입니다.'
    } else if (error.message.includes('400')) {
      errorMessage.value = '입력한 정보를 다시 확인해주세요.'
    } else if (error.message.includes('network') || error.message.includes('연결')) {
      errorMessage.value = '네트워크 연결을 확인해주세요.'
    } else {
      errorMessage.value = '회원가입에 실패했습니다. 다시 시도해주세요.'
    }
  } finally {
    loadingStore.stopOperation('signup')
  }
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

// 로그인 페이지로 이동
const goToLogin = () => {
  router.push('/login')
}

// 비밀번호 확인 실시간 검증
watch(() => signupForm.confirmPassword, () => {
  if (signupForm.confirmPassword) {
    validateConfirmPassword()
  }
})
</script>

<style scoped>
.signup-container {
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
  border: 1px solid #e2e8f0;
  color: #6b7280;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.back-button:hover {
  background: #f8fafc;
  border-color: #cbd5e0;
  color: #374151;
  transform: translateX(-2px);
}

.signup-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  width: 100%;
  max-width: 480px;
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

.signup-form {
  padding: 20px 30px 24px;
}

.signup-form h2 {
  margin: 0 0 20px 0;
  font-size: 22px;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
}

.input-group {
  margin-bottom: 14px;
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
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  background: #ffffff;
  transition: all 0.2s ease;
  box-sizing: border-box;
  height: 44px;
}

.input-field:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.input-field.error {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.input-field.verified {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.email-input-wrapper {
  display: flex;
  gap: 8px;
}

.email-input-wrapper .input-field {
  flex: 1;
}

.verify-btn {
  padding: 0 16px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  white-space: nowrap;
  min-width: 120px;
  height: 44px;
}

.verify-btn:hover:not(:disabled) {
  background: #4f46e5;
}

.verify-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.verification-wrapper {
  display: flex;
  gap: 8px;
}

.verification-wrapper .input-field {
  flex: 1;
}

.verify-code-btn {
  padding: 0 16px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  white-space: nowrap;
  min-width: 100px;
  height: 44px;
}

.verify-code-btn:hover:not(:disabled) {
  background: #059669;
}

.verify-code-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
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
  height: 28px;
  width: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.password-toggle:hover {
  color: #374151;
}

.error-text {
  margin-top: 6px;
  font-size: 14px;
  color: #dc2626;
}

.timer-text {
  margin-top: 6px;
  font-size: 14px;
  color: #6366f1;
  font-weight: 500;
}

.password-requirements {
  margin-top: 6px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.requirement {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #9ca3af;
  transition: color 0.2s ease;
  line-height: 1.2;
}

.requirement.met {
  color: #10b981;
}

.requirement i {
  width: 10px;
  height: 10px;
  font-size: 8px;
}

.signup-button {
  width: 100%;
  padding: 0 20px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
  height: 48px;
}

.signup-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
}

.signup-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

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
  margin-bottom: 20px;
}

.login-section {
  text-align: center;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-section p {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #6b7280;
}

.login-link {
  background: none;
  border: 1px solid #6366f1;
  color: #6366f1;
  padding: 0 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.login-link:hover {
  background: #6366f1;
  color: white;
}

/* 반응형 디자인 */
@media (max-width: 480px) {
  .signup-container {
    padding: 10px;
  }
  
  .back-button {
    top: 20px;
    left: 20px;
    padding: 8px 12px;
    font-size: 13px;
  }
  
  .signup-card {
    max-width: none;
  }
  
  .logo-section {
    padding: 30px 20px;
  }
  
  .signup-form {
    padding: 30px 20px 20px;
  }
  
  .email-input-wrapper,
  .verification-wrapper {
    flex-direction: column;
  }
  
  .verify-btn,
  .verify-code-btn {
    min-width: unset;
  }
  
  .password-requirements {
    gap: 8px;
  }
}
</style>