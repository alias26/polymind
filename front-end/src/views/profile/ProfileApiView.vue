<template>
  <div class="tab-content">
    <h2 class="tab-title">API 설정</h2>
    <p class="tab-subtitle">AI API 키를 입력하여 PolyMind를 사용하세요</p>
    <div class="api-settings">
      <div class="api-card">
        <div class="api-header">
          <div class="api-icon gpt-icon">
            <span>GPT</span>
          </div>
          <div class="api-info">
            <h3>OpenAI GPT</h3>
            <p>ChatGPT API 키를 입력하세요</p>
          </div>
        </div>
        <div class="api-form">
          <input
            :value="getDisplayValue('gpt')"
            @input="updateInputKey('gpt', $event.target.value)"
            :type="showKey.gpt ? 'text' : 'password'"
            :placeholder="
              serverKeys.gpt
                ? '••••••••••••••••••••••••••••••••••••••••••••••••'
                : 'sk-...'
            "
            class="api-input"
            :class="{ valid: isCurrentKeyValid('gpt') }"
            :readonly="serverKeys.gpt && !showKey.gpt"
          />
          <div class="api-buttons">
            <button
              v-if="serverKeys.gpt"
              @click="toggleShowKey('gpt')"
              class="btn-base btn-show"
              :disabled="loading[`show_gpt`]"
            >
              {{
                loading[`show_gpt`]
                  ? '로딩 중...'
                  : showKey.gpt
                    ? 'API 숨기기'
                    : 'API 표시'
              }}
            </button>
            <button
              @click="saveApiKey('gpt')"
              class="btn-base btn-primary"
              :disabled="!canSaveKey('gpt') || loading.gpt"
            >
              {{ loading.gpt ? '저장 중...' : '저장' }}
            </button>
            <button
              @click="clearApiKey('gpt')"
              class="btn-base btn-danger"
              :disabled="(!inputKeys.gpt && !serverKeys.gpt) || loading.gpt"
            >
              {{ loading.gpt ? '삭제 중...' : '지우기' }}
            </button>
          </div>
        </div>
      </div>

      <div class="api-card">
        <div class="api-header">
          <div class="api-icon claude-icon">
            <span>Claude</span>
          </div>
          <div class="api-info">
            <h3>Anthropic Claude</h3>
            <p>Claude API 키를 입력하세요</p>
          </div>
        </div>
        <div class="api-form">
          <input
            :value="getDisplayValue('claude')"
            @input="updateInputKey('claude', $event.target.value)"
            :type="showKey.claude ? 'text' : 'password'"
            :placeholder="
              serverKeys.claude
                ? '••••••••••••••••••••••••••••••••••••••••••••••••'
                : 'sk-ant-...'
            "
            class="api-input"
            :class="{ valid: isCurrentKeyValid('claude') }"
            :readonly="serverKeys.claude && !showKey.claude"
          />
          <div class="api-buttons">
            <button
              v-if="serverKeys.claude"
              @click="toggleShowKey('claude')"
              class="btn-base btn-show"
              :disabled="loading[`show_claude`]"
            >
              {{
                loading[`show_claude`]
                  ? '로딩 중...'
                  : showKey.claude
                    ? 'API 숨기기'
                    : 'API 표시'
              }}
            </button>
            <button
              @click="saveApiKey('claude')"
              class="btn-base btn-primary"
              :disabled="!canSaveKey('claude') || loading.claude"
            >
              {{ loading.claude ? '저장 중...' : '저장' }}
            </button>
            <button
              @click="clearApiKey('claude')"
              class="btn-base btn-danger"
              :disabled="
                (!inputKeys.claude && !serverKeys.claude) || loading.claude
              "
            >
              {{ loading.claude ? '삭제 중...' : '지우기' }}
            </button>
          </div>
        </div>
      </div>

      <div class="api-card">
        <div class="api-header">
          <div class="api-icon gemini-icon">
            <span>Gemini</span>
          </div>
          <div class="api-info">
            <h3>Google Gemini</h3>
            <p>Gemini API 키를 입력하세요</p>
          </div>
        </div>
        <div class="api-form">
          <input
            :value="getDisplayValue('gemini')"
            @input="updateInputKey('gemini', $event.target.value)"
            :type="showKey.gemini ? 'text' : 'password'"
            :placeholder="
              serverKeys.gemini
                ? '••••••••••••••••••••••••••••••••••••••••••••••••'
                : 'AI...'
            "
            class="api-input"
            :class="{ valid: isCurrentKeyValid('gemini') }"
            :readonly="serverKeys.gemini && !showKey.gemini"
          />
          <div class="api-buttons">
            <button
              v-if="serverKeys.gemini"
              @click="toggleShowKey('gemini')"
              class="btn-base btn-show"
              :disabled="loading[`show_gemini`]"
            >
              {{
                loading[`show_gemini`]
                  ? '로딩 중...'
                  : showKey.gemini
                    ? 'API 숨기기'
                    : 'API 표시'
              }}
            </button>
            <button
              @click="saveApiKey('gemini')"
              class="btn-base btn-primary"
              :disabled="!canSaveKey('gemini') || loading.gemini"
            >
              {{ loading.gemini ? '저장 중...' : '저장' }}
            </button>
            <button
              @click="clearApiKey('gemini')"
              class="btn-base btn-danger"
              :disabled="
                (!inputKeys.gemini && !serverKeys.gemini) || loading.gemini
              "
            >
              {{ loading.gemini ? '삭제 중...' : '지우기' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="setting-actions">
      <button
        @click="clearAllKeys"
        class="btn-base btn-danger"
        :disabled="loading.all"
      >
        <span>🗑️</span>
        {{ loading.all ? '삭제 중...' : '모든 키 지우기' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated, computed } from 'vue'
import { useApiKeyStore } from '@/store/apiKeys'
import { useLoadingStore } from '@/store/loading'
import { apiKeyApi } from '@/apis'
import { toastService } from '@/utils/toastService'

const apiKeyStore = useApiKeyStore()
const loadingStore = useLoadingStore()
const serverKeys = ref({})
const showKey = ref({})
const inputKeys = ref({})
const originalKeys = ref({})

// 전역 스토어에서 로딩 상태 가져오기
const loading = computed(() => ({
  show_gpt: loadingStore.isOperationLoading('api-show-gpt'),
  show_claude: loadingStore.isOperationLoading('api-show-claude'),
  show_gemini: loadingStore.isOperationLoading('api-show-gemini'),
  gpt: loadingStore.isOperationLoading('api-save-gpt'),
  claude: loadingStore.isOperationLoading('api-save-claude'),
  gemini: loadingStore.isOperationLoading('api-save-gemini'),
  all: loadingStore.isOperationLoading('api-clear-all')
}))

// 프론트엔드 provider를 백엔드 provider로 매핑
const getBackendProvider = (frontendProvider) => {
  const mapping = {
    gpt: 'openai',
    chatgpt: 'openai',
    openai: 'openai',
    claude: 'anthropic',
    anthropic: 'anthropic',
    gemini: 'google',
    google: 'google',
  }
  return mapping[frontendProvider] || frontendProvider
}

// 서버에 저장된 API 키 존재 여부 확인
const checkServerApiKeys = async () => {
  const providers = ['gpt', 'claude', 'gemini']

  for (const provider of providers) {
    try {
      const backendProvider = getBackendProvider(provider)
      const keyInfo = await apiKeyApi.checkApiKeyExists(backendProvider)
      if (keyInfo) {
        serverKeys.value[provider] = true
      }
    } catch (error) {
      // 404는 정상적인 경우 (키가 없음)
      if (!error.message.includes('404')) {
        console.error(`${provider} API 키 확인 오류:`, error)
      }
    }
  }
}

// API 키 표시/숨기기 토글
const toggleShowKey = async (provider) => {
  if (showKey.value[provider]) {
    // 키 숨기기
    showKey.value[provider] = false
    inputKeys.value[provider] = ''
    originalKeys.value[provider] = ''
    apiKeyStore.clearKey(provider)
  } else {
    // 키 표시
    try {
      loadingStore.startOperation(`api-show-${provider}`, 'API 키 로딩 중...')
      const backendProvider = getBackendProvider(provider)
      const response = await apiKeyApi.getDecryptedApiKey(backendProvider)

      inputKeys.value[provider] = response.api_key
      originalKeys.value[provider] = response.api_key // 원본 키 저장
      apiKeyStore.setKey(provider, response.api_key)
      showKey.value[provider] = true
    } catch (error) {
      console.error(`${provider} API 키 로드 오류:`, error)
      toastService.error(`API 키 로드 실패: ${error.message}`)
    } finally {
      loadingStore.stopOperation(`api-show-${provider}`)
    }
  }
}

// 입력창 값 업데이트 함수
const updateInputKey = (provider, value) => {
  inputKeys.value[provider] = value
  // validation을 위해 항상 store 업데이트
  apiKeyStore.setKey(provider, value)
}

// 입력창에 표시할 값 계산
const getDisplayValue = (provider) => {
  if (serverKeys.value[provider] && !showKey.value[provider]) {
    return ''
  }
  return inputKeys.value[provider] || apiKeyStore.getKey(provider) || ''
}

// 현재 입력값이 유효한지 확인 (UI 표시용)
const isCurrentKeyValid = (provider) => {
  const currentValue = inputKeys.value[provider] || apiKeyStore.getKey(provider)

  // 서버에 키가 있고 숨겨진 상태이면서 입력창이 비어있으면 유효한 것으로 표시
  if (serverKeys.value[provider] && !showKey.value[provider] && !currentValue) {
    return true
  }

  // 실제 입력값이 있으면 validation 수행
  if (currentValue) {
    return apiKeyStore.isValidKey(provider, currentValue)
  }

  return false
}

// 저장 가능한지 확인 (저장 버튼용)
const canSaveKey = (provider) => {
  const currentValue = inputKeys.value[provider]
  
  // 입력값이 없으면 저장 불가
  if (!currentValue || currentValue.trim() === '') {
    return false
  }

  // 입력값이 있고 유효한 형식이어야 저장 가능
  if (apiKeyStore.isValidKey(provider, currentValue)) {
    // 서버에 이미 키가 있는 경우
    if (serverKeys.value[provider]) {
      // showKey가 true인 경우 (키를 표시 중인 경우)
      if (showKey.value[provider]) {
        // 원본 키와 현재 입력값이 다르면 저장 가능 (키가 변경됨)
        return currentValue !== originalKeys.value[provider]
      }
      // showKey가 false인 경우에만 새로운 키 입력으로 간주하여 저장 가능
      return true
    }
    // 서버에 키가 없는 경우에는 항상 저장 가능
    return true
  }

  return false
}

// 개별 API 키 저장
const saveApiKey = async (provider) => {
  try {
    const key = inputKeys.value[provider] || apiKeyStore.getKey(provider)

    // 입력값이 없으면 저장할 수 없음
    if (!key || key.trim() === '') {
      toastService.error('저장할 API 키를 입력해주세요.')
      return
    }

    // API 키 형식 검증
    if (!apiKeyStore.isValidKey(provider, key)) {
      toastService.invalidApiKey()
      return
    }

    loadingStore.startOperation(`api-save-${provider}`, 'API 키 저장 중...')

    // 서버사이드 저장
    await apiKeyApi.saveApiKey(provider, key)

    toastService.apiKeySaved(provider)
    serverKeys.value[provider] = true
    originalKeys.value[provider] = key // 저장 후 원본 키 업데이트
  } catch (error) {
    console.error('API 키 저장 오류:', error)
    toastService.apiKeyError(`API 키 저장 실패: ${error.message}`)
  } finally {
    loadingStore.stopOperation(`api-save-${provider}`)
  }
}

// 개별 API 키 지우기
const clearApiKey = async (provider) => {
  try {
    if (
      confirm(
        `${provider.toUpperCase()} API 키를 지우시겠습니까? (서버에서도 삭제됩니다)`
      )
    ) {
      loadingStore.startOperation(`api-save-${provider}`, 'API 키 삭제 중...')

      // 서버사이드 삭제 (백엔드 provider 사용)
      const backendProvider = getBackendProvider(provider)
      await apiKeyApi.deleteApiKey(backendProvider)

      // 로컬 삭제
      apiKeyStore.clearKey(provider)
      inputKeys.value[provider] = ''
      originalKeys.value[provider] = ''
      serverKeys.value[provider] = false
      showKey.value[provider] = false

      toastService.apiKeyDeleted(provider)
    }
  } catch (error) {
    console.error('API 키 삭제 오류:', error)
    toastService.apiKeyError(`API 키 삭제 실패: ${error.message}`)
  } finally {
    loadingStore.stopOperation(`api-save-${provider}`)
  }
}

// 모든 API 키 지우기
const clearAllKeys = async () => {
  try {
    if (confirm('모든 API 키를 지우시겠습니까? (서버에서도 삭제됩니다)')) {
      loadingStore.startOperation('api-clear-all', '모든 API 키 삭제 중...')

      // 서버사이드 삭제
      await apiKeyApi.deleteAllApiKeys()

      // 로컬 삭제
      apiKeyStore.clearAllKeys()
      inputKeys.value = {}
      originalKeys.value = {}
      serverKeys.value = {}
      showKey.value = {}

      toastService.success('모든 API 키가 삭제되었습니다.', {
        title: '삭제 완료',
      })
    }
  } catch (error) {
    console.error('모든 API 키 삭제 오류:', error)
    toastService.apiKeyError(`모든 API 키 삭제 실패: ${error.message}`)
  } finally {
    loadingStore.stopOperation('api-clear-all')
  }
}

// 초기화 함수
const initializeComponent = () => {
  // 기존 로컬 키들을 inputKeys에 복사
  const providers = ['gpt', 'claude', 'gemini']
  providers.forEach((provider) => {
    // showKey 상태가 true인 경우 (표시 중인 경우)
    if (showKey.value[provider]) {
      // 표시 중인 키는 유지
      const existingKey = apiKeyStore.getKey(provider)
      inputKeys.value[provider] = existingKey || ''
    } else {
      // 표시 중이지 않은 경우 입력값 초기화
      inputKeys.value[provider] = ''
    }
    
    // showKey 상태 초기화
    if (showKey.value[provider] === undefined) {
      showKey.value[provider] = false
    }
  })

  checkServerApiKeys()
}

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  initializeComponent()
})

// 탭 변경 후 다시 활성화될 때 초기화
onActivated(() => {
  initializeComponent()
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

.api-settings {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
  width: 100%;
}

.api-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  width: 100%;
  box-sizing: border-box;
}

.api-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.api-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  color: white;
}

.gpt-icon {
  background: linear-gradient(135deg, #10a37f, #1a7f64);
}

.claude-icon {
  background: linear-gradient(135deg, #ff6b35, #f7931e);
}

.gemini-icon {
  background: linear-gradient(135deg, #4285f4, #34a853);
}

.api-info h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.5;
  text-align: left;
}

.api-info p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
  text-align: left;
}

.api-form {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.api-buttons {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.api-buttons > button {
  min-width: fit-content;
  white-space: nowrap;
  height: 44px;
  align-items: center;
  justify-content: center;
}

.api-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  font-family: 'Monaco', 'Courier New', monospace;
  background: #ffffff;
}

.api-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.api-input.valid {
  border-color: #10b981;
  background: #f0fdf4;
}

.api-input.valid:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.api-input[readonly] {
  background-color: #f9fafb;
  cursor: default;
}

.api-input[readonly]:focus {
  box-shadow: none;
  border-color: #d1d5db;
}

.save-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  box-shadow: 0 1px 3px rgba(99, 102, 241, 0.2);
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(99, 102, 241, 0.3);
}

.save-btn:active:not(:disabled) {
  transform: translateY(0);
}

.save-btn:disabled {
  background: #9ca3af;
  color: #ffffff;
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
  box-shadow: none;
}

.api-buttons .clear-btn {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  color: #ef4444;
  border: 1px solid #ef4444;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.api-buttons .clear-btn:hover:not(:disabled) {
  background: #fef2f2;
  border-color: #dc2626;
  color: #dc2626;
  transform: translateY(-1px);
}

.api-buttons .clear-btn:active:not(:disabled) {
  transform: translateY(0);
}

.api-buttons .clear-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
  border-color: #9ca3af;
  color: #ffffff;
}

.setting-actions {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.clear-all-btn {
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2);
}

.clear-all-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
}

.clear-all-btn:active {
  transform: translateY(0);
}

.clear-all-btn:disabled {
  background: #9ca3af;
  color: #ffffff;
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-show {
  padding: 0.5rem 1rem;
  background: #e0e7ff;
  color: #4338ca;
  border: 1px solid #c7d2fe;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-show:hover:not(:disabled) {
  background: #c7d2fe;
  border-color: #a5b4fc;
  color: #3730a3;
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(67, 56, 202, 0.2);
}

.btn-show:active:not(:disabled) {
  transform: translateY(0);
}

.btn-show:disabled {
  background: #f3f4f6;
  color: #9ca3af;
  border-color: #d1d5db;
  cursor: not-allowed;
  opacity: 0.7;
  transform: none;
  box-shadow: none;
}

.show-key-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  white-space: nowrap;
}

.show-key-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(139, 92, 246, 0.3);
}

.show-key-btn:active:not(:disabled) {
  transform: translateY(0);
}

.show-key-btn:disabled {
  background: #9ca3af;
  color: #ffffff;
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
  box-shadow: none;
}

.btn-icon {
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .api-form {
    flex-direction: column;
    align-items: stretch;
  }

  .api-buttons {
    justify-content: center;
  }
}
</style>
