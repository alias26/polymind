<template>
  <div v-if="isVisible" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>새 채팅 만들기</h3>
        <button class="btn-base btn-icon modal-close" @click="closeModal">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="createChat">
          <!-- 채팅명 -->
          <div class="form-group">
            <label class="form-label">채팅명</label>
            <input
              v-model="chatTitle"
              type="text"
              class="form-input"
              placeholder="새 채팅"
              maxlength="50"
            />
          </div>

          <!-- API 선택 -->
          <div class="form-group">
            <label class="form-label">API</label>
            <select v-model="selectedApi" class="form-select" @change="onApiChange">
              <option 
                v-for="api in availableApis" 
                :key="api.key" 
                :value="api.key"
              >
                {{ api.name }}
              </option>
            </select>
          </div>

          <!-- 모델 선택 -->
          <div class="form-group">
            <label class="form-label">모델</label>
            <select v-model="selectedModel" class="form-select">
              <option 
                v-for="model in availableModels" 
                :key="model.key" 
                :value="model.key"
              >
                {{ model.name }}
              </option>
            </select>
          </div>

          <!-- Temperature -->
          <div class="form-group">
            <label class="form-label">Temperature</label>
            <div class="slider-container">
              <input
                v-model="temperature"
                type="range"
                :min="currentModelSettings?.temperature.min || 0"
                :max="currentModelSettings?.temperature.max || 1"
                :step="currentModelSettings?.temperature.step || 0.1"
                class="form-slider"
              />
              <span class="slider-value">{{ temperature }}</span>
            </div>
            <p class="form-hint">
              창의성 조절 ({{ currentModelSettings?.temperature.min || 0 }}: 일관성, {{ currentModelSettings?.temperature.max || 1 }}: 창의성)
            </p>
          </div>

          <!-- 최대 토큰 수 -->
          <div class="form-group">
            <label class="form-label">최대 토큰 수</label>
            <input
              v-model="maxTokens"
              type="number"
              :min="currentModelSettings?.maxTokens.min || 1"
              :max="currentModelSettings?.maxTokens.max || 8192"
              class="form-input"
              placeholder="2048"
            />
            <p class="form-hint">
              응답의 최대 길이 제한 ({{ currentModelSettings?.maxTokens.min || 1 }}-{{ currentModelSettings?.maxTokens.max || 8192 }})
            </p>
          </div>

        </form>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn-base btn-secondary" @click="closeModal">
          취소
        </button>
        <button type="button" class="btn-base btn-primary" :class="{ 'btn-loading': isCreating }" @click="createChat" :disabled="isCreating">
          <span>{{ isCreating ? '⏳' : '✨' }}</span>
          {{ isCreating ? '생성 중...' : '채팅 만들기' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useLoadingStore } from '@/store/loading'
import { getApiList, getModelList, getModelSettings, DEFAULT_SETTINGS } from '@/config/modelSettings'
import { getAllDefaultSettings, getAllDefaultSettingsAsync, getDefaultSystemPrompt } from '@/utils/profileSettings'

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'create'])

// 프로필 기본 설정 로드
const profileDefaults = getAllDefaultSettings()

// 폼 데이터
const chatTitle = ref('새 채팅')
const selectedApi = ref(profileDefaults.selectedApi)
const selectedModel = ref(profileDefaults.selectedModel)
const temperature = ref(profileDefaults.temperature)
const maxTokens = ref(profileDefaults.maxTokens)

// 생성 상태
// 채팅 생성 로딩 상태는 전역 스토어에서 가져옴
const loadingStore = useLoadingStore()
const isCreating = computed(() => loadingStore.isOperationLoading('new-chat-create'))

// 사용 가능한 API 목록
const availableApis = computed(() => getApiList())

// 선택된 API의 모델 목록
const availableModels = computed(() => {
  return getModelList(selectedApi.value)
})

// 현재 모델의 설정 범위
const currentModelSettings = computed(() => {
  return getModelSettings(selectedApi.value, selectedModel.value)
})

// API 변경 시 첫 번째 모델로 자동 선택
const onApiChange = () => {
  const models = getModelList(selectedApi.value)
  if (models.length > 0) {
    selectedModel.value = models[0].key
  }
  
  // 모델 설정에 맞게 기본값 조정
  const modelSettings = getModelSettings(selectedApi.value, selectedModel.value)
  if (modelSettings) {
    temperature.value = modelSettings.temperature.default || DEFAULT_SETTINGS.temperature
    maxTokens.value = modelSettings.maxTokens.default || DEFAULT_SETTINGS.maxTokens
  }
}

// 모델 변경 시 기본값 조정
watch(selectedModel, () => {
  const modelSettings = getModelSettings(selectedApi.value, selectedModel.value)
  if (modelSettings) {
    temperature.value = modelSettings.temperature.default || DEFAULT_SETTINGS.temperature
    maxTokens.value = modelSettings.maxTokens.default || DEFAULT_SETTINGS.maxTokens
  }
})

// 폼을 프로필 기본값으로 초기화
const resetFormToDefaults = async () => {
  
  try {
    // 서버에서 프로필에 저장한 기본 설정을 매번 새로 로드 (실시간 반영)
    const defaultSettings = await getAllDefaultSettingsAsync()
    
    chatTitle.value = '새 채팅'
    selectedApi.value = defaultSettings.selectedApi
    selectedModel.value = defaultSettings.selectedModel
    temperature.value = defaultSettings.temperature
    maxTokens.value = defaultSettings.maxTokens
    
    // 선택된 모델이 해당 API에 있는지 확인
    const availableModelsForApi = getModelList(selectedApi.value)
    const modelExists = availableModelsForApi.some(model => model.key === selectedModel.value)
    
    if (!modelExists && availableModelsForApi.length > 0) {
      // 모델이 존재하지 않으면 첫 번째 모델로 설정
      selectedModel.value = availableModelsForApi[0].key
      
      // 변경된 모델의 기본값 적용
      const modelSettings = getModelSettings(selectedApi.value, selectedModel.value)
      if (modelSettings) {
        temperature.value = modelSettings.temperature.default || defaultSettings.temperature
        maxTokens.value = modelSettings.maxTokens.default || defaultSettings.maxTokens
      }
    }
  } catch (error) {
    console.error('프로필 기본 설정 로드 실패:', error)
    // 오류 시 로컬 설정 사용
    const defaultSettings = getAllDefaultSettings()
    chatTitle.value = '새 채팅'
    selectedApi.value = defaultSettings.selectedApi
    selectedModel.value = defaultSettings.selectedModel
    temperature.value = defaultSettings.temperature
    maxTokens.value = defaultSettings.maxTokens
  }
}

// 모달 닫기
const closeModal = () => {
  emit('close')
}

// Escape 키로 모달 닫기
const handleEscapeKey = (event) => {
  if (event.key === 'Escape' && props.isVisible) {
    closeModal()
  }
}

// 채팅 생성
const createChat = () => {
  // 중복 생성 방지
  if (isCreating.value) return
  
  loadingStore.startOperation('new-chat-create', '새 채팅 생성 중...')
  
  try {
    const chatSettings = {
      title: chatTitle.value || '새 채팅',
      apiKey: selectedApi.value,
      selectedModel: selectedModel.value,
      temperature: parseFloat(temperature.value),
      maxTokens: parseInt(maxTokens.value),
      systemPrompt: getDefaultSystemPrompt() // 프로필의 기본 프롬프트 탭에서 가져오기
    }
    
    
    emit('create', chatSettings)
    
    // 폼 초기화
    resetFormToDefaults()
  } finally {
    // 생성 완료 후 상태 초기화
    setTimeout(() => {
      loadingStore.stopOperation('new-chat-create')
    }, 500)
  }
}

// 컴포넌트 마운트 시 초기 모델 설정
onMounted(() => {
  resetFormToDefaults()
  document.addEventListener('keydown', handleEscapeKey)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscapeKey)
})

// 모달이 열릴 때 초기화
watch(() => props.isVisible, async (newVal) => {
  if (newVal) {
    // 모달이 열릴 때마다 폼을 기본값으로 초기화
    await resetFormToDefaults()
    loadingStore.stopOperation('new-chat-create') // 생성 상태 초기화
  } else {
    loadingStore.stopOperation('new-chat-create') // 모달이 닫힐 때도 초기화
  }
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
}

.modal-content {
  background: #ffffff;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  padding: 24px 24px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
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
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.form-input, .form-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  background: #ffffff;
  transition: all 0.2s ease;
  box-sizing: border-box;
  font-family: inherit;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 16px;
}

.form-slider {
  flex: 1;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  outline: none;
  appearance: none;
  cursor: pointer;
}

.form-slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  background: #6366f1;
  border-radius: 50%;
  cursor: pointer;
}

.form-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #6366f1;
  border-radius: 50%;
  cursor: pointer;
  border: none;
}

.slider-value {
  font-size: 14px;
  font-weight: 600;
  color: #6366f1;
  min-width: 40px;
  text-align: center;
}

.form-hint {
  margin-top: 6px;
  font-size: 12px;
  color: #6b7280;
  line-height: 1.4;
}

.modal-footer {
  padding: 0 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.cancel-btn {
  background: #f3f4f6;
  color: #374151;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.create-btn {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
}

.create-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
}

.create-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 16px;
}
</style>