<template>
  <div class="chat-settings">
    <div class="settings-header">
      <div class="settings-header-container">
        <button class="back-btn" @click="goBack">
          <span class="back-icon">←</span>
          <span>돌아가기</span>
        </button>
        <h2>채팅 설정</h2>
      </div>
    </div>

    <div class="settings-layout">
      <!-- 좌측 사이드바 -->
      <div class="settings-sidebar">
        <nav class="sidebar-nav">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            :class="['nav-item', { active: activeTab === tab.key }]"
            @click="activeTab = tab.key"
          >
            <span class="nav-icon">{{ tab.icon }}</span>
            <span>{{ tab.label }}</span>
          </button>
        </nav>
      </div>

      <!-- 우측 콘텐츠 -->
      <div class="settings-content">
        <!-- 일반 설정 탭 -->
        <div v-show="activeTab === 'general'" class="content-area">
          <!-- 채팅 제목 -->
          <div class="form-group">
            <label class="form-label">채팅 제목</label>
            <input
              v-model="editingTitle"
              type="text"
              class="form-input"
              placeholder="채팅 제목을 입력하세요"
            />
          </div>

          <!-- AI 모델 -->
          <div class="form-group">
            <label class="form-label">AI 모델</label>
            <div class="model-grid">
              <div class="model-field">
                <label class="field-label">API (변경 불가)</label>
                <div class="api-badge">
                  {{ currentChatModelInfo?.apiName || 'Claude' }}
                </div>
              </div>
              <div class="model-field">
                <label class="field-label">모델</label>
                <select v-model="editingModel" class="form-select">
                  <option 
                    v-for="model in availableModels" 
                    :key="model.key" 
                    :value="model.key"
                  >
                    {{ model.name }}
                  </option>
                </select>
              </div>
            </div>
            <p class="form-hint">
              ※ API 변경 시 기존 채팅 내용의 의미가 달라질 수 있어 API는 변경할
              수 없습니다.
            </p>
          </div>

          <!-- Temperature -->
          <div class="form-group">
            <label class="form-label">Temperature</label>
            <div class="slider-container">
              <input
                v-model="editingTemperature"
                type="range"
                :min="currentModelSettings?.temperature.min || 0"
                :max="currentModelSettings?.temperature.max || 1"
                :step="currentModelSettings?.temperature.step || 0.1"
                class="form-slider"
              />
              <span class="slider-value">{{ editingTemperature }}</span>
            </div>
            <p class="form-hint">
              창의성 조절 ({{ currentModelSettings?.temperature.min || 0 }}:
              일관성, {{ currentModelSettings?.temperature.max || 1 }}: 창의성)
            </p>
          </div>

          <!-- 최대 토큰 수 -->
          <div class="form-group">
            <label class="form-label">최대 토큰 수</label>
            <input
              v-model="editingMaxTokens"
              type="number"
              :min="currentModelSettings?.maxTokens.min || 1"
              :max="currentModelSettings?.maxTokens.max || 8192"
              class="form-input"
              placeholder="최대 토큰 수를 입력하세요"
            />
            <p class="form-hint">
              응답의 최대 길이 제한 ({{
                currentModelSettings?.maxTokens.min || 1
              }}-{{ currentModelSettings?.maxTokens.max || 8192 }})
            </p>
          </div>
        </div>

        <!-- 프롬프트 탭 -->
        <div v-show="activeTab === 'prompt'" class="content-area">
          <div class="form-group">
            <label class="form-label">시스템 프롬프트</label>
            <textarea
              v-model="editingSystemPrompt"
              class="form-textarea"
              placeholder="시스템 프롬프트를 입력하세요"
            ></textarea>
            <p class="form-hint">
              AI의 행동과 응답 스타일을 정의하는 지침입니다.
            </p>
          </div>
        </div>

        <div class="settings-actions">
          <button class="btn-base btn-primary" @click="saveSettings">
            <span>💾</span>
            저장
          </button>
          <button class="btn-base btn-secondary" @click="cancelChanges">
            <span>↺</span>
            취소
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import chatStore from '@/store/chatStore'
import { getModelSettings, getApiFromModel, getModelList, getCurrentApi, MODEL_SETTINGS } from '@/config/modelSettings'

const route = useRoute()
const router = useRouter()

const chatId = computed(() => {
  const id = route.params.chatId
  // 숫자로 변환 (백엔드 ID가 숫자형인 경우)
  return id ? parseInt(id) : null
})
const activeTab = ref('general')
const editingTitle = ref('')
const editingSystemPrompt = ref('')
const editingModel = ref('')
const editingTemperature = ref(0.7)
const editingMaxTokens = ref(2048)

const tabs = [
  { key: 'general', label: '일반 설정', icon: '⚙️' },
  { key: 'prompt', label: '프롬프트', icon: '📝' },
]

const currentChatModelInfo = computed(() => {
  if (!chatId.value) return null
  const chat = chatStore.getChat(chatId.value)
  if (!chat) return null
  
  const modelKey = chat.model || chat.selectedModel || 'claude-3-sonnet'
  const apiKey = getApiFromModel(modelKey)
  const apiName = MODEL_SETTINGS[apiKey]?.name || 'Unknown'

  return {
    apiName: apiName,
    model: modelKey,
    apiKey: apiKey,
  }
})

// 사용 가능한 모델 목록
const availableModels = computed(() => {
  if (!chatId.value) return []
  
  const chat = chatStore.getChat(chatId.value)
  if (!chat) return []
  
  // 채팅에 저장된 apiKey를 사용하거나, 모델로부터 API 추정
  const modelKey = chat.model || chat.selectedModel || 'claude-3-sonnet'
  const apiKey = chat.apiKey || getApiFromModel(modelKey)
  return getModelList(apiKey)
})

// 현재 선택된 모델의 설정 범위
const currentModelSettings = computed(() => {
  if (!currentChatModelInfo.value) return null
  return getModelSettings(
    currentChatModelInfo.value.apiKey,
    currentChatModelInfo.value.model
  )
})

const loadChatSettings = async () => {
  if (!chatId.value) {
    console.error('ChatSettings: chatId가 없습니다.')
    return
  }
  
  
  // 특정 채팅의 완전한 데이터를 로드 (새로고침 시에도 안정적)
  
  // 항상 서버에서 해당 채팅의 완전한 데이터를 로드
  let chat
  try {
    await chatStore.loadChatWithMessages(chatId.value)
    chat = chatStore.getChat(chatId.value)
  } catch (error) {
    console.error('채팅 데이터 로드 실패:', error)
    return
  }
  
  if (chat) {
    
    editingTitle.value = chat.title || ''
    editingSystemPrompt.value =
      chat.system_prompt || chat.systemPrompt || '당신은 도움이 되는 AI 어시스턴트입니다.'
    editingModel.value = chat.model || chat.selectedModel || 'claude-3-sonnet'
    editingTemperature.value = parseFloat(chat.temperature) || 0.7
    editingMaxTokens.value = parseInt(chat.max_tokens || chat.maxTokens) || 2048
  } else {
    console.error('채팅을 찾을 수 없습니다:', chatId.value)
  }
}

const saveSettings = async () => {
  if (!chatId.value) return
  
  try {
    await chatStore.updateChatTitle(chatId.value, editingTitle.value)
    await chatStore.updateChatSystemPrompt(chatId.value, editingSystemPrompt.value)
    await chatStore.updateChatModel(chatId.value, editingModel.value)
    await chatStore.updateChatTemperature(
      chatId.value,
      parseFloat(editingTemperature.value)
    )
    await chatStore.updateChatMaxTokens(
      chatId.value,
      parseInt(editingMaxTokens.value)
    )
    
    goBack()
  } catch (error) {
    console.error('채팅 설정 저장 실패:', error)
    // 에러 메시지를 사용자에게 표시할 수 있도록 추후 구현
  }
}

const cancelChanges = () => {
  // 현재 채팅을 활성 상태로 유지하면서 메인으로 돌아가기
  if (chatId.value) {
    chatStore.setActiveChat(chatId.value)
    router.push(`/chat/${chatId.value}`)
  } else {
    router.push('/chat')
  }
}

const goBack = () => {
  // 현재 채팅을 활성 상태로 유지하면서 메인으로 돌아가기
  if (chatId.value) {
    chatStore.setActiveChat(chatId.value)
    router.push(`/chat/${chatId.value}`)
  } else {
    router.push('/chat')
  }
}

// chatId가 변경될 때마다 설정 다시 로드
watch(chatId, async (newChatId) => {
  if (newChatId) {
    await loadChatSettings()
  }
})

onMounted(async () => {
  await loadChatSettings()
})
</script>

<style scoped>
.chat-settings {
  height: calc(100vh - 72px);
  display: flex;
  flex-direction: column;
  background: #ffffff;
  overflow: hidden;
}

.settings-header {
  background: #ffffff;
  padding: 20px 0;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.settings-header-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.settings-header h2 {
  margin: 0;
  color: #1f2937;
  font-size: 24px;
  font-weight: 600;
  flex: 1;
}

/* 메인 레이아웃 */
.settings-layout {
  flex: 1;
  display: flex;
  height: 100%;
  overflow: hidden;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  gap: 0;
}

/* 좌측 사이드바 */
.settings-sidebar {
  width: 320px;
  height: 100%;
  background: #f8fafc;
  border-right: 1px solid #e2e8f0;
  border-left: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  text-align: left;
}

.back-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.back-icon {
  font-size: 1rem;
  font-weight: 600;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 24px 24px 0 24px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  text-align: left;
  width: 100%;
}

.nav-item:hover {
  background: #e2e8f0;
  color: #475569;
}

.nav-item.active {
  background: #6366f1;
  color: white;
}

.nav-icon {
  font-size: 1.25rem;
  width: 20px;
  text-align: center;
}

/* 우측 콘텐츠 */
.settings-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: calc(100% - 48px);
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  
  border: 1px solid #e2e8f0;
  margin: 24px;
  min-width: 0;
  overflow: hidden;
  padding: 1.5rem;
  box-sizing: border-box;
}

/* 새로운 폼 스타일 */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 20px;
}

.form-group {
  margin-bottom: 2rem;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  background: #ffffff;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-select {
  width: 100%;
  padding: 10px 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  background: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  box-sizing: border-box;
  min-height: 40px;
}

.form-select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  background: #ffffff;
  resize: vertical;
  height: 400px;
  resize: none;
  font-family: inherit;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-hint {
  margin-top: 8px;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.4;
}

.model-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 20px;
  margin-bottom: 12px;
}

.model-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.api-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 12px;
  background: #f0f9ff;
  border: 1px solid #e0f2fe;
  border-radius: 6px;
  color: #0369a1;
  font-size: 14px;
  font-weight: 500;
  min-height: 40px;
  width: 100%;
  box-sizing: border-box;
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

.settings-actions {
  margin-top: auto;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 1.5rem 0 0 0;
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

.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
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

@media (max-width: 768px) {
  .settings-sidebar {
    width: 100%;
    position: static;
  }

  .sidebar-nav {
    flex-direction: row;
    overflow-x: auto;
  }

  .nav-item {
    white-space: nowrap;
  }

  .settings-layout {
    flex-direction: column;
  }

  .settings-content {
    margin: 1rem;
    padding: 1.5rem;
    max-width: none;
  }

  .model-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  .form-textarea {
    min-height: 200px;
  }
}
</style>
