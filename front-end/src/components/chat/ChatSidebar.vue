<template>
  <div class="chat-sidebar">
    <div v-if="props.isLoggedIn" class="sidebar-header">
      <h3>채팅 목록</h3>
      <button class="btn-base btn-primary new-chat-btn" @click="requestNewChat">
        <i class="fas fa-plus"></i>
        새 채팅
      </button>
    </div>
    
    <div class="chat-list">
      <!-- 비로그인 상태일 때 안내 메시지 -->
      <div v-if="!props.isLoggedIn" class="login-prompt">
        <div class="prompt-icon">
          🔐
        </div>
        <div class="prompt-content">
          <h4>로그인이 필요합니다</h4>
          <p>채팅 기능을 사용하시려면<br/>로그인을 해주세요.</p>
        </div>
      </div>
      
      <!-- 로그인 된 경우 채팅 목록 -->
      <template v-else>
        <button 
          v-for="chat in chatList" 
          :key="chat.id"
          class="chat-item"
          :class="{ active: String(props.activeChat) === String(chat.id) }"
          @click="selectChat(chat.id)"
          type="button"
        >
          <div class="chat-preview">
            <div class="chat-title">{{ chat.title }}</div>
            <!-- 최근 대화 내역 표시 제거 (성능 개선) -->
          </div>
          <div class="chat-time">{{ formatTime(chat.updatedAt) }}</div>
        </button>
      </template>
    </div>

  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import chatStore from '@/store/chatStore'

const props = defineProps({
  activeChat: {
    type: [String, Number],
    default: null
  },
  isLoggedIn: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['chatSelected', 'newChatCreated', 'request-new-chat'])

// 채팅 목록 가져오기 (반응성 강화)
const chatList = computed(() => {
  
  // 비교 디버깅
  if (chatStore.chats.length > 0) {
    const firstChat = chatStore.chats[0]
  }
  
  // chatStore.chats 배열을 직접 참조하여 반응성을 확보
  const chats = [...chatStore.chats]
  
  const list = chats
    .filter((chat, index, arr) => arr.findIndex(c => c.id === chat.id) === index) // 중복 제거
    .sort((a, b) => new Date(b.updated_at || b.updatedAt) - new Date(a.updated_at || a.updatedAt)) // 정렬
    .map(chat => ({
      id: chat.id,
      title: chat.title || '제목 없음',
      // lastMessage: chatStore.getLastMessage(chat.id), // 성능 개선을 위해 제거
      updatedAt: chat.updated_at || chat.updatedAt
    }))
  
  
  // 중복 ID 체크
  const ids = list.map(chat => chat.id)
  const uniqueIds = [...new Set(ids)]
  if (ids.length !== uniqueIds.length) {
    console.error('ChatSidebar: 중복된 채팅 ID 발견!', ids)
  }
  
  return list
})

// chatStore의 채팅 배열 변화를 명시적으로 감지
watch(() => chatStore.chats.length, (newLength, oldLength) => {
}, { immediate: true })

// chatStore.chats 배열 자체의 변화를 감지
watch(() => [...chatStore.chats], (newChats, oldChats) => {
}, { deep: true })

// 활성 채팅 변화 감지
watch(() => chatStore.activeChat, (newActiveChat, oldActiveChat) => {
})

const selectChat = (chatId) => {
  emit('chatSelected', chatId)
}

// 새 채팅 요청
const requestNewChat = () => {
  emit('request-new-chat')
}

const formatTime = (date) => {
  if (!date) return '시간 없음'
  
  try {
    const now = new Date()
    
    // 백엔드에서 오는 시간이 UTC인지 확인하고 적절히 처리
    let chatDate
    if (typeof date === 'string') {
      // 백엔드에서 UTC 시간으로 저장된 경우, 'Z'가 없으면 추가
      const dateStr = date.includes('Z') ? date : date + 'Z'
      chatDate = new Date(dateStr)
    } else {
      chatDate = new Date(date)
    }
    
    // 유효하지 않은 날짜 체크
    if (isNaN(chatDate.getTime())) {
      return '시간 오류'
    }
    
    const diff = now - chatDate
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)
    
    if (minutes < 1) {
      return '방금 전'
    } else if (minutes < 60) {
      return `${minutes}분 전`
    } else if (hours < 24) {
      return `${hours}시간 전`
    } else if (days < 30) {
      return `${days}일 전`
    } else {
      // 30일 이상이면 날짜 표시
      return chatDate.toLocaleDateString('ko-KR', {
        month: 'short',
        day: 'numeric'
      })
    }
  } catch (error) {
    console.error('날짜 포맷 오류:', error)
    return '시간 오류'
  }
}
</script>

<style scoped>
.chat-sidebar {
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

.sidebar-header {
  padding: 24px 24px 24px 24px;
  border-bottom: 1px solid #e2e8f0;
  background: transparent;
  margin: 0;
}

.sidebar-header h3 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #4338ca;
  font-weight: 700;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: -0.025em;
}

.new-chat-btn {
  width: 100%;
  padding: 12px 16px;
  background: #4338ca;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
  transition: background-color 0.2s ease;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.new-chat-btn:hover {
  background: #3730a3;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 24px 24px 0 24px;
  background: transparent;
  margin: 0;
}

.chat-list::-webkit-scrollbar {
  width: 6px;
}

.chat-list::-webkit-scrollbar-track {
  background: #e2e8f0;
  border-radius: 3px;
}

.chat-list::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.chat-list::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

.chat-item {
  padding: 16px;
  margin: 0 0 8px 0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  position: relative;
  width: 100%;
  text-align: left;
  font-family: inherit;
  font-size: inherit;
  box-sizing: border-box;
}

.chat-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e0;
}

.chat-item:focus {
  outline: 2px solid #6366f1;
  outline-offset: 2px;
}

.chat-item.active {
  background: #e2e8f0;
  border-color: #4338ca;
  border-left: 4px solid #4338ca;
  box-shadow: 0 0 0 2px rgba(67, 56, 202, 0.2);
}

.chat-item.active .chat-title {
  color: #1f2937;
}

.chat-item.active .chat-last-message {
  color: #6b7280;
}

.chat-item.active .chat-time {
  color: #9ca3af;
}

.chat-preview {
  flex: 1;
  min-width: 0;
}

.chat-title {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 6px;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  text-align: left;
}


.chat-time {
  font-size: 11px;
  color: #9ca3af;
  margin-left: 12px;
  flex-shrink: 0;
  font-weight: 500;
}

.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  height: 60%;
  min-height: 300px;
}

.prompt-icon {
  font-size: 48px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.prompt-content h4 {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 12px 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.prompt-content p {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.prompt-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 200px;
}

.prompt-btn {
  padding: 12px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  text-align: center;
  transition: all 0.2s ease;
  border: 1px solid;
}

.prompt-btn.login {
  background: transparent;
  color: #6366f1;
  border-color: #6366f1;
}

.prompt-btn.login:hover {
  background: #6366f1;
  color: white;
}

.prompt-btn.signup {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  border-color: #4f46e5;
  box-shadow: 0 1px 3px rgba(99, 102, 241, 0.15);
}

.prompt-btn.signup:hover {
  background: linear-gradient(135deg, #4f46e5, #4338ca);
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(99, 102, 241, 0.25);
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .chat-sidebar {
    width: 280px;
    min-width: 260px;
    max-width: 300px;
  }
}

@media (max-width: 768px) {
  .chat-sidebar {
    width: 100%;
    min-width: unset;
    max-width: unset;
    height: auto;
    min-height: 200px;
    max-height: 300px;
    margin: 0;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .sidebar-header {
    padding: 16px;
  }
  
  .sidebar-header h3 {
    font-size: 18px;
    margin-bottom: 16px;
  }
  
  .new-chat-btn {
    padding: 10px 14px;
    font-size: 13px;
  }
  
  .chat-list {
    padding: 8px 12px;
    max-height: 160px;
  }
  
  .chat-item {
    padding: 12px;
    margin-bottom: 6px;
  }
  
  .chat-title {
    font-size: 13px;
  }
  
  .chat-time {
    font-size: 10px;
  }
}

</style>