<template>
  <div class="tab-content">
    <h2 class="tab-title">기본 프리셋</h2>
    <p class="tab-subtitle">
      새 채팅 생성시 기본값으로 사용될 AI 모델 설정입니다
    </p>
    <div class="setting-section">
      <div class="setting-card">
        <div class="preset-settings">
          <div class="setting-item">
            <label>API 제공자</label>
            <select
              v-model="presetSettings.selectedApi"
              class="setting-select"
              @change="onApiChange"
            >
              <option v-for="api in availableApis" :key="api.value" :value="api.value">
                {{ api.label }}
              </option>
            </select>
            <small class="setting-hint"
              >사용할 AI 서비스를 선택하세요.</small
            >
          </div>

          <div class="setting-item">
            <label>모델</label>
            <select
              v-model="presetSettings.selectedModel"
              class="setting-select"
              @change="onModelChange"
            >
              <option v-for="model in availableModels" :key="model.value" :value="model.value">
                {{ model.label }}
              </option>
            </select>
            <small class="setting-hint"
              >사용할 AI 모델을 선택하세요.</small
            >
          </div>

          <div class="setting-item">
            <label>온도 (Temperature)</label>
            <div class="slider-container">
              <input
                type="range"
                :min="currentModelSettings.temperature.min"
                :max="currentModelSettings.temperature.max"
                :step="currentModelSettings.temperature.step"
                v-model.number="presetSettings.temperature"
                class="setting-slider"
                :key="`slider-${presetSettings.selectedApi}-${presetSettings.selectedModel}`"
              />
              <span class="slider-value">{{ Number(presetSettings.temperature).toFixed(1) }}</span>
            </div>
            <small class="setting-hint"
              >응답의 창의성을 조절합니다. (범위: {{ currentModelSettings.temperature.min }} - {{ currentModelSettings.temperature.max }})</small
            >
          </div>

          <div class="setting-item">
            <label>최대 토큰 수</label>
            <input
              type="number"
              :min="currentModelSettings.maxTokens.min"
              :max="currentModelSettings.maxTokens.max"
              v-model.number="presetSettings.maxTokens"
              class="setting-input"
            />
            <small class="setting-hint"
              >응답의 최대 길이를 설정합니다. (범위: {{ currentModelSettings.maxTokens.min }} - {{ currentModelSettings.maxTokens.max?.toLocaleString() || currentModelSettings.maxTokens.max }})</small
            >
          </div>
        </div>
      </div>
    </div>

    <div class="setting-actions">
      <button 
        class="btn-base btn-primary" 
        :disabled="!hasChanges"
        @click="savePresetSettings"
      >
        <span>💾</span>
        기본 프리셋 저장
      </button>
      <button class="btn-base btn-secondary" @click="resetToDefaults">
        <span>↺</span>
        초기값 복원
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { toastService } from '@/utils/toastService'
import { userPreferencesApi } from '@/apis/userPreferencesApi'
import { DEFAULT_SETTINGS, getApiList, getModelList, getModelSettings } from '@/config/modelSettings'

const presetSettings = ref({
  selectedApi: 'anthropic',
  selectedModel: 'Sonnet4',
  temperature: 0.7,
  maxTokens: 2048
})

// 원본 설정값 저장 (변경사항 감지용)
const originalSettings = ref({})

// 설정값이 변경되었는지 확인
const hasChanges = computed(() => {
  return JSON.stringify(presetSettings.value) !== JSON.stringify(originalSettings.value)
})

// API 목록
const availableApis = computed(() => {
  return getApiList().map(api => ({
    value: api.key,
    label: api.name
  }))
})

// 선택된 API에 따른 사용 가능한 모델들
const availableModels = computed(() => {
  return getModelList(presetSettings.value.selectedApi).map(model => ({
    value: model.key,
    label: model.name
  }))
})

// 현재 선택된 모델의 설정 범위
const currentModelSettings = computed(() => {
  return getModelSettings(presetSettings.value.selectedApi, presetSettings.value.selectedModel)
})

// 로딩 상태 추가 (서버에서 로드 중일 때는 자동 업데이트 방지)
const isLoadingFromServer = ref(false)

// API 변경 시 첫 번째 모델로 자동 선택
const onApiChange = async () => {
  // 서버에서 로드 중일 때는 자동 업데이트하지 않음
  if (isLoadingFromServer.value) return
  
  const models = availableModels.value
  if (models.length > 0) {
    presetSettings.value.selectedModel = models[0].value
    await updateSettingsForModel()
  }
}

// 모델 변경 시 설정값 업데이트
const onModelChange = async () => {
  // 서버에서 로드 중일 때는 자동 업데이트하지 않음
  if (isLoadingFromServer.value) return
  
  await updateSettingsForModel()
}

// 모델에 맞게 설정값 업데이트
const updateSettingsForModel = async () => {
  const modelSettings = currentModelSettings.value
  
  // 현재 설정값이 새 모델의 범위를 벗어나면 기본값으로 설정
  if (presetSettings.value.temperature < modelSettings.temperature.min || 
      presetSettings.value.temperature > modelSettings.temperature.max) {
    presetSettings.value.temperature = modelSettings.temperature.default
  }
  
  if (presetSettings.value.maxTokens < modelSettings.maxTokens.min || 
      presetSettings.value.maxTokens > modelSettings.maxTokens.max) {
    presetSettings.value.maxTokens = modelSettings.maxTokens.default
  }
  
  // Vue의 반응성을 위해 강제로 값 업데이트 트리거
  presetSettings.value = { ...presetSettings.value }
  
  // DOM 업데이트를 위해 nextTick 사용
  await nextTick()
}

const savePresetSettings = async () => {
  try {
    
    const serverData = {
      default_api: presetSettings.value.selectedApi,
      default_model: presetSettings.value.selectedModel,
      default_temperature: presetSettings.value.temperature,
      default_max_tokens: presetSettings.value.maxTokens
    }
    
    
    // 서버에 프리셋 설정 저장
    const response = await userPreferencesApi.updateUserPreferences(serverData)
    
    // 로컬 스토리지에도 백업 저장
    localStorage.setItem('defaultPresetSettings', JSON.stringify(presetSettings.value))
    
    // 원본 설정값 업데이트 (변경사항 없음으로 설정)
    originalSettings.value = { ...presetSettings.value }
    
    toastService.presetSaved()
  } catch (error) {
    console.error('프리셋 설정 저장 오류:', error)
    toastService.presetError()
  }
}

const resetToDefaults = () => {
  if (confirm('프리셋 설정을 초기값으로 복원하시겠습니까?')) {
    presetSettings.value = {
      selectedApi: 'anthropic',
      selectedModel: 'Sonnet4',
      temperature: DEFAULT_SETTINGS.temperature,
      maxTokens: DEFAULT_SETTINGS.maxTokens
    }
    // 원본 설정값도 동일하게 설정
    originalSettings.value = { ...presetSettings.value }
    toastService.presetRestored()
  }
}

const loadServerPresetSettings = async () => {
  try {
    isLoadingFromServer.value = true // 로딩 시작
    
    // 서버에서 프리셋 설정 로드
    const serverPreferences = await userPreferencesApi.getUserPreferences()
    
    if (serverPreferences && (serverPreferences.default_api || serverPreferences.default_model)) {
      // 서버에 프리셋 설정이 있는 경우
      presetSettings.value = {
        selectedApi: serverPreferences.default_api || 'anthropic',
        selectedModel: serverPreferences.default_model || 'Sonnet4',
        temperature: serverPreferences.default_temperature || DEFAULT_SETTINGS.temperature,
        maxTokens: serverPreferences.default_max_tokens || DEFAULT_SETTINGS.maxTokens
      }
      // 원본 설정값도 동일하게 설정
      originalSettings.value = { ...presetSettings.value }
    } else {
      // 서버에 프리셋 설정이 없으면 로컬에서 로드 시도
      loadLocalPresetSettings()
    }
  } catch (error) {
    console.error('서버에서 프리셋 설정 로드 오류:', error)
    // 서버 로드 실패 시 로컬 스토리지에서 로드 시도
    loadLocalPresetSettings()
  } finally {
    isLoadingFromServer.value = false // 로딩 완료
  }
}

const loadLocalPresetSettings = () => {
  // 로컬 스토리지에서 프리셋 설정 로드 (백업용)
  const savedSettings = localStorage.getItem('defaultPresetSettings')
  if (savedSettings) {
    try {
      const parsed = JSON.parse(savedSettings)
      presetSettings.value = {
        selectedApi: parsed.selectedApi || 'anthropic',
        selectedModel: parsed.selectedModel || 'Sonnet4',
        temperature: parsed.temperature || DEFAULT_SETTINGS.temperature,
        maxTokens: parsed.maxTokens || DEFAULT_SETTINGS.maxTokens
      }
      // 원본 설정값도 동일하게 설정
      originalSettings.value = { ...presetSettings.value }
    } catch (error) {
      console.error('로컬 프리셋 설정 로드 오류:', error)
      // 오류 시 기본값으로 설정
      const defaultSettings = {
        selectedApi: 'anthropic',
        selectedModel: 'Sonnet4',
        temperature: DEFAULT_SETTINGS.temperature,
        maxTokens: DEFAULT_SETTINGS.maxTokens
      }
      presetSettings.value = defaultSettings
      originalSettings.value = { ...defaultSettings }
    }
  } else {
    // 저장된 설정이 없으면 기본값으로 설정
    const defaultSettings = {
      selectedApi: 'anthropic',
      selectedModel: 'Sonnet4',
      temperature: DEFAULT_SETTINGS.temperature,
      maxTokens: DEFAULT_SETTINGS.maxTokens
    }
    presetSettings.value = defaultSettings
    originalSettings.value = { ...defaultSettings }
  }
}

onMounted(() => {
  // 서버에서 프리셋 설정 로드 시도
  loadServerPresetSettings()
})
</script>

<style scoped>
.tab-content {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tab-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
  line-height: 1.5;
  text-align: left;
}

.tab-subtitle {
  font-size: 1.125rem;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 2rem;
  line-height: 1.5;
  text-align: left;
  font-family: inherit;
}

.setting-section {
  margin-bottom: 2rem;
  width: 100%;
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

.preset-settings {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  width: 100%;
  align-items: stretch;
  overflow: hidden;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-item label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
  line-height: 1.4;
  text-align: left;
}

.setting-hint {
  color: #6b7280;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  line-height: 1.3;
  text-align: left;
}

.setting-select {
  padding: 0.875rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  font-family: inherit;
  background: #ffffff;
  transition: all 0.2s ease;
}

.setting-select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  background: #fefefe;
}

.setting-input {
  padding: 0.875rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  font-family: inherit;
  background: #ffffff;
  transition: all 0.2s ease;
  width: 100%;
  box-sizing: border-box;
  max-width: 100%;
}

.setting-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  background: #fefefe;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.setting-slider {
  flex: 1;
  height: 6px;
  border-radius: 3px;
  background: #e2e8f0;
  outline: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  margin: 0;
  transition: all 0.2s ease;
  cursor: pointer;
}

.setting-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #6366f1;
  cursor: pointer;
  transition: all 0.2s ease;
}

.setting-slider::-webkit-slider-thumb:hover {
  background: #4f46e5;
  transform: scale(1.1);
}

.setting-slider::-moz-range-track {
  height: 6px;
  border-radius: 3px;
  background: #e2e8f0;
  border: none;
}

.setting-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #6366f1;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  -moz-appearance: none;
}

.setting-slider::-moz-range-thumb:hover {
  background: #4f46e5;
  transform: scale(1.1);
}

.slider-value {
  min-width: 2.5rem;
  text-align: center;
  font-weight: 500;
  color: #374151;
  background: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.setting-actions {
  margin-top: 2rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

@media (max-width: 768px) {
  .setting-actions {
    flex-direction: column;
  }
}
</style>