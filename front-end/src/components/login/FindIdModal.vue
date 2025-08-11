<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>아이디 찾기</h3>
        <button class="btn-base btn-icon modal-close" @click="closeModal">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="modal-body">
        <p class="modal-description">가입 시 등록한 이메일을 입력해주세요.</p>
        <div class="input-group">
          <label class="input-label">이메일</label>
          <input
            v-model="form.email"
            type="email"
            class="input-field"
            :class="{ 'error': errors.email }"
            placeholder="example@email.com"
            @blur="validateEmail"
          />
          <div v-if="errors.email" class="error-text">{{ errors.email }}</div>
        </div>
        <div v-if="result" class="success-message">
          <i class="fas fa-check-circle"></i>
          {{ result }}
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-base btn-secondary" @click="closeModal">
          취소
        </button>
        <button class="btn-base btn-primary" :class="{ 'btn-loading': isLoading }" @click="submitFindId" :disabled="!isValidForm || isLoading">
          {{ isLoading ? '찾는 중...' : '아이디 찾기' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const form = reactive({
  email: ''
})

const errors = reactive({
  email: ''
})

const isLoading = ref(false)
const result = ref('')

const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const isValidForm = computed(() => {
  return form.email.trim() !== '' && 
         isValidEmail(form.email) && 
         !errors.email
})

const validateEmail = () => {
  if (!form.email.trim()) {
    errors.email = '이메일을 입력해주세요.'
  } else if (!isValidEmail(form.email)) {
    errors.email = '올바른 이메일 형식을 입력해주세요.'
  } else {
    errors.email = ''
  }
}

const resetForm = () => {
  form.email = ''
  errors.email = ''
  result.value = ''
  isLoading.value = false
}

const closeModal = () => {
  resetForm()
  emit('close')
}

// Escape 키로 모달 닫기
const handleEscapeKey = (event) => {
  if (event.key === 'Escape' && props.show) {
    closeModal()
  }
}

const submitFindId = async () => {
  if (!isValidForm.value || isLoading.value) return
  
  isLoading.value = true
  result.value = ''
  
  try {
    const { authApi } = await import('@/apis/authApi')
    const response = await authApi.findUserId(form.email)
    
    if (response.found_ids && response.found_ids.length > 0) {
      const ids = response.found_ids.join(', ')
      result.value = `찾은 아이디: ${ids}\n\n※ 개발 환경에서는 콘솔도 확인해주세요.`
    } else {
      result.value = '해당 이메일로 등록된 아이디를 찾을 수 없습니다.'
    }
    
    // 5초 후 모달 닫기
    setTimeout(() => {
      closeModal()
    }, 5000)
  } catch (error) {
    errors.email = error.message || '아이디 찾기에 실패했습니다. 다시 시도해주세요.'
  } finally {
    isLoading.value = false
  }
}

watch(() => props.show, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})

// 키보드 이벤트 리스너 설정
onMounted(() => {
  document.addEventListener('keydown', handleEscapeKey)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscapeKey)
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  background: oklab(0 none none/.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
  padding: 20px;
}

.modal-content {
  background: #ffffff;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.modal-close {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 16px;
}

.modal-close:hover {
  color: #374151;
  background: #f3f4f6;
}

.modal-body {
  padding: 20px 24px;
}

.modal-description {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
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

.input-field.error {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.error-text {
  margin-top: 6px;
  font-size: 12px;
  color: #dc2626;
}

.success-message {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
}

.modal-footer {
  padding: 0 24px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.cancel-btn {
  background: #f3f4f6;
  color: #374151;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.confirm-btn {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
}

.confirm-btn:disabled {
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
</style>