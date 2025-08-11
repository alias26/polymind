import { reactive, watch } from 'vue'
import { chatApi } from '@/apis/chatApi'

// 채팅 데이터를 중앙에서 관리하는 store
const chatStore = reactive({
  // 채팅 목록 (배열 형태로 변경)
  chats: [],
  
  // 현재 활성 채팅 ID
  activeChat: null,
  
  // 로딩 상태
  isLoading: false,
  
  
  // 초기화 (서버에서 채팅 목록 로드)
  async initialize() {
    await this.loadChatsFromServer()
    this.loadActiveFromStorage()
    
    // 활성 채팅이 있으면 해당 채팅의 메시지도 로드
    if (this.activeChat) {
      try {
        const chat = this.getChat(this.activeChat)
        if (chat && (!chat.messages || chat.messages.length === 0)) {
          await this.loadChatWithMessages(this.activeChat)
        }
      } catch (error) {
        console.error('chatStore.initialize: 활성 채팅 메시지 로드 실패:', error)
      }
    }
  },
  
  // 서버에서 채팅 목록 로드
  async loadChatsFromServer() {
    try {
      // 토큰이 없으면 API 호출하지 않음
      const token = localStorage.getItem('access_token')
      if (!token) {
        this.chats = []
        return
      }

      this.isLoading = true
      const serverChats = await chatApi.getChats()
      
      // 서버 채팅으로 완전히 교체 (서버가 진실의 소스)
      
      if (serverChats.length === 0) {
        console.warn('⚠️ 서버에서 빈 채팅 목록을 받았습니다!')
      }
      
      // 기존 메시지를 보존하기 위한 맵
      const existingMessagesMap = new Map()
      this.chats.forEach(chat => {
        if (chat.messages && chat.messages.length > 0) {
          existingMessagesMap.set(chat.id, chat.messages)
        }
      })
      
      // 서버 채팅으로 교체하되 기존 메시지는 보존
      this.chats = serverChats.map(serverChat => ({
        ...serverChat,
        messages: existingMessagesMap.get(serverChat.id) || []
      }))
      
    } catch (error) {
      console.error('서버에서 채팅 목록 로드 실패:', error)
      // 인증 오류인 경우 채팅 데이터 초기화
      if (error.message.includes('401') || error.message.includes('403') || error.message.includes('인증')) {
        this.chats = []
        this.activeChat = null
      } else {
        // 기타 서버 연결 실패 시 빈 배열로 초기화
        this.chats = []
      }
    } finally {
      this.isLoading = false
    }
  },
  
  // localStorage에서 활성 채팅 ID만 로드
  loadActiveFromStorage() {
    try {
      if (typeof localStorage !== 'undefined') {
        const savedActiveChat = localStorage.getItem('activeChat')
        if (savedActiveChat) {
          this.activeChat = savedActiveChat
        }
      }
    } catch (error) {
      console.error('활성 채팅 로드 중 오류:', error)
    }
  },

  
  // 활성 채팅 ID만 localStorage에 저장
  saveActiveToStorage() {
    try {
      if (typeof localStorage !== 'undefined') {
        if (this.activeChat) {
          localStorage.setItem('activeChat', this.activeChat)
        } else {
          localStorage.removeItem('activeChat')
        }
      }
    } catch (error) {
      console.error('활성 채팅 저장 중 오류:', error)
    }
  },
  
  // 채팅 목록 가져오기 (최근 업데이트 순으로 정렬)
  getChatList() {
    
    // 중복 제거 후 정렬 (원본 배열 변경 방지를 위해 복사본 생성)
    const uniqueChats = this.chats.filter((chat, index, arr) => 
      arr.findIndex(c => c.id === chat.id) === index
    )
    
    
    return [...uniqueChats].sort((a, b) => 
      new Date(b.updated_at || b.updatedAt) - new Date(a.updated_at || a.updatedAt)
    )
  },
  
  // 특정 채팅 가져오기
  getChat(chatId) {
    
    const result = this.chats.find(chat => chat.id == chatId) || null
    
    
    return result
  },
  
  // 서버에서 특정 채팅 데이터 로드 (최신 메시지만)
  async loadChatWithMessages(chatId) {
    try {
      
      const chat = await chatApi.getChat(chatId)
      // 처음에는 최신 20개 메시지만 로드
      const response = await chatApi.getMessages(chatId, { limit: 20, offset: 0 })
      const messages = response.data
      
      
      // ID 28 메시지 찾아서 디버깅
      const msg28 = messages.find(m => m.id === 28)
      
      if (messages.length === 0) {
        console.warn('⚠️  서버에서 메시지가 0개 반환됨!')
      }
      
      // 로컬 캐시 업데이트 (message_order를 포함하여 정렬)
      const existingChatIndex = this.chats.findIndex(c => c.id === chatId)
      
      // 서버에서 최신순으로 받은 메시지를 오래된 순으로 다시 정렬 (화면 표시용)
      const mappedMessages = messages
        .map(msg => {
          
          // content가 객체인 경우 안전하게 문자열로 변환
          let textContent = msg.content
          if (typeof msg.content === 'object' && msg.content !== null) {
            textContent = JSON.stringify(msg.content, null, 2)
          } else if (typeof msg.content !== 'string') {
            textContent = String(msg.content || '')
          }
          
          
          const resultMessage = {
            id: msg.id,
            sender: msg.sender,
            text: textContent,
            timestamp: msg.created_at,
            message_order: msg.message_order || 0, // 순서 정보 포함
            images: msg.images || [], // 이미지 데이터 포함
            ...(msg.sender === 'ai' && { 
              apiName: msg.api_provider === 'openai' ? 'OpenAI' : 
                       msg.api_provider === 'anthropic' ? 'Claude' : 
                       msg.api_provider === 'google' ? 'Gemini' : 'AI', 
              model: msg.model_name || chat.model 
            })
          }
          
          
          return resultMessage
        })
        .sort((a, b) => (a.message_order || 0) - (b.message_order || 0)) // 화면 표시용으로 오래된 순 정렬
        
      
      const chatWithMessages = {
        ...chat,
        messages: mappedMessages
      }
      
      // 최근 메시지 정보 업데이트 제거 (성능 개선)
      
      
      if (existingChatIndex >= 0) {
        this.chats[existingChatIndex] = chatWithMessages
      } else {
        this.chats.push(chatWithMessages)
      }
      
      const finalChat = this.getChat(chatId)
      return chatWithMessages
    } catch (error) {
      console.error('채팅 메시지 로드 실패:', error)
      throw error
    }
  },

  // 채팅의 주요 AI 모델 정보 가져오기 (가장 최근 사용된 모델)
  getChatMainModel(chatId) {
    const chat = this.getChat(chatId)
    
    if (!chat || !chat.messages || chat.messages.length === 0) {
      return null
    }
    
    // AI 메시지들에서 가장 최근 메시지를 찾음
    const aiMessages = chat.messages.filter(msg => msg.sender === 'ai' && msg.apiName && msg.model)
    
    if (aiMessages.length === 0) {
      return null
    }
    
    // 가장 최근 AI 메시지 반환 (배열의 마지막 요소)
    const latestAiMessage = aiMessages[aiMessages.length - 1]
    
    return { 
      apiName: latestAiMessage.apiName, 
      model: latestAiMessage.model 
    }
  },
  
  // 채팅의 마지막 메시지 가져오기 (사용 중지 - 성능 개선을 위해 빈 문자열 반환)
  getLastMessage(chatId) {
    return ''
  },
  
  
  // 활성 채팅 설정
  setActiveChat(chatId) {
    this.activeChat = chatId
    this.saveActiveToStorage()
  },
  
  // 새 채팅 생성 (서버)
  async createNewChat() {
    try {
      const newChat = await chatApi.createChat({
        title: `새 채팅 ${this.chats.length + 1}`,
        selectedModel: 'claude-3-sonnet'
      })
      
      // 중복 방지: 이미 존재하는 채팅인지 확인
      const existingChatIndex = this.chats.findIndex(chat => chat.id === newChat.id)
      
      // 메시지를 빈 배열로 초기화하여 채팅 객체 생성
      const chatWithMessages = {
        ...newChat,
        messages: []
      }
      
      if (existingChatIndex >= 0) {
        // 이미 존재하면 업데이트
        this.chats[existingChatIndex] = chatWithMessages
      } else {
        // 새 채팅이면 맨 앞에 추가
        this.chats.unshift(chatWithMessages)
      }
      
      this.activeChat = newChat.id
      this.saveActiveToStorage()
      
      return newChat.id
    } catch (error) {
      console.error('새 채팅 생성 실패:', error)
      throw error
    }
  },

  // 설정값과 함께 새 채팅 생성 (서버)
  async createNewChatWithSettings(settings) {
    try {
      
      const requestData = {
        title: settings.title || `새 채팅 ${this.chats.length + 1}`,
        selectedModel: settings.selectedModel,
        systemPrompt: settings.systemPrompt,
        temperature: settings.temperature,
        maxTokens: settings.maxTokens
      }
      
      
      const newChat = await chatApi.createChat(requestData)
      
      
      // 중복 방지: 이미 존재하는 채팅인지 확인
      const existingChatIndex = this.chats.findIndex(chat => chat.id === newChat.id)
      
      // 메시지를 빈 배열로 초기화하여 채팅 객체 생성
      const chatWithMessages = {
        ...newChat,
        messages: []
      }
      
      
      if (existingChatIndex >= 0) {
        // 이미 존재하면 업데이트
        this.chats[existingChatIndex] = chatWithMessages
      } else {
        // 새 채팅이면 맨 앞에 추가
        this.chats.unshift(chatWithMessages)
      }
      
      this.activeChat = newChat.id
      this.saveActiveToStorage()
      
      return newChat.id
    } catch (error) {
      console.error('설정과 함께 새 채팅 생성 실패:', error)
      throw error
    }
  },
  
  // 메시지 추가 (로컬 캐시만)
  addMessage(chatId, message) {
    const chat = this.getChat(chatId)
    if (!chat) return
    
    // 현재 채팅의 최대 message_order 계산
    const currentMaxOrder = chat.messages && chat.messages.length > 0 
      ? Math.max(...chat.messages.map(m => m.message_order || 0)) 
      : 0
    
    // text가 객체인 경우 안전하게 문자열로 변환
    let textContent = message.text
    if (typeof message.text === 'object' && message.text !== null) {
      textContent = JSON.stringify(message.text, null, 2)
    } else if (typeof message.text !== 'string') {
      textContent = String(message.text || '')
    }
    
    const newMessage = {
      id: message.id || Date.now().toString(),
      sender: message.sender,
      text: textContent,
      timestamp: message.timestamp || new Date(),
      message_order: message.message_order || (currentMaxOrder + 1), // 순서 정보 추가
      ...(message.images && { images: message.images }),
      ...(message.apiName && { apiName: message.apiName }),
      ...(message.model && { model: message.model }),
      ...(message.isError && { isError: message.isError })
    }
    
    if (!chat.messages) {
      chat.messages = []
    }
    
    // 메시지를 추가한 후 순서대로 정렬
    chat.messages.push(newMessage)
    chat.messages.sort((a, b) => (a.message_order || 0) - (b.message_order || 0))
    
    // 최근 메시지 캐시 업데이트
    // 최근 메시지 캐시 업데이트 제거 (성능 개선)
    
    // 자동 제목 업데이트 로직 제거 (사용자 입력이 제목으로 바뀌는 문제 해결)
    
    return newMessage
  },

  // 메시지 업데이트 (스트리밍용)
  updateMessage(chatId, messageId, updates) {
    const chat = this.getChat(chatId)
    if (!chat || !chat.messages) return
    
    const messageIndex = chat.messages.findIndex(msg => msg.id === messageId)
    if (messageIndex === -1) return
    
    // 메시지 업데이트
    const existingMessage = chat.messages[messageIndex]
    chat.messages[messageIndex] = {
      ...existingMessage,
      ...updates
    }
    
    return chat.messages[messageIndex]
  },
  
  // 채팅 삭제 (서버)
  async deleteChat(chatId) {
    try {
      
      await chatApi.deleteChat(chatId)
      
      // 로컬 캐시에서 제거 - 반응성을 위해 새 배열로 교체
      const filteredChats = this.chats.filter(chat => chat.id != chatId)
      
      // 반응성 트리거를 위해 배열 전체를 교체
      this.chats.splice(0, this.chats.length, ...filteredChats)
      
      
      // activeChat이 삭제된 채팅이면 null로 설정
      if (this.activeChat == chatId) {
        this.activeChat = null
        this.saveActiveToStorage()
      }
      
      // 서버와 동기화를 위해 최신 채팅 목록을 다시 불러오기
      try {
        await this.loadChatsFromServer()
      } catch (syncError) {
        console.warn('채팅 목록 동기화 실패:', syncError)
        // 동기화 실패해도 로컬 삭제는 이미 완료되었으므로 계속 진행
      }
      
    } catch (error) {
      console.error('채팅 삭제 실패:', error)
      throw error
    }
  },
  
  // 채팅 제목 업데이트 (서버)
  async updateChatTitle(chatId, newTitle) {
    try {
      await chatApi.updateChat(chatId, { title: newTitle })
      
      // 로컬 캐시 업데이트
      const chat = this.getChat(chatId)
      if (chat) {
        chat.title = newTitle
      }
    } catch (error) {
      console.error('채팅 제목 업데이트 실패:', error)
      throw error
    }
  },

  // 채팅 모델 업데이트 (서버)
  async updateChatModel(chatId, newModel) {
    try {
      await chatApi.updateChat(chatId, { selectedModel: newModel })
      
      // 로컬 캐시 업데이트
      const chat = this.getChat(chatId)
      if (chat) {
        chat.model = newModel
        chat.selectedModel = newModel
      }
    } catch (error) {
      console.error('채팅 모델 업데이트 실패:', error)
      throw error
    }
  },

  // 채팅 시스템 프롬프트 업데이트 (서버)
  async updateChatSystemPrompt(chatId, newSystemPrompt) {
    try {
      await chatApi.updateChat(chatId, { systemPrompt: newSystemPrompt })
      
      // 로컬 캐시 업데이트
      const chat = this.getChat(chatId)
      if (chat) {
        chat.system_prompt = newSystemPrompt
        chat.systemPrompt = newSystemPrompt
      }
    } catch (error) {
      console.error('채팅 시스템 프롬프트 업데이트 실패:', error)
      throw error
    }
  },

  // 채팅 Temperature 업데이트 (서버)
  async updateChatTemperature(chatId, newTemperature) {
    try {
      await chatApi.updateChat(chatId, { temperature: newTemperature })
      
      // 로컬 캐시 업데이트
      const chat = this.getChat(chatId)
      if (chat) {
        chat.temperature = newTemperature
      }
    } catch (error) {
      console.error('채팅 Temperature 업데이트 실패:', error)
      throw error
    }
  },

  // 채팅 최대 토큰 수 업데이트 (서버)
  async updateChatMaxTokens(chatId, newMaxTokens) {
    try {
      await chatApi.updateChat(chatId, { maxTokens: newMaxTokens })
      
      // 로컬 캐시 업데이트
      const chat = this.getChat(chatId)
      if (chat) {
        chat.max_tokens = newMaxTokens
        chat.maxTokens = newMaxTokens
      }
    } catch (error) {
      console.error('채팅 최대 토큰 수 업데이트 실패:', error)
      throw error
    }
  },
  
  // 채팅 내용 지우기 (서버)
  async clearChatMessages(chatId) {
    try {
      await chatApi.clearMessages(chatId)
      
      // 로컬 캐시 업데이트
      const chat = this.getChat(chatId)
      if (chat) {
        chat.messages = []
        // 최근 메시지 정보 초기화 제거 (성능 개선)
      }
    } catch (error) {
      console.error('채팅 메시지 클리어 실패:', error)
      throw error
    }
  },

  // 로그아웃 시 채팅 상태 초기화
  clearAllData() {
    this.chats = []
    this.activeChat = null
    
    // localStorage에서도 제거
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('activeChat')
      }
    } catch (error) {
      console.error('채팅 데이터 삭제 중 오류:', error)
    }
  }
})

// 활성 채팅 변경 감지 및 자동 저장
watch(() => chatStore.activeChat, () => {
  chatStore.saveActiveToStorage()
})

export default chatStore