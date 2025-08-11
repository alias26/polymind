<template>
  <div class="reset-password-container">

    <div class="reset-password-card">
      <!-- 로고 영역 -->
      <div class="logo-section">
        <div class="logo">
          <h1>PolyMind</h1>
          <p class="tagline">비밀번호 재설정</p>
        </div>
      </div>

      <!-- 재설정 폼 -->
      <div class="reset-form">
        <h2>새 비밀번호 설정</h2>
        <p class="form-description">새로운 비밀번호를 설정해주세요.</p>
        
        <!-- 토큰 에러 메시지 -->
        <div v-if="tokenError" class="token-error">
          <i class="fas fa-exclamation-triangle"></i>
          <div>
            <p>{{ tokenError }}</p>
            <button class="btn-base btn-secondary btn-small" @click="goToFindPassword">
              비밀번호 찾기
            </button>
          </div>
        </div>

        <form @submit.prevent="submitReset" v-if="!tokenError">
          <!-- 개발 환경에서 토큰 입력 -->
          <div class="input-group" v-if="!hasTokenInUrl">
            <label class="input-label">
              재설정 토큰 
              <span class="dev-label">(개발용)</span>
            </label>
            <input
              v-model="form.token"
              type="text"
              class="input-field"
              :class="{ 'error': errors.token }"
              placeholder="콘솔에서 복사한 토큰을 입력하세요"
            />
            <div v-if="errors.token" class="error-text">{{ errors.token }}</div>
            <div class="input-help">
              💡 비밀번호 찾기 후 콘솔에 출력된 토큰을 입력하세요.
            </div>
          </div>

          <!-- 새 비밀번호 입력 -->
          <div class="input-group">
            <label class="input-label">새 비밀번호</label>
            <input
              v-model="form.newPassword"
              type="password"
              class="input-field"
              :class="{ 'error': errors.newPassword }"
              placeholder="새 비밀번호를 입력하세요"
              @input="validatePassword"
            />
            <div v-if="errors.newPassword" class="error-text">{{ errors.newPassword }}</div>
          </div>

          <!-- 새 비밀번호 확인 -->
          <div class="input-group">
            <label class="input-label">새 비밀번호 확인</label>
            <input
              v-model="form.confirmPassword"
              type="password"
              class="input-field"
              :class="{ 'error': errors.confirmPassword }"
              placeholder="새 비밀번호를 다시 입력하세요"
              @input="validateConfirmPassword"
            />
            <div v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</div>
          </div>

          <!-- 비밀번호 요구사항 -->
          <div class="password-requirements" v-if="form.newPassword">
            <div class="requirements-header">비밀번호 요구사항</div>
            <div class="requirements-grid">
              <div class="requirement-item" :class="{ 'valid': hasMinLength }">
                <i class="fas fa-check"></i>
                <span>최소 8자</span>
              </div>
              <div class="requirement-item" :class="{ 'valid': hasLowerCase }">
                <i class="fas fa-check"></i>
                <span>소문자</span>
              </div>
              <div class="requirement-item" :class="{ 'valid': hasUpperCase }">
                <i class="fas fa-check"></i>
                <span>대문자</span>
              </div>
              <div class="requirement-item" :class="{ 'valid': hasNumber }">
                <i class="fas fa-check"></i>
                <span>숫자</span>
              </div>
              <div class="requirement-item" :class="{ 'valid': hasSpecialChar }">
                <i class="fas fa-check"></i>
                <span>특수문자</span>
              </div>
            </div>
          </div>

          <!-- 성공 메시지 -->
          <div v-if="successMessage" class="success-message">
            <i class="fas fa-check-circle"></i>
            {{ successMessage }}
          </div>

          <!-- 재설정 버튼 -->
          <div class="form-actions">
            <button 
              type="submit"
              class="btn-base btn-primary btn-full" 
              :class="{ 'btn-loading': isLoading }" 
              :disabled="!isValidForm || isLoading"
            >
              {{ isLoading ? '재설정 중...' : '비밀번호 재설정' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authApi } from '@/apis/authApi'

const route = useRoute()
const router = useRouter()

const form = reactive({
  token: '',
  newPassword: '',
  confirmPassword: ''
})

const errors = reactive({
  token: '',
  newPassword: '',
  confirmPassword: ''
})

const isLoading = ref(false)
const successMessage = ref('')
const hasTokenInUrl = ref(false)
const tokenError = ref('')

// 비밀번호 강도 체크
const hasMinLength = computed(() => form.newPassword.length >= 8)
const hasLowerCase = computed(() => /[a-z]/.test(form.newPassword))
const hasUpperCase = computed(() => /[A-Z]/.test(form.newPassword))
const hasNumber = computed(() => /\d/.test(form.newPassword))
const hasSpecialChar = computed(() => /[!@#$%^&*(),.?":{}|<>]/.test(form.newPassword))

const isPasswordValid = computed(() => {
  return hasMinLength.value && hasLowerCase.value && hasUpperCase.value && 
         hasNumber.value && hasSpecialChar.value
})

const isValidForm = computed(() => {
  return form.token.trim() && 
         isPasswordValid.value && 
         form.newPassword === form.confirmPassword &&
         !errors.token && !errors.newPassword && !errors.confirmPassword
})

const validatePassword = () => {
  if (!form.newPassword) {
    errors.newPassword = ''
    return
  }

  if (!isPasswordValid.value) {
    errors.newPassword = '비밀번호가 요구사항을 충족하지 않습니다.'
  } else {
    errors.newPassword = ''
  }
}

const validateConfirmPassword = () => {
  if (!form.confirmPassword) {
    errors.confirmPassword = ''
    return
  }

  if (form.newPassword !== form.confirmPassword) {
    errors.confirmPassword = '비밀번호가 일치하지 않습니다.'
  } else {
    errors.confirmPassword = ''
  }
}

const validateToken = () => {
  if (!form.token.trim()) {
    errors.token = '재설정 토큰을 입력해주세요.'
  } else {
    errors.token = ''
  }
}

const submitReset = async () => {
  validateToken()
  validatePassword()
  validateConfirmPassword()
  
  if (!isValidForm.value || isLoading.value) return
  
  isLoading.value = true
  successMessage.value = ''
  
  try {
    const response = await authApi.resetPassword(form.token, form.newPassword)
    successMessage.value = response.message
    
    // 2초 후 로그인 페이지로 자동 이동 (히스토리 교체)
    setTimeout(() => {
      router.replace('/login')
    }, 2000)
  } catch (error) {
    if (error.message.includes('토큰')) {
      errors.token = error.message
    } else {
      errors.newPassword = error.message || '비밀번호 재설정에 실패했습니다.'
    }
  } finally {
    isLoading.value = false
  }
}


// 비밀번호 찾기 페이지로 이동
const goToFindPassword = () => {
  router.replace('/login')
}

// 토큰 유효성 확인
const validateTokenOnMount = async () => {
  const urlToken = route.query.token
  if (urlToken) {
    form.token = urlToken
    hasTokenInUrl.value = true
    
    // 토큰이 이미 사용되었거나 만료되었는지 확인
    try {
      // 간단한 토큰 검증을 위해 실제 재설정 요청을 보내보지 않고
      // 토큰 형식만 확인 (UUID 형식인지)
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
      if (!uuidRegex.test(urlToken)) {
        tokenError.value = '유효하지 않은 토큰 형식입니다.'
        return
      }
    } catch (error) {
      console.error('토큰 검증 오류:', error)
    }
  } else {
    // URL에 토큰이 없으면 직접 접근으로 간주
    tokenError.value = '비밀번호 재설정 링크를 통해 접근해주세요.'
  }
}

onMounted(validateTokenOnMount)
</script>

<style scoped>
.reset-password-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7fafc;
  padding: 20px;
  position: relative;
}


.reset-password-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  width: 100%;
  max-width: 450px;
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

.reset-form {
  padding: 30px;
}

.reset-form h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
}

.form-description {
  text-align: center;
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 30px;
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

.dev-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 400;
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

.input-field.error {
  border-color: #ef4444;
}

.input-help {
  margin-top: 6px;
  font-size: 12px;
  color: #6b7280;
  background: #f9fafb;
  padding: 8px 12px;
  border-radius: 6px;
  border-left: 3px solid #6366f1;
}

.error-text {
  color: #ef4444;
  font-size: 13px;
  margin-top: 4px;
}

.password-requirements {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.requirements-header {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
}

.requirements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 8px;
}

.requirement-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
}

.requirement-item i {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 8px;
  color: #9ca3af;
}

.requirement-item.valid {
  color: #10b981;
}

.requirement-item.valid i {
  background: #10b981;
  color: white;
}

.success-message {
  background: #d1fae5;
  color: #065f46;
  padding: 12px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  font-size: 14px;
}

.token-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 16px;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
  text-align: left;
}

.token-error i {
  font-size: 18px;
  margin-top: 2px;
  flex-shrink: 0;
}

.token-error div {
  flex: 1;
}

.token-error p {
  margin: 0 0 12px 0;
  font-size: 14px;
  line-height: 1.5;
}

.btn-small {
  padding: 8px 16px;
  font-size: 14px;
}

.form-actions {
  margin-top: 30px;
}

.btn-base {
  padding: 14px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  text-align: center;
}

.btn-full {
  width: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

.btn-loading {
  position: relative;
  color: transparent;
}

.btn-loading:after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  top: 50%;
  left: 50%;
  margin-left: -10px;
  margin-top: -10px;
  border: 2px solid transparent;
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 1s ease infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 반응형 디자인 */
@media (max-width: 640px) {
  .reset-password-container {
    padding: 16px;
  }
  
  
  .reset-password-card {
    max-width: none;
  }
  
  .logo-section {
    padding: 32px 24px;
  }
  
  .reset-form {
    padding: 24px;
  }
  
  
  .requirements-grid {
    grid-template-columns: 1fr;
  }
}
</style>