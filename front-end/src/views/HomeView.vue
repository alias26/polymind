<template>
  <div class="home">
    <!-- 로그인된 사용자용 레이아웃 (사이드바 + 메인 영역) -->
    <div v-if="isLoggedIn" class="main-layout">
      <div class="layout-container">
        <ChatSidebar 
          :activeChat="activeChat"
          :isLoggedIn="isLoggedIn"
          @chatSelected="onChatSelected"
          @newChatCreated="onNewChatCreated"
          @request-new-chat="openNewChatModal"
        />
        <ChatMainArea 
          :activeChat="activeChat"
          :isLoggedIn="isLoggedIn"
          @newChatStarted="onNewChatStarted"
          @messageSent="onMessageSent"
          @chatDeleted="onChatDeleted"
          @openSettings="onOpenSettings"
          @request-new-chat="openNewChatModal"
        />
      </div>
    </div>
    
    <!-- 비로그인 사용자용 전체 화면 권유 -->
    <div v-else class="fullscreen-welcome">
      <ChatMainArea 
        :activeChat="null"
        :isLoggedIn="false"
        @newChatStarted="onNewChatStarted"
        @messageSent="onMessageSent"
        @chatDeleted="onChatDeleted"
        @openSettings="onOpenSettings"
        @request-new-chat="openNewChatModal"
      />
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
import ChatSidebar from '@/components/chat/ChatSidebar.vue'
import ChatMainArea from '@/components/chat/ChatMainArea.vue'
import NewChatModal from '@/components/chat/NewChatModal.vue'
import chatStore from '@/store/chatStore'

const router = useRouter()
const route = useRoute()
const activeChat = ref(null)
const isLoggedIn = ref(false)
const showNewChatModal = ref(false)

// 로그인 상태 확인 함수
const checkLoginStatus = () => {
  const token = localStorage.getItem('access_token')
  const loginStatus = !!token
  isLoggedIn.value = loginStatus
  return loginStatus
}

// 컴포넌트 마운트 시 store 초기화 및 로그인 상태에 따른 채팅 복원
onMounted(async () => {
  
  // 로그인 상태 확인 후 채팅 store 초기화 여부 결정
  if (checkLoginStatus()) {
    // 로그인된 상태에서만 chatStore 초기화 (API 호출)
    await chatStore.initialize()
    
    // URL에 chatId가 있으면 해당 채팅을 활성화
    const urlChatId = route.params.chatId
    if (urlChatId) {
      try {
        // 채팅이 존재하는지 확인 후 활성화
        let chat = chatStore.getChat(urlChatId)
        if (chat) {
          activeChat.value = urlChatId
          chatStore.setActiveChat(urlChatId)
          
          // 채팅 메시지가 로드되지 않았다면 로드
          if (!chat.messages || chat.messages.length === 0) {
            await chatStore.loadChatWithMessages(urlChatId)
          } else {
          }
        } else {
          // 로컬에 없으면 서버에서 직접 해당 채팅을 가져와서 확인
          try {
            await chatStore.loadChatWithMessages(urlChatId)
            chat = chatStore.getChat(urlChatId)
            if (chat) {
              activeChat.value = urlChatId
              chatStore.setActiveChat(urlChatId)
            } else {
              router.push('/')
            }
          } catch (loadError) {
            console.error('서버에서 채팅 로드 실패:', loadError)
            router.push('/')
          }
        }
      } catch (error) {
        console.error('URL chatId 처리 중 오류:', error)
        router.push('/')
      }
    } else {
      // URL에 chatId가 없으면 저장된 activeChat 사용
      const savedActiveChat = chatStore.activeChat
      if (savedActiveChat) {
        activeChat.value = savedActiveChat
        
        // 저장된 activeChat의 메시지가 없으면 로드
        const chat = chatStore.getChat(savedActiveChat)
        if (chat && (!chat.messages || chat.messages.length === 0)) {
          try {
            await chatStore.loadChatWithMessages(savedActiveChat)
          } catch (error) {
            console.error('저장된 채팅 메시지 로드 실패:', error)
          }
        }
      } else {
        activeChat.value = null
      }
    }
  } else {
    // 로그인되지 않은 상태에서는 로컬 데이터만 초기화
    chatStore.clearAllData()
    activeChat.value = null
  }
})

// 라우터 경로 변경 감지
watch(() => route.params.chatId, async (newChatId, oldChatId) => {
  
  if (!checkLoginStatus()) {
    activeChat.value = null
    return
  }
  
  if (newChatId && newChatId !== oldChatId) {
    // 새로운 chatId로 변경된 경우
    try {
      let chat = chatStore.getChat(newChatId)
      
      if (chat) {
        activeChat.value = newChatId
        chatStore.setActiveChat(newChatId)
        
        // 채팅 메시지가 로드되지 않았다면 로드
        if (!chat.messages || chat.messages.length === 0) {
          await chatStore.loadChatWithMessages(newChatId)
        } else {
        }
      } else {
        // 로컬에 없으면 서버에서 직접 해당 채팅을 가져와서 확인
        try {
          await chatStore.loadChatWithMessages(newChatId)
          chat = chatStore.getChat(newChatId)
          if (chat) {
            activeChat.value = newChatId
            chatStore.setActiveChat(newChatId)
          } else {
            router.push('/')
          }
        } catch (loadError) {
          console.error('HomeView: 서버에서 채팅 로드 실패:', loadError)
          router.push('/')
        }
      }
    } catch (error) {
      console.error('HomeView: 라우트 chatId 변경 처리 중 오류:', error)
      router.push('/')
    }
  } else if (!newChatId && oldChatId) {
    // chatId가 제거된 경우 (홈으로 이동)
    activeChat.value = chatStore.activeChat
  }
})

// chatStore의 activeChat 변경을 감지하여 HomeView의 activeChat과 동기화
watch(() => chatStore.activeChat, async (newActiveChat) => {
  if (activeChat.value !== newActiveChat) {
    activeChat.value = newActiveChat
    
    // 새로운 채팅이 선택되었을 때 메시지 로드
    if (newActiveChat && isLoggedIn.value) {
      try {
        await chatStore.loadChatWithMessages(newActiveChat)
      } catch (error) {
        console.error('초기 채팅 메시지 로드 중 오류:', error)
      }
    }
  }
})

// localStorage 변경 감지 (다른 탭에서 로그인/로그아웃 시)
window.addEventListener('storage', () => {
  if (!checkLoginStatus()) {
    activeChat.value = null
  }
})

const onChatSelected = async (chatId) => {
  try {
    
    // chatId를 문자열로 변환하여 비교
    const chatIdStr = String(chatId)
    const routeChatIdStr = String(route.params.chatId)
    
    // 즉시 activeChat 설정 및 메시지 로드 (URL 변경과 독립적으로)
    activeChat.value = chatId
    chatStore.setActiveChat(chatId)
    
    // 채팅 메시지가 없으면 미리 로드
    const chat = chatStore.getChat(chatId)
    if (!chat || !chat.messages || chat.messages.length === 0) {
      await chatStore.loadChatWithMessages(chatId)
    }
    
    // URL 업데이트 (위의 처리와 별도로)
    if (routeChatIdStr !== chatIdStr) {
      router.push(`/chat/${chatIdStr}`)
    }
  } catch (error) {
    console.error('HomeView: 채팅 선택 중 오류:', error)
  }
}

const onNewChatCreated = (newChatId) => {
  // URL 업데이트로 새 채팅으로 이동
  router.push(`/chat/${newChatId}`)
}

const onNewChatStarted = (newChatId) => {
  const targetChatId = newChatId || chatStore.activeChat
  if (targetChatId) {
    router.push(`/chat/${targetChatId}`)
  }
}

const onMessageSent = (message) => {
  // 메시지 전송 처리 (이미 chatStore에서 처리됨)
}

const onChatDeleted = async (chatId) => {
  // 채팅 삭제 처리
  try {
    
    // 서버에서 채팅 삭제 (chatStore에서 로컬 캐시와 activeChat도 업데이트함)
    await chatStore.deleteChat(chatId)
    
    
    // 삭제 후 홈으로 이동
    activeChat.value = null
    router.push('/')
    
  } catch (error) {
    console.error('채팅 삭제 중 오류:', error)
    // 사용자에게 에러 알림 (Toast 등)
  }
}

const onOpenSettings = (chatId) => {
  router.push(`/chat/${chatId}/settings`)
}

// 새 채팅 모달 관련
const openNewChatModal = () => {
  showNewChatModal.value = true
}

const closeNewChatModal = () => {
  showNewChatModal.value = false
}

const handleCreateNewChat = async (chatSettings) => {
  try {
    const newChatId = await chatStore.createNewChatWithSettings(chatSettings)
    
    closeNewChatModal()
    // URL 업데이트로 새 채팅으로 이동
    router.push(`/chat/${newChatId}`)
  } catch (error) {
    console.error('새 채팅 생성 실패:', error)
    // 에러 처리 (사용자에게 알림 등)
  }
}
</script>

<style scoped>
.home {
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

.fullscreen-welcome {
  flex: 1;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
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
