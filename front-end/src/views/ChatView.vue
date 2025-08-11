<template>
  <div class="chat-view">
    <div class="main-layout">
      <div class="layout-container">
        <ChatSidebar 
          :activeChat="activeChat"
          :isLoggedIn="true"
          @chatSelected="onChatSelected"
          @newChatCreated="onNewChatCreated"
          @request-new-chat="openNewChatModal"
        />
        <ChatMainArea 
          :activeChat="activeChat"
          :isLoggedIn="true"
          @newChatStarted="onNewChatStarted"
          @messageSent="onMessageSent"
          @chatDeleted="onChatDeleted"
          @openSettings="onOpenSettings"
          @request-new-chat="openNewChatModal"
        />
      </div>
    </div>

    <!-- 새 채팅 생성 모달 -->
    <NewChatModal 
      :isVisible="showNewChatModal"
      @close="closeNewChatModal"
      @create="handleCreateNewChat"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import ChatSidebar from '@/components/chat/ChatSidebar.vue'
import ChatMainArea from '@/components/chat/ChatMainArea.vue'
import NewChatModal from '@/components/chat/NewChatModal.vue'
import chatStore from '@/store/chatStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeChat = ref(null)
const showNewChatModal = ref(false)

// 채팅 선택 핸들러
const onChatSelected = (chatId) => {
  activeChat.value = chatId
  chatStore.setActiveChat(chatId)
  router.push(`/chat/${chatId}`)
}

// 새 채팅 생성 핸들러
const onNewChatCreated = (newChatId) => {
  activeChat.value = newChatId
  chatStore.setActiveChat(newChatId)
  router.push(`/chat/${newChatId}`)
}

// 새 채팅 시작 핸들러
const onNewChatStarted = (newChatId) => {
  activeChat.value = newChatId
  chatStore.setActiveChat(newChatId)
}

// 메시지 전송 핸들러
const onMessageSent = () => {
  // 메시지 전송 후 처리 로직
}

// 채팅 삭제 핸들러
const onChatDeleted = async (chatId) => {
  
  try {
    // chatStore를 통해 실제 삭제 실행
    await chatStore.deleteChat(chatId)
    
    // 삭제된 채팅이 현재 활성 채팅이면 초기화
    if (activeChat.value === chatId) {
      activeChat.value = null
      chatStore.setActiveChat(null)
      router.push('/chat')
    }
  } catch (error) {
    console.error('채팅 삭제 실패:', error)
    // 에러 처리 (토스트 메시지 등)
  }
}

// 설정 열기 핸들러
const onOpenSettings = (chatId) => {
  router.push(`/chat/${chatId}/settings`)
}

// 새 채팅 모달 열기
const openNewChatModal = () => {
  showNewChatModal.value = true
}

// 새 채팅 모달 닫기
const closeNewChatModal = () => {
  showNewChatModal.value = false
}

// 새 채팅 생성 처리
const handleCreateNewChat = async (chatSettings) => {
  try {
    
    // chatStore를 통해 새 채팅 생성
    const newChatId = await chatStore.createNewChatWithSettings(chatSettings)
    
    // 모달 닫기
    closeNewChatModal()
    
    // 새 채팅으로 이동
    activeChat.value = newChatId
    chatStore.setActiveChat(newChatId)
    router.push(`/chat/${newChatId}`)
    
  } catch (error) {
    console.error('새 채팅 생성 실패:', error)
    // 에러 처리 (토스트 메시지 등)
  }
}

// 라우트 파라미터 변경 감지 (채팅 목록 로드 후에만 실행)
watch(() => route.params.id, async (newId) => {
  
  // 채팅 목록이 로드되지 않았으면 대기
  if (chatStore.chats.length === 0) {
    return
  }
  
  if (newId) {
    // URL에서 채팅 ID가 있으면 설정
    activeChat.value = newId
    chatStore.setActiveChat(newId)
    
    // 메시지가 없으면 로드
    const chat = chatStore.getChat(newId)
    if (chat && (!chat.messages || chat.messages.length === 0)) {
      await chatStore.loadChatWithMessages(newId)
    } else if (!chat) {
      console.warn('⚠️ 존재하지 않는 채팅 ID:', newId)
    }
  } else {
    activeChat.value = null
    chatStore.setActiveChat(null)
  }
})

// 컴포넌트 마운트 시 초기화
onMounted(async () => {
  
  // 채팅 목록 로드
  try {
    await chatStore.initialize()
    
    // 채팅 목록 로드 후 현재 라우트 처리
    const currentChatId = route.params.id
    if (currentChatId) {
      activeChat.value = currentChatId
      chatStore.setActiveChat(currentChatId)
      
      // 메시지 로드
      const chat = chatStore.getChat(currentChatId)
      if (chat && (!chat.messages || chat.messages.length === 0)) {
        await chatStore.loadChatWithMessages(currentChatId)
      } else if (chat) {
      } else {
        console.warn('⚠️ 존재하지 않는 채팅 ID:', currentChatId)
      }
    }
  } catch (error) {
    console.error('❌ 초기화 실패:', error)
  }
})
</script>

<style scoped>
.chat-view {
  height: calc(100vh - 72px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.main-layout {
  flex: 1;
  display: flex;
  height: 100%;
  overflow: hidden;
  justify-content: center;
}

.layout-container {
  width: 100%;
  max-width: 1400px;
  display: flex;
  height: 100%;
  overflow: hidden;
  padding: 0 24px;
  box-sizing: border-box;
  gap: 24px;
  margin: 0 auto;
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .layout-container {
    max-width: 100%;
    padding: 0 16px;
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .layout-container {
    flex-direction: column;
    padding: 0 12px;
    gap: 0;
  }
  
  .main-layout {
    height: 100%;
  }
}
</style>