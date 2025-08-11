<template>
  <div class="tab-content">
    <h2 class="tab-title">계정 설정</h2>
    <div class="account-settings">
      <!-- 기본 정보 섹션 -->
      <div class="setting-section">
        <h3 class="section-title">기본 정보</h3>
        <div class="setting-card">
          <div class="setting-item">
            <label class="setting-label">
              <span class="label-icon">👤</span>
              <span class="label-text">사용자 ID (변경 불가)</span>
            </label>
            <input 
              type="text" 
              v-model="userInfo.username" 
              class="setting-input readonly-input" 
              placeholder="사용자 ID" 
              readonly
              disabled
            />
          </div>
          <div class="setting-item">
            <label class="setting-label">
              <span class="label-icon">👤</span>
              <span class="label-text">이름</span>
            </label>
            <input 
              type="text" 
              v-model="userInfo.name" 
              class="setting-input" 
              :class="{ 'error': validationErrors.name }"
              placeholder="이름을 입력하세요" 
            />
            <div v-if="validationErrors.name" class="error-message">{{ validationErrors.name }}</div>
          </div>
          <div class="setting-item">
            <label class="setting-label">
              <span class="label-icon">✉️</span>
              <span class="label-text">이메일</span>
            </label>
            <input 
              type="email" 
              v-model="userInfo.email" 
              class="setting-input" 
              :class="{ 'error': validationErrors.email }"
              placeholder="이메일을 입력하세요" 
            />
            <div v-if="validationErrors.email" class="error-message">{{ validationErrors.email }}</div>
            <div v-if="serverErrors.emailExists" class="error-message server-error">
              이미 사용 중인 이메일입니다.
            </div>
          </div>
        </div>
      </div>
      
      <!-- 비밀번호 변경 섹션 -->
      <div class="setting-section">
        <h3 class="section-title">보안</h3>
        <div class="setting-card">
          <div class="setting-item">
            <label class="setting-label">
              <span class="label-icon">🔒</span>
              <span class="label-text">현재 비밀번호</span>
            </label>
            <input 
              type="password" 
              v-model="passwords.current" 
              class="setting-input" 
              :class="{ 'error': validationErrors.currentPassword || serverErrors.currentPasswordIncorrect }"
              placeholder="현재 비밀번호를 입력하세요"
              @blur="validateCurrentPassword" 
            />
            <div v-if="validationErrors.currentPassword" class="error-message">{{ validationErrors.currentPassword }}</div>
            <div v-if="serverErrors.currentPasswordIncorrect" class="error-message server-error">
              현재 비밀번호가 올바르지 않습니다.
            </div>
            <div v-if="serverErrors.currentPasswordCorrect" class="success-message">
              현재 비밀번호가 확인되었습니다.
            </div>
          </div>
          <div class="setting-item">
            <label class="setting-label">
              <span class="label-icon">🔑</span>
              <span class="label-text">새 비밀번호</span>
            </label>
            <input 
              type="password" 
              v-model="passwords.new" 
              class="setting-input" 
              :class="{ 'error': validationErrors.newPassword }"
              placeholder="새 비밀번호를 입력하세요" 
            />
            <div v-if="validationErrors.newPassword" class="error-message">{{ validationErrors.newPassword }}</div>
            <div v-if="passwords.new && !validationErrors.newPassword" class="password-requirements">
              <small>비밀번호 요구사항: 8자 이상, 대소문자, 숫자, 특수문자 포함</small>
            </div>
          </div>
          <div class="setting-item">
            <label class="setting-label">
              <span class="label-icon">✓</span>
              <span class="label-text">비밀번호 확인</span>
            </label>
            <input 
              type="password" 
              v-model="passwords.confirm" 
              class="setting-input" 
              :class="{ 'error': validationErrors.confirmPassword }"
              placeholder="새 비밀번호를 다시 입력하세요" 
            />
            <div v-if="validationErrors.confirmPassword" class="error-message">{{ validationErrors.confirmPassword }}</div>
          </div>
        </div>
      </div>
      
      <!-- 서버 메시지 표시 영역 -->
      <div v-if="serverErrors.general" class="server-message" 
           :class="{ 'success': serverErrors.general.includes('성공적으로'), 'error': !serverErrors.general.includes('성공적으로') }">
        {{ serverErrors.general }}
      </div>
      
      <!-- 액션 버튼 -->
      <div class="setting-actions">
        <button 
          class="btn-base btn-primary" 
          @click="saveAccountSettings"
          :disabled="!isFormValid || isLoading"
          :class="{ 'btn-loading': isLoading }"
        >
          <span>{{ isLoading ? '⏳' : '💾' }}</span>
          {{ isLoading ? '저장 중...' : hasAnyChanges ? '변경사항 저장' : '저장' }}
        </button>
        <button class="btn-base btn-secondary" @click="resetForm" :disabled="isLoading">
          <span>↺</span>
          취소
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'

const userInfo = ref({
  username: '', // 사용자 ID (읽기 전용)
  name: '',     // 사용자 이름
  email: ''     // 이메일
})

// 초기 사용자 정보 저장 (변경 사항 비교용)
const originalUserInfo = ref({
  username: '',
  name: '',
  email: ''
})

const passwords = ref({
  current: '',
  new: '',
  confirm: ''
})

// Validation 상태 관리
const validationErrors = ref({
  name: '',
  email: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 서버 에러 상태 관리
const serverErrors = ref({
  currentPasswordIncorrect: false,
  currentPasswordCorrect: false,
  emailExists: false,
  general: ''
})

const isLoading = ref(false)

// Validation 함수들
const validateName = (name) => {
  if (!name || !name.trim()) {
    return '이름은 필수 입력 항목입니다.'
  }
  if (name.trim().length < 1) {
    return '이름은 최소 1자 이상이어야 합니다.'
  }
  if (name.trim().length > 100) {
    return '이름은 최대 100자까지 가능합니다.'
  }
  if (!/^[가-힣a-zA-Z\s]+$/.test(name.trim())) {
    return '이름은 한글, 영문, 공백만 사용 가능합니다.'
  }
  return ''
}

const validateEmail = (email) => {
  if (!email || !email.trim()) {
    return '이메일은 필수 입력 항목입니다.'
  }
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!emailPattern.test(email)) {
    return '올바른 이메일 형식을 입력해주세요.'
  }
  return ''
}

const validatePassword = (password) => {
  if (!password) {
    return '비밀번호를 입력해주세요.'
  }
  if (password.length < 8) {
    return '비밀번호는 최소 8자 이상이어야 합니다.'
  }
  if (password.length > 128) {
    return '비밀번호는 최대 128자까지 가능합니다.'
  }
  if (!/[a-z]/.test(password)) {
    return '비밀번호에는 소문자가 포함되어야 합니다.'
  }
  if (!/[A-Z]/.test(password)) {
    return '비밀번호에는 대문자가 포함되어야 합니다.'
  }
  if (!/\d/.test(password)) {
    return '비밀번호에는 숫자가 포함되어야 합니다.'
  }
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    return '비밀번호에는 특수문자가 포함되어야 합니다.'
  }
  return ''
}

const validateConfirmPassword = (newPassword, confirmPassword) => {
  if (!confirmPassword) {
    return '비밀번호 확인을 입력해주세요.'
  }
  if (newPassword !== confirmPassword) {
    return '새 비밀번호가 일치하지 않습니다.'
  }
  return ''
}

// 실시간 validation
watch(() => userInfo.value.name, (newName) => {
  validationErrors.value.name = validateName(newName)
})

watch(() => userInfo.value.email, (newEmail) => {
  validationErrors.value.email = validateEmail(newEmail)
  // 이메일을 다시 입력하면 이메일 중복 서버 에러 초기화
  if (serverErrors.value.emailExists) {
    serverErrors.value.emailExists = false
  }
})

watch(() => passwords.value.current, (currentPassword) => {
  if (currentPassword) {
    validationErrors.value.currentPassword = currentPassword.trim() ? '' : '현재 비밀번호를 입력해주세요.'
    // 현재 비밀번호를 다시 입력하면 서버 에러 및 성공 상태 초기화
    if (serverErrors.value.currentPasswordIncorrect || serverErrors.value.currentPasswordCorrect) {
      serverErrors.value.currentPasswordIncorrect = false
      serverErrors.value.currentPasswordCorrect = false
    }
  } else {
    validationErrors.value.currentPassword = ''
    serverErrors.value.currentPasswordIncorrect = false
    serverErrors.value.currentPasswordCorrect = false
  }
})

watch(() => passwords.value.new, (newPassword) => {
  if (newPassword) {
    validationErrors.value.newPassword = validatePassword(newPassword)
    // 확인 비밀번호도 다시 검증
    if (passwords.value.confirm) {
      validationErrors.value.confirmPassword = validateConfirmPassword(newPassword, passwords.value.confirm)
    }
  } else {
    validationErrors.value.newPassword = ''
    validationErrors.value.confirmPassword = ''
  }
})

watch(() => passwords.value.confirm, (confirmPassword) => {
  if (passwords.value.new) {
    validationErrors.value.confirmPassword = validateConfirmPassword(passwords.value.new, confirmPassword)
  } else {
    validationErrors.value.confirmPassword = ''
  }
})

// 사용자 정보 변경 감지
const hasUserInfoChanges = computed(() => {
  return userInfo.value.name !== originalUserInfo.value.name ||
         userInfo.value.email !== originalUserInfo.value.email
})

// 비밀번호 변경 감지
const hasPasswordChanges = computed(() => {
  return passwords.value.current.trim() !== '' ||
         passwords.value.new.trim() !== '' ||
         passwords.value.confirm.trim() !== ''
})

// 전체 변경 사항 감지
const hasAnyChanges = computed(() => {
  return hasUserInfoChanges.value || hasPasswordChanges.value
})

// 폼 검증 상태
const isFormValid = computed(() => {
  // 변경 사항이 없으면 저장 불가
  if (!hasAnyChanges.value) {
    return false
  }

  const hasUserInfoErrors = validationErrors.value.name || validationErrors.value.email
  const hasPasswordErrors = validationErrors.value.currentPassword || validationErrors.value.newPassword || validationErrors.value.confirmPassword
  
  // 사용자 정보만 변경하는 경우
  if (hasUserInfoChanges.value && !hasPasswordChanges.value) {
    return !hasUserInfoErrors
  }
  
  // 비밀번호만 변경하는 경우
  if (!hasUserInfoChanges.value && hasPasswordChanges.value) {
    const passwordFieldsFilled = passwords.value.current && passwords.value.new && passwords.value.confirm
    return passwordFieldsFilled && !hasPasswordErrors
  }
  
  // 둘 다 변경하는 경우
  if (hasUserInfoChanges.value && hasPasswordChanges.value) {
    const passwordFieldsFilled = passwords.value.current && passwords.value.new && passwords.value.confirm
    return passwordFieldsFilled && !hasPasswordErrors && !hasUserInfoErrors
  }
  
  return false
})

const saveAccountSettings = async () => {
  if (!isFormValid.value || isLoading.value) {
    return
  }

  // 에러 상태 초기화
  serverErrors.value = {
    currentPasswordIncorrect: false,
    currentPasswordCorrect: false,
    emailExists: false,
    general: ''
  }

  isLoading.value = true

  try {

    // 클라이언트 사이드 검증
    const nameError = validateName(userInfo.value.name)
    const emailError = validateEmail(userInfo.value.email)
    
    if (nameError || emailError) {
      validationErrors.value.name = nameError
      validationErrors.value.email = emailError
      return
    }

    // 비밀번호 변경이 있는 경우 추가 검증
    if (passwords.value.current || passwords.value.new || passwords.value.confirm) {
      if (!passwords.value.current) {
        validationErrors.value.currentPassword = '현재 비밀번호를 입력해주세요.'
        return
      }
      
      const newPasswordError = validatePassword(passwords.value.new)
      const confirmPasswordError = validateConfirmPassword(passwords.value.new, passwords.value.confirm)
      
      if (newPasswordError || confirmPasswordError) {
        validationErrors.value.newPassword = newPasswordError
        validationErrors.value.confirmPassword = confirmPasswordError
        return
      }
    }

    const { authApi } = await import('@/apis/authApi')

    // 사용자 정보 변경이 있는 경우에만 업데이트
    if (hasUserInfoChanges.value) {
      try {
        const updatedUser = await authApi.updateUserInfo({
          email: userInfo.value.email,
          name: userInfo.value.name
        })
        
        // 성공시 원본 데이터 업데이트
        originalUserInfo.value.email = userInfo.value.email
        originalUserInfo.value.name = userInfo.value.name
      } catch (userUpdateError) {
        if (userUpdateError.message.includes('Email already exists') || 
            userUpdateError.message.includes('이미 존재하는')) {
          serverErrors.value.emailExists = true
          return
        }
        throw userUpdateError
      }
    }

    // 비밀번호 변경이 있는 경우에만 처리
    if (hasPasswordChanges.value && passwords.value.current && passwords.value.new) {
      try {
        await authApi.changePassword({
          current_password: passwords.value.current,
          new_password: passwords.value.new
        })
        
        // 비밀번호 폼 초기화
        resetForm()
      } catch (passwordError) {
        if (passwordError.message.includes('Current password is incorrect') ||
            passwordError.message.includes('현재 비밀번호')) {
          serverErrors.value.currentPasswordIncorrect = true
          return
        }
        throw passwordError
      }
    }

    // 성공 메시지를 서버 에러 영역에 표시
    serverErrors.value.general = '계정 설정이 성공적으로 저장되었습니다.'
    
    // 3초 후 성공 메시지 숨기기
    setTimeout(() => {
      if (serverErrors.value.general.includes('성공적으로')) {
        serverErrors.value.general = ''
      }
    }, 3000)

  } catch (error) {
    console.error('계정 설정 저장 실패:', error)
    
    // 일반적인 서버 에러 처리
    let errorMessage = error.message
    if (error.message.includes('detail')) {
      try {
        const detail = JSON.parse(error.message.split('detail: ')[1])
        errorMessage = detail
      } catch (e) {
        // JSON 파싱 실패 시 원본 메시지 사용
      }
    }
    
    serverErrors.value.general = `설정 저장에 실패했습니다: ${errorMessage}`
  } finally {
    isLoading.value = false
  }
}

// 현재 비밀번호 검증
const validateCurrentPassword = async () => {
  if (!passwords.value.current || !passwords.value.current.trim()) {
    return
  }

  try {
    const { authApi } = await import('@/apis/authApi')
    await authApi.verifyCurrentPassword(passwords.value.current)
    
    // 비밀번호가 맞으면 에러 상태 초기화하고 성공 표시
    serverErrors.value.currentPasswordIncorrect = false
    serverErrors.value.currentPasswordCorrect = true
    validationErrors.value.currentPassword = ''
    
  } catch (error) {
    console.error('현재 비밀번호 검증 실패:', error)
    
    if (error.message.includes('Current password is incorrect') ||
        error.message.includes('현재 비밀번호')) {
      serverErrors.value.currentPasswordIncorrect = true
      serverErrors.value.currentPasswordCorrect = false
    } else {
      // 네트워크 오류 등 다른 에러는 무시 (사용자 경험을 위해)
      console.warn('현재 비밀번호 검증 중 네트워크 오류 발생:', error.message)
    }
  }
}

const resetForm = () => {
  // 사용자 정보를 원본으로 복원
  userInfo.value = {
    username: originalUserInfo.value.username,
    email: originalUserInfo.value.email,
    name: originalUserInfo.value.name
  }
  
  // 비밀번호 필드 초기화
  passwords.value = {
    current: '',
    new: '',
    confirm: ''
  }
  
  // 에러 상태 초기화
  validationErrors.value = {
    name: '',
    email: '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  
  serverErrors.value = {
    currentPasswordIncorrect: false,
    currentPasswordCorrect: false,
    emailExists: false,
    general: ''
  }
}

onMounted(async () => {
  try {
    const { authApi } = await import('@/apis/authApi')
    const userResponse = await authApi.getUserInfo()
    
    userInfo.value = {
      username: userResponse.id, // 사용자 ID (읽기 전용)
      email: userResponse.email,
      name: userResponse.name
    }
    
    // 원본 데이터도 동일하게 설정
    originalUserInfo.value = {
      username: userResponse.id,
      email: userResponse.email,
      name: userResponse.name
    }
    
  } catch (error) {
    console.error('사용자 정보 로드 실패:', error)
    
    // 로그인이 안 된 경우 로그인 페이지로 리다이렉트
    if (error.message.includes('인증')) {
      serverErrors.value.general = '로그인이 필요합니다. 로그인 페이지로 이동합니다.'
      setTimeout(() => {
        window.location.href = '/login'
      }, 2000)
    } else {
      serverErrors.value.general = `사용자 정보 로드에 실패했습니다: ${error.message}`
    }
  }
})
</script>

<style scoped>
.tab-content {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.tab-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 2rem;
  line-height: 1.5;
  text-align: left;
}

.account-settings {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 100%;
  max-width: none;
}

.setting-section {
  margin-bottom: 1rem;
  width: 100%;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  line-height: 1.5;
  text-align: left;
}

.setting-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  width: 100%;
  box-sizing: border-box;
}


.setting-item {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  width: 100%;
  align-items: stretch;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  line-height: 1.4;
  text-align: left;
}

.label-icon {
  font-size: 1rem;
  width: 20px;
  text-align: center;
}

.label-text {
  flex: 1;
}

.setting-input {
  padding: 0.875rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  background: #ffffff;
  transition: all 0.2s ease;
  font-family: inherit;
}

.setting-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  background: #fefefe;
}

.setting-input::placeholder {
  color: #9ca3af;
}

.readonly-input {
  background: #e5e7eb !important;
  color: #374151 !important;
  font-weight: 600 !important;
  cursor: not-allowed !important;
  border-color: #9ca3af !important;
}

.readonly-input:focus {
  border-color: #d1d5db !important;
  box-shadow: none !important;
}


.setting-actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.save-btn {
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.save-btn.loading {
  opacity: 0.8;
}

.save-btn.has-changes:not(:disabled) {
  background: linear-gradient(135deg, #059669, #047857);
  box-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
}

.save-btn.has-changes:hover:not(:disabled) {
  box-shadow: 0 4px 8px rgba(5, 150, 105, 0.3);
}

.save-btn:active {
  transform: translateY(0);
}

.cancel-btn {
  padding: 0.875rem 1.5rem;
  background: #f3f4f6;
  color: #6b7280;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cancel-btn:hover {
  background: #e5e7eb;
  color: #4b5563;
  border-color: #9ca3af;
  transform: translateY(-1px);
}

.cancel-btn:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 0.875rem;
}

/* Validation 스타일 */
.setting-input.error {
  border-color: #ef4444;
  background-color: #fef2f2;
}

.setting-input.error:focus {
  outline: none;
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.error-message {
  margin-top: 6px;
  font-size: 12px;
  color: #dc2626;
  display: flex;
  align-items: center;
  gap: 4px;
}

.error-message::before {
  content: '⚠️';
  font-size: 10px;
}

.password-requirements {
  margin-top: 6px;
  color: #6b7280;
  font-size: 11px;
  line-height: 1.4;
}

.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 서버 에러 스타일 */
.server-error {
  color: #dc2626 !important;
}

.server-message {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.server-message.success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #16a34a;
}

.server-message.success::before {
  content: '✅';
}

.server-message.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
}

.server-message.error::before {
  content: '❌';
}

/* 성공 메시지 스타일 */
.success-message {
  margin-top: 6px;
  font-size: 12px;
  color: #16a34a;
  display: flex;
  align-items: center;
  gap: 4px;
}

.success-message::before {
  content: '✅';
  font-size: 10px;
}
</style>