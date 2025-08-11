<template>
  <div class="tab-content">
    <h2 class="tab-title">기본 프롬프트</h2>
    <p class="tab-subtitle">
      새 채팅 생성시 기본값으로 사용될 시스템 프롬프트입니다
    </p>
    <div class="setting-section">
      <div class="setting-card">
        <div class="prompting-settings">
          <div class="setting-item">
            <label>기본 시스템 프롬프트</label>
            <textarea
              v-model="promptSettings.systemPrompt"
              class="setting-textarea"
              placeholder="기본 시스템 프롬프트를 입력하세요..."
            ></textarea>
            <small class="setting-hint"
              >새 채팅 생성시 기본값으로 사용되는 시스템 프롬프트입니다.</small
            >
          </div>
        </div>
      </div>
    </div>

    <div class="setting-actions">
      <button class="btn-base btn-primary" @click="savePromptSettings">
        <span>💾</span>
        기본 프롬프트 저장
      </button>
      <button class="btn-base btn-secondary" @click="resetToDefaults">
        <span>↺</span>
        초기값 복원
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { toastService } from '@/utils/toastService'
import { userPreferencesApi } from '@/apis/userPreferencesApi'
import { DEFAULT_SETTINGS } from '@/config/modelSettings'

const promptSettings = ref({
  systemPrompt: ''
})

const savePromptSettings = async () => {
  try {
    // 서버에 기본 프롬프트 저장
    await userPreferencesApi.updateUserPreferences({
      default_system_prompt: promptSettings.value.systemPrompt
    })
    
    // 로컬 스토리지에도 백업 저장
    localStorage.setItem('defaultPromptSettings', JSON.stringify(promptSettings.value))
    toastService.promptSaved()
  } catch (error) {
    console.error('기본 프롬프트 저장 오류:', error)
    toastService.promptError()
  }
}

const resetToDefaults = () => {
  if (confirm('기본 프롬프트를 초기값으로 복원하시겠습니까?')) {
    promptSettings.value = {
      systemPrompt: DEFAULT_SETTINGS.systemPrompt
    }
    toastService.promptRestored()
  }
}

const loadServerPromptSettings = async () => {
  try {
    // 서버에서 기본 프롬프트 설정 로드
    const serverPreferences = await userPreferencesApi.getUserPreferences()
    if (serverPreferences && serverPreferences.default_system_prompt) {
      promptSettings.value = {
        systemPrompt: serverPreferences.default_system_prompt
      }
    } else {
      // 서버에 설정이 없으면 기본값 사용
      promptSettings.value = {
        systemPrompt: DEFAULT_SETTINGS.systemPrompt
      }
    }
  } catch (error) {
    console.error('서버에서 기본 프롬프트 로드 오류:', error)
    // 서버 로드 실패 시 로컬 스토리지에서 로드 시도
    loadLocalPromptSettings()
  }
}

const loadLocalPromptSettings = () => {
  // 로컬 스토리지에서 기본 프롬프트 로드 (백업용)
  const savedSettings = localStorage.getItem('defaultPromptSettings')
  if (savedSettings) {
    try {
      const parsed = JSON.parse(savedSettings)
      promptSettings.value = {
        ...promptSettings.value,
        ...parsed
      }
    } catch (error) {
      console.error('로컬 기본 프롬프트 로드 오류:', error)
      // 오류 시 기본값으로 설정
      promptSettings.value = {
        systemPrompt: DEFAULT_SETTINGS.systemPrompt
      }
    }
  } else {
    // 저장된 설정이 없으면 기본값으로 설정
    promptSettings.value = {
      systemPrompt: DEFAULT_SETTINGS.systemPrompt
    }
  }
}

onMounted(() => {
  // 서버에서 기본 프롬프트 로드 시도
  loadServerPromptSettings()
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

.prompting-settings {
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

.setting-textarea {
  padding: 0.875rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  height: 400px;
  resize: none;
  font-family: inherit;
  background: #ffffff;
  transition: all 0.2s ease;
  overflow-y: auto;
}

.setting-textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  background: #fefefe;
}

.setting-textarea::placeholder {
  color: #9ca3af;
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

.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
}

.save-btn:active {
  transform: translateY(0);
}

.reset-btn {
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

.reset-btn:hover {
  background: #e5e7eb;
  color: #4b5563;
  border-color: #9ca3af;
  transform: translateY(-1px);
}

.reset-btn:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .setting-actions {
    flex-direction: column;
  }
}
</style>