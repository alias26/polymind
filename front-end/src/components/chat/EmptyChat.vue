<template>
  <div class="empty-chat-container">
    <div class="empty-chat-content">
      <!-- 로고 및 환영 메시지 -->
      <div class="welcome-section">
        <div class="logo-icon">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L13.09 8.26L22 9L13.09 9.74L12 16L10.91 9.74L2 9L10.91 8.26L12 2Z" fill="url(#gradient1)"/>
            <defs>
              <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea"/>
                <stop offset="100%" style="stop-color:#764ba2"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <h1 class="welcome-title">PolyMind에 오신 것을 환영합니다!</h1>
        <p class="welcome-subtitle">AI와 함께 새로운 대화를 시작해보세요</p>
      </div>

      <!-- 액션 버튼들 -->
      <div class="action-buttons">
        <button class="action-btn primary-btn" @click="openNewChatModal">
          <div class="btn-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/>
            </svg>
          </div>
          <div class="btn-content">
            <span class="btn-title">새 채팅 시작</span>
            <span class="btn-subtitle">AI와 새로운 대화를 시작합니다</span>
          </div>
        </button>

        <button class="action-btn secondary-btn" @click="loadRecentChats" :disabled="isLoading">
          <div class="btn-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/>
            </svg>
          </div>
          <div class="btn-content">
            <span class="btn-title">최근 채팅 불러오기</span>
            <span class="btn-subtitle">이전 대화 기록을 확인합니다</span>
          </div>
        </button>
      </div>

      <!-- 기능 소개 -->
      <div class="features-section">
        <h3 class="features-title">PolyMind 기능</h3>
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">🤖</div>
            <span class="feature-text">다양한 AI 모델</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">💬</div>
            <span class="feature-text">실시간 대화</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">📝</div>
            <span class="feature-text">채팅 기록 저장</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <span class="feature-text">빠른 응답</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['open-new-chat-modal', 'load-recent-chats'])

const isLoading = ref(false)

const openNewChatModal = () => {
  emit('open-new-chat-modal')
}

const loadRecentChats = async () => {
  isLoading.value = true
  try {
    emit('load-recent-chats')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.empty-chat-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #ffffff;
}

.empty-chat-content {
  max-width: 600px;
  width: 100%;
  text-align: center;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 3rem;
}

.logo-icon {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.welcome-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.welcome-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin: 0;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 3rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.primary-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.secondary-btn {
  background: white;
  color: #374151;
  border: 2px solid #e5e7eb;
}

.secondary-btn:hover:not(:disabled) {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.secondary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
}

.secondary-btn .btn-icon {
  background: #f3f4f6;
  color: #667eea;
}

.btn-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.btn-title {
  font-size: 1.125rem;
  font-weight: 600;
}

.btn-subtitle {
  font-size: 0.875rem;
  opacity: 0.8;
}

.features-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.features-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1.25rem;
  text-align: center;
}

.features-grid {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  justify-content: center;
  max-width: 480px;
  margin: 0 auto;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  flex: 1;
  min-width: 90px;
}

.feature-item:hover {
  background: #f8fafc;
  border-color: #cbd5e0;
  transform: translateY(-1px);
}

.feature-icon {
  font-size: 1.25rem;
}

.feature-text {
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 500;
  text-align: center;
  line-height: 1.2;
}

/* 반응형 디자인 */
@media (max-width: 640px) {
  .empty-chat-container {
    padding: 1rem;
  }
  
  .welcome-title {
    font-size: 1.75rem;
  }
  
  .action-btn {
    padding: 1rem;
  }
  
  .btn-icon {
    width: 40px;
    height: 40px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .feature-item {
    padding: 0.75rem;
  }
}
</style>