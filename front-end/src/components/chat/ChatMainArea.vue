<template>
  <div class="chat-main-area">
    <!-- 채팅이 선택되지 않은 경우 -->
    <div v-if="!props.activeChat" class="welcome-screen">
      <!-- 로그인된 사용자용 환영 화면 -->
      <div v-if="props.isLoggedIn" class="empty-chat-wrapper">
        <EmptyChat 
          @open-new-chat-modal="handleOpenNewChatModal"
          @load-recent-chats="handleLoadRecentChats"
        />
      </div>
      
      <!-- 비로그인 사용자용 전체 스크롤 랜딩 페이지 -->
      <div v-else class="landing-page">
        <!-- Hero Section -->
        <section class="hero-section">
          <div class="hero-container">
            <div class="hero-content">
              <h1 class="hero-title">
                다양한 AI 모델을
                <span class="gradient-text">PolyMind</span>에서 사용하세요
              </h1>
              <p class="hero-description">
                Claude, GPT, Gemini 등 주요 AI 모델들을 하나의 플랫폼에서 편리하게 사용할 수 있습니다.
                업무 효율성과 창의적 작업을 향상시켜보세요.
              </p>
              <div class="hero-actions">
                <router-link to="/signup" class="primary-cta">
                  <span>무료로 시작하기</span>
                  <i class="fas fa-arrow-right"></i>
                </router-link>
                <router-link to="/login" class="secondary-cta">
                  로그인
                </router-link>
              </div>
              <div class="hero-stats">
                <div class="stat-item">
                  <span class="stat-number">5+</span>
                  <span class="stat-label">AI 모델</span>
                </div>
                <div class="stat-item">
                  <span class="stat-number">편리한</span>
                  <span class="stat-label">통합 관리</span>
                </div>
                <div class="stat-item">
                  <span class="stat-number">안전한</span>
                  <span class="stat-label">데이터 보호</span>
                </div>
              </div>
            </div>
            <div class="hero-visual">
              <div class="floating-card card-1">
                <div class="card-header">
                  <div class="ai-badge claude">Claude</div>
                  <span class="card-title">창작 도우미</span>
                </div>
                <p class="card-content">소설 줄거리를 작성해주세요...</p>
              </div>
              <div class="floating-card card-2">
                <div class="card-header">
                  <div class="ai-badge gpt">GPT-4</div>
                  <span class="card-title">코딩 어시스턴트</span>
                </div>
                <p class="card-content">React 컴포넌트를 최적화하는 방법...</p>
              </div>
              <div class="floating-card card-3">
                <div class="card-header">
                  <div class="ai-badge gemini">Gemini</div>
                  <span class="card-title">분석 전문가</span>
                </div>
                <p class="card-content">이 차트 데이터를 해석해주세요...</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Features Section -->
        <section class="features-section">
          <div class="section-container">
            <div class="section-header">
              <h2 class="section-title">주요 기능</h2>
              <p class="section-subtitle">AI 모델 사용을 위한 필수 도구들</p>
            </div>
            <div class="features-grid">
              <div class="feature-card">
                <div class="feature-icon ai-models">
                  <i class="fas fa-brain"></i>
                </div>
                <h3>다양한 AI 모델</h3>
                <p>Claude, GPT, Gemini 등 주요 AI 모델들을 편리하게 전환하며 사용할 수 있습니다</p>
              </div>
              <div class="feature-card">
                <div class="feature-icon smart-chat">
                  <i class="fas fa-comments-dollar"></i>
                </div>
                <h3>대화 기록 관리</h3>
                <p>대화 내용을 체계적으로 저장하고 필요할 때 쉽게 찾아볼 수 있습니다</p>
              </div>
              <div class="feature-card">
                <div class="feature-icon customization">
                  <i class="fas fa-sliders-h"></i>
                </div>
                <h3>모델 설정 조정</h3>
                <p>Temperature, 토큰 수 등 AI 모델의 파라미터를 조정할 수 있습니다</p>
              </div>
              <div class="feature-card">
                <div class="feature-icon multimodal">
                  <i class="fas fa-image"></i>
                </div>
                <h3>파일 업로드</h3>
                <p>텍스트, 이미지, 문서 등 다양한 형태의 파일을 AI에 업로드할 수 있습니다</p>
              </div>
              <div class="feature-card">
                <div class="feature-icon export">
                  <i class="fas fa-download"></i>
                </div>
                <h3>대화 내보내기</h3>
                <p>중요한 대화 내용을 텍스트 파일로 내보내어 보관할 수 있습니다</p>
              </div>
              <div class="feature-card">
                <div class="feature-icon security">
                  <i class="fas fa-shield-alt"></i>
                </div>
                <h3>데이터 보안</h3>
                <p>사용자 데이터는 암호화되어 안전하게 보호됩니다</p>
              </div>
            </div>
          </div>
        </section>

        <!-- AI Models Section -->
        <section class="models-section">
          <div class="section-container">
            <div class="section-header">
              <h2 class="section-title">지원하는 AI 모델</h2>
              <p class="section-subtitle">각각의 특징을 가진 AI 모델을 상황에 맞게 선택하세요</p>
            </div>
            <div class="models-grid">
              <div class="model-card claude">
                <div class="model-header">
                  <div class="model-logo">
                    <i class="fas fa-brain"></i>
                  </div>
                  <h3>Claude</h3>
                  <span class="model-provider">by Anthropic</span>
                </div>
                <ul class="model-features">
                  <li>창작 및 분석에 특화</li>
                  <li>긴 문맥 이해 능력</li>
                  <li>윤리적이고 안전한 답변</li>
                </ul>
              </div>
              <div class="model-card gpt">
                <div class="model-header">
                  <div class="model-logo">
                    <i class="fas fa-robot"></i>
                  </div>
                  <h3>GPT-4</h3>
                  <span class="model-provider">by OpenAI</span>
                </div>
                <ul class="model-features">
                  <li>범용적인 문제 해결</li>
                  <li>코딩 및 기술 지원</li>
                  <li>창의적 사고 능력</li>
                </ul>
              </div>
              <div class="model-card gemini">
                <div class="model-header">
                  <div class="model-logo">
                    <i class="fas fa-gem"></i>
                  </div>
                  <h3>Gemini</h3>
                  <span class="model-provider">by Google</span>
                </div>
                <ul class="model-features">
                  <li>멀티모달 이해 능력</li>
                  <li>실시간 정보 접근</li>
                  <li>빠른 응답 속도</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <!-- CTA Section -->
        <section class="final-cta-section">
          <div class="section-container">
            <div class="cta-content">
              <h2 class="cta-title">지금 바로 시작해보세요</h2>
              <p class="cta-description">
                간단한 회원가입 후 다양한 AI 모델들을 사용할 수 있습니다.
                무료 플랜으로 먼저 체험해보세요.
              </p>
              <div class="cta-actions">
                <router-link to="/signup" class="primary-cta large">
                  <span>무료로 시작하기</span>
                  <i class="fas fa-rocket"></i>
                </router-link>
              </div>
              <p class="cta-note">신용카드 등록 불필요 • 언제든 업그레이드 가능</p>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- 채팅이 선택된 경우 -->
    <div v-else-if="props.activeChat" class="chat-container">
      <div class="chat-header">
        <div class="chat-title-section">
          <h3>{{ currentChatTitle }}</h3>
          <div v-if="currentChatModelInfo" class="chat-header-model-info">
            <span class="header-model-api">{{ currentChatModelInfo.apiName }}</span>
            <span class="header-model-name">{{ currentChatModelInfo.model }}</span>
          </div>
        </div>
        <div class="chat-actions">
          <button class="action-btn" @click="openChatSettings">
            <i class="fas fa-cog"></i>
          </button>
          <button class="action-btn" @click="deleteChat">
            <i class="fas fa-trash"></i>
          </button>
          <button class="action-btn" @click="exportChat">
            <i class="fas fa-download"></i>
          </button>
        </div>
      </div>
      
      <div 
        class="chat-messages" 
        ref="messagesContainer" 
        @scroll="handleScroll"
      >
        <!-- 무한 스크롤 트리거 (메시지 상단) -->
        <div 
          v-if="hasMoreMessages" 
          ref="loadTrigger" 
          class="load-trigger"
          style="height: 1px; width: 100%;"
        ></div>
        
        <div v-if="isLoadingMessages" class="loading-indicator">
          <div class="loading-spinner"></div>
          <span>이전 메시지 로딩 중...</span>
        </div>
        
        <div 
          v-for="message in messages" 
          :key="message.id"
          v-memo="[message.id, message.text, message.sender, message.images]"
          class="message"
          :class="{ 'user-message': message.sender === 'user', 'ai-message': message.sender === 'ai' }"
        >
          <div class="message-content">
            <!-- 이미지가 있는 경우 표시 -->
            <div v-if="message.images && message.images.length > 0" class="message-images">
              <div 
                v-for="image in message.images" 
                :key="image.filename"
                class="message-image-item"
              >
                <button 
                  class="image-thumbnail-container" 
                  @click="openImageModal(image)"
                  type="button"
                  :aria-label="`이미지 ${image.originalName} 크게 보기`"
                >
                  <img 
                    :src="image.preview || image.url" 
                    :alt="image.originalName"
                    class="message-image"
                  />
                  <div class="image-overlay">
                    <i class="fas fa-search-plus" aria-hidden="true"></i>
                  </div>
                </button>
                <div class="image-filename">{{ image.originalName }}</div>
              </div>
            </div>
            <!-- 텍스트 메시지 -->
            <div v-if="message.text" class="message-text">
              <SimpleMarkdownRenderer :content="message.text" />
            </div>
          </div>
        </div>
        
        <!-- AI 응답 대기 중 타이핑 인디케이터 -->
        <div v-if="isWaitingForResponse" class="typing-indicator">
          <div class="message ai-message">
            <div class="message-content typing-content">
              <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span class="typing-text">응답 중...</span>
            </div>
          </div>
        </div>
        
      </div>

      <!-- 이미지 미리보기 영역 (입력창 위에 배치) -->
      <div v-if="selectedImages.length > 0" class="image-preview-container">
        <div class="image-preview-wrapper">
          <div 
            v-for="image in selectedImages" 
            :key="image.id"
            class="image-preview-card"
          >
            <div class="image-container">
              <img :src="image.preview" :alt="image.name" class="preview-image" />
              <button 
                @click="removeImage(image.id)"
                class="remove-image-btn"
                title="이미지 제거"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div class="image-details">
              <span class="image-name">{{ image.name }}</span>
              <span class="image-size">{{ formatFileSize(image.size) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <!-- 최근 메시지로 이동 버튼 (채팅 입력창 위에 투명 오버레이) -->
        <button 
          v-if="shouldShowScrollButton"
          class="scroll-to-bottom-btn-floating"
          @click="scrollToBottom"
          type="button"
          aria-label="최근 메시지로 이동"
        >
          <i class="fas fa-chevron-down" aria-hidden="true"></i>
          <span>최근 메시지로 이동</span>
        </button>
        
        <div class="input-container">
          <button 
            @click="uploadFile"
            class="upload-btn-left"
            title="이미지 업로드"
          >
            <i class="fas fa-plus"></i>
          </button>
          
          <div class="input-wrapper">
            <textarea 
              v-model="inputMessage"
              @keydown.enter.prevent="sendMessage"
              placeholder="무엇이든 물어보세요"
              class="message-input"
              rows="1"
            ></textarea>
          </div>
          
          <div class="input-actions-right">
            <button 
              @click="sendMessage"
              :disabled="!inputMessage.trim() && selectedImages.length === 0"
              class="send-btn"
              title="메시지 전송"
            >
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 삭제 확인 모달 -->
  <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>채팅 삭제</h3>
        <button class="modal-close" @click="closeDeleteModal">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="modal-body">
        <p>정말로 이 채팅을 삭제하시겠습니까?</p>
        <p class="modal-warning">삭제된 채팅은 복구할 수 없습니다.</p>
      </div>
      <div class="modal-footer">
        <button class="modal-btn cancel-btn" @click="closeDeleteModal">
          취소
        </button>
        <button class="modal-btn delete-btn" @click="confirmDelete">
          삭제
        </button>
      </div>
    </div>
  </div>

  <!-- 이미지 모달 -->
  <div v-if="showImageModal && modalImage" class="image-modal-overlay" @click="closeImageModal">
    <!-- 닫기 버튼 (외부) -->
    <button class="image-modal-close-external" @click="closeImageModal">
      <i class="fas fa-times"></i>
    </button>
    
    <!-- 이미지 컨테이너 -->
    <div class="image-modal-content" @click.stop>
      <img 
        :src="modalImage.preview || modalImage.url" 
        :alt="modalImage.originalName"
        class="modal-image"
      />
    </div>
  </div>


</template>

<script setup>
import { ref, computed, nextTick, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLoadingStore } from '@/store/loading'
import chatStore from '@/store/chatStore'
import { chatApi } from '@/apis/chatApi'
import { aiApi } from '@/apis/aiApi'
import { getApiFromModel, MODEL_SETTINGS } from '@/config/modelSettings'
import EmptyChat from '@/components/chat/EmptyChat.vue'
import SimpleMarkdownRenderer from '@/components/common/SimpleMarkdownRenderer.vue'
import { throttle, debounce } from '@/utils/performance'

const router = useRouter()
const loadingStore = useLoadingStore()

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

const emit = defineEmits(['newChatStarted', 'messageSent', 'chatDeleted', 'openSettings', 'chatSelected', 'request-new-chat'])

const inputMessage = ref('')
const messagesContainer = ref(null)
// 메시지 로딩 상태는 전역 스토어에서 가져옴
const isLoadingMessages = computed(() => loadingStore.isOperationLoading('chat-load-messages'))
const waitingChats = ref(new Set()) // 응답 대기 중인 채팅 ID들의 Set
const hasMoreMessages = ref(true)
const currentPage = ref(1)
const messagesPerPage = 20
const showDeleteModal = ref(false)
const selectedImages = ref([])
const fileInputRef = ref(null)
const showImageModal = ref(false)
const modalImage = ref(null)
const isUserScrolling = ref(false) // 사용자가 스크롤 중인지 추적

// 현재 채팅방에서 응답을 기다리고 있는지 확인
const isWaitingForResponse = computed(() => {
  return waitingChats.value.has(props.activeChat)
})

// 채팅 목록 확인
const hasAnyChats = computed(() => {
  return chatStore.chats.length > 0
})

// 현재 채팅의 메시지들
const messages = computed(() => {
  if (!props.activeChat) {
    return []
  }
  
  const chat = chatStore.getChat(props.activeChat)
  const rawMessages = chat ? (chat.messages || []) : []
  
  // 메시지를 message_order 오름차순으로 정렬 (오래된 메시지가 위로, 최신 메시지가 아래로)
  // 서버에서 이미 정렬된 상태지만, 로컬에서 추가된 메시지 때문에 안전장치로 정렬 수행
  const sortedMessages = [...rawMessages].sort((a, b) => {
    const orderA = a.message_order || 0
    const orderB = b.message_order || 0
    
    // message_order가 다르면 message_order로 정렬
    if (orderA !== orderB) {
      return orderA - orderB  // 오름차순 정렬 (작은 번호가 위로)
    }
    
    // message_order가 같으면 id로 정렬 (더 안정적)
    const idA = a.id || 0
    const idB = b.id || 0
    if (idA !== idB) {
      return idA - idB
    }
    
    // 마지막으로 timestamp로 정렬
    const timeA = new Date(a.timestamp || a.created_at || 0)
    const timeB = new Date(b.timestamp || b.created_at || 0)
    return timeA - timeB
  })
  
  // 메시지의 이미지 데이터 처리 (데이터베이스에서 온 Base64 이미지를 data URL로 변환)
  const processedMessages = sortedMessages.map(message => {
    if (message.images && message.images.length > 0) {
      const processedImages = message.images.map(image => {
        // 이미 preview가 있는 경우 (로컬에서 추가된 메시지)
        if (image.preview) {
          return image
        }
        // 데이터베이스에서 온 이미지 (Base64 data가 있는 경우)
        if (image.data) {
          return {
            ...image,
            preview: `data:${image.content_type};base64,${image.data}`,
            originalName: image.filename,
            url: `data:${image.content_type};base64,${image.data}`
          }
        }
        return image
      })
      return {
        ...message,
        images: processedImages
      }
    }
    return message
  })
  
  return processedMessages
})

const currentChatTitle = computed(() => {
  if (!props.activeChat) return ''
  const chat = chatStore.getChat(props.activeChat)
  return chat ? chat.title : ''
})

const currentChatModelInfo = computed(() => {
  if (!props.activeChat) return null
  const chat = chatStore.getChat(props.activeChat)
  if (!chat) return null
  
  
  // 채팅에서 모델 정보 가져오기 (백엔드에서는 model 필드로 저장됨)
  const modelKey = chat.model || 'claude-3-sonnet'
  const apiKey = getApiFromModel(modelKey)
  const apiName = MODEL_SETTINGS[apiKey]?.name || 'Unknown'
  
  // 모델 이름 가져오기
  const modelName = MODEL_SETTINGS[apiKey]?.models[modelKey]?.name || modelKey
  
  
  return {
    apiName: apiName,
    model: modelName
  }
})

// Provider에서 API 이름 추출
const getApiNameFromProvider = (provider) => {
  const providerNames = {
    'openai': 'OpenAI',
    'anthropic': 'Claude',
    'google': 'Gemini'
  }
  return providerNames[provider] || 'AI'
}

const startNewChat = () => {
  emit('newChatStarted')
}

const handleOpenNewChatModal = () => {
  emit('request-new-chat')
}

const handleLoadRecentChats = () => {
  // 최근 채팅을 불러오는 로직
  // 여기서는 첫 번째 채팅을 선택하는 것으로 구현
  if (hasAnyChats.value) {
    const firstChatId = chatStore.chats[0].id
    emit('chatSelected', firstChatId)
  }
}

// 🚀 성능 최적화: 메시지 전송을 debounce로 중복 방지
const sendMessageCore = async () => {
  if ((!inputMessage.value.trim() && selectedImages.value.length === 0) || !props.activeChat) return
  
  const messageText = inputMessage.value
  const currentChatId = props.activeChat
  const imagesToSend = [...selectedImages.value]
  
  // 입력 필드와 이미지 초기화
  inputMessage.value = ''
  selectedImages.value = []
  waitingChats.value.add(currentChatId)
  
  try {
    // 이미지 데이터 준비 (원본 File 객체 우선 사용)
    const imageData = imagesToSend.map(img => {
      // 파일 크기 확인 (10MB 제한)
      if (img.size > 10 * 1024 * 1024) {
        console.warn(`[FRONTEND] Image ${img.name} is too large (${Math.round(img.size / 1024 / 1024)}MB), skipping`);
        return null;
      }
      
      return {
        filename: img.name,
        content_type: img.type,
        size: img.size,
        originalFile: img.file, // 원본 File 객체 전달 (FormData용)
        data: img.preview && img.preview.includes(',') ? img.preview.split(',')[1] : null // 항상 Base64 데이터 제공 (JSON용)
      };
    }).filter(Boolean); // null 값 제거
    
    // 로컬 스토어에 사용자 메시지 추가 (이미지 정보 포함)
    const userMessage = {
      sender: 'user',
      text: messageText,
      timestamp: new Date().toISOString(),
      images: imagesToSend.map(img => ({
        filename: img.name,
        originalName: img.name,
        preview: img.preview,
        size: img.size
      }))
    }
    
    chatStore.addMessage(currentChatId, userMessage)
    
    emit('messageSent', { text: messageText, images: imageData })
    
    // 메시지 전송 후 스크롤을 맨 아래로
    nextTick(() => {
      scrollToBottom()
    })
    
    // 현재 채팅 정보 가져오기 (원래 메시지를 보낸 채팅방)
    const chat = chatStore.getChat(currentChatId)
    const selectedModel = chat?.selectedModel || chat?.model || 'claude-3-sonnet'
    
    // 모델에서 provider 추출
    const provider = getApiFromModel(selectedModel) || 'anthropic'
    
    // API 키 상태 확인
    try {
      const providers = await aiApi.getAvailableProviders()
      
      if (!providers.available_providers.includes(provider)) {
        const providerNames = {
          'openai': 'OpenAI',
          'anthropic': 'Claude (Anthropic)', 
          'google': 'Gemini (Google)'
        }
        const providerName = providerNames[provider] || provider
        throw new Error(`${providerName} API 키가 설정되지 않았습니다.\n\n설정 → API 키 관리에서 ${providerName} API 키를 등록해주세요.`)
      }
    } catch (keyError) {
      if (keyError.message.includes('API 키가 설정되지 않았습니다')) {
        throw keyError
      }
      throw new Error(`API 키 확인 실패: ${keyError.message}`)
    }
    
    // AI 응답 생성 요청 (이미지 데이터 포함)
    
    const requestData = {
      chat_id: currentChatId,
      message: messageText,
      images: imageData.length > 0 ? imageData : null,
      provider: provider,
      model: selectedModel,
      max_tokens: chat?.max_tokens || chat?.maxTokens || 1000,
      temperature: chat?.temperature || 0.7,
      system_prompt: chat?.system_prompt || chat?.systemPrompt,
      include_history: true
    }
    
    
    // 항상 스트리밍 모드 사용
    
    // AI 메시지 ID 미리 생성 (실제 메시지는 첫 번째 청크에서 추가)
    const aiMessageId = Date.now() + Math.random()
    let messageAdded = false
    
    // 스트리밍으로 AI 응답 요청
    aiApi.generateChatResponseStream(
      requestData,
      // onChunk - 실시간으로 텍스트 업데이트
      (chunk, fullContent) => {
        // 첫 번째 청크를 받으면 AI 메시지 추가하고 "응답 중..." 표시기 제거
        if (!messageAdded && fullContent.length > 0) {
          chatStore.addMessage(currentChatId, {
            id: aiMessageId,
            sender: 'ai',
            text: fullContent,
            timestamp: new Date().toISOString(),
            model: requestData.model,
            apiName: getApiNameFromProvider(provider),
            isStreaming: true
          })
          messageAdded = true
          waitingChats.value.delete(currentChatId)
        } else if (messageAdded) {
          // 이후 청크들은 기존 메시지 업데이트
          chatStore.updateMessage(currentChatId, aiMessageId, {
            text: fullContent,
            isStreaming: true
          })
        }
        
        // 현재 활성 채팅방이면 스크롤 유지
        if (currentChatId === props.activeChat) {
          nextTick(() => {
            scrollToBottom()
          })
        }
      },
      // onComplete - 스트리밍 완료
      (finalContent) => {
        
        if (messageAdded) {
          chatStore.updateMessage(currentChatId, aiMessageId, {
            text: finalContent,
            isStreaming: false
          })
        } else if (finalContent) {
          // 메시지가 추가되지 않았지만 최종 내용이 있는 경우
          chatStore.addMessage(currentChatId, {
            id: aiMessageId,
            sender: 'ai',
            text: finalContent,
            timestamp: new Date().toISOString(),
            model: requestData.model,
            apiName: getApiNameFromProvider(provider),
            isStreaming: false
          })
        }
        
        if (currentChatId === props.activeChat) {
          nextTick(() => {
            scrollToBottom()
          })
        }
        
        // 응답 완료된 채팅방을 대기 목록에서 제거
        waitingChats.value.delete(currentChatId)
      },
      // onError - 에러 처리
      (error) => {
        console.error('[FRONTEND] Streaming error for chat:', currentChatId, error)
        
        const errorText = `❌ ${error.message || '스트리밍 오류가 발생했습니다.'}`
        
        if (messageAdded) {
          chatStore.updateMessage(currentChatId, aiMessageId, {
            text: errorText,
            isError: true,
            isStreaming: false
          })
        } else {
          // 메시지가 추가되지 않은 경우 새로 추가
          chatStore.addMessage(currentChatId, {
            id: aiMessageId,
            sender: 'ai',
            text: errorText,
            timestamp: new Date().toISOString(),
            model: requestData.model,
            apiName: getApiNameFromProvider(provider),
            isError: true,
            isStreaming: false
          })
        }
        
        if (currentChatId === props.activeChat) {
          nextTick(() => {
            scrollToBottom()
          })
        }
        
        waitingChats.value.delete(currentChatId)
      }
    )
    
  } catch (error) {
    // API 키 체크나 기본 설정 오류는 즉시 처리
    console.error('설정 오류:', error)
    let errorMessage = error.message || '설정 오류가 발생했습니다.'
    
    chatStore.addMessage(currentChatId, {
      sender: 'ai',
      text: `❌ ${errorMessage}`,
      isError: true,
      timestamp: new Date().toISOString()
    })
    
    if (currentChatId === props.activeChat) {
      nextTick(() => {
        scrollToBottom()
      })
    }
    
    // 설정 오류 시에도 대기 목록에서 제거
    waitingChats.value.delete(currentChatId)
  }
}

// 🚀 성능 최적화: 중복 전송 방지를 위한 debounce (300ms)
const sendMessage = debounce(sendMessageCore, 300)

const uploadFile = () => {
  const fileInput = document.createElement('input')
  fileInput.type = 'file'
  fileInput.accept = 'image/*'
  fileInput.multiple = true
  fileInput.onchange = (event) => {
    const files = Array.from(event.target.files)
    handleImageSelection(files)
  }
  fileInput.click()
}

const handleImageSelection = (files) => {
  files.forEach(file => {
    if (file.type.startsWith('image/')) {
      // 이미지 파일 크기 제한 (5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('이미지 파일 크기는 5MB 이하여야 합니다.')
        return
      }
      
      const reader = new FileReader()
      reader.onload = (e) => {
        const imageData = {
          id: Date.now() + Math.random(),
          file: file,
          name: file.name,
          size: file.size,
          type: file.type,
          preview: e.target.result
        }
        selectedImages.value.push(imageData)
      }
      reader.readAsDataURL(file)
    }
  })
}

const removeImage = (imageId) => {
  selectedImages.value = selectedImages.value.filter(img => img.id !== imageId)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const openImageModal = (image) => {
  modalImage.value = image
  showImageModal.value = true
}

const closeImageModal = () => {
  showImageModal.value = false
  modalImage.value = null
}


const deleteChat = () => {
  if (props.activeChat) {
    showDeleteModal.value = true
  }
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
}

// Escape 키로 모달 닫기
const handleEscapeKey = (event) => {
  if (event.key === 'Escape') {
    if (showImageModal.value) {
      closeImageModal()
    } else if (showDeleteModal.value) {
      closeDeleteModal()
    }
  }
}

const confirmDelete = () => {
  if (props.activeChat) {
    // 부모 컴포넌트에 삭제 요청 전달 (실제 삭제는 HomeView에서 처리)
    emit('chatDeleted', props.activeChat)
  }
  showDeleteModal.value = false
}


const openChatSettings = () => {
  if (props.activeChat) {
    emit('openSettings', props.activeChat)
  }
}


const exportChat = () => {
  if (!props.activeChat) return
  
  const chat = chatStore.getChat(props.activeChat)
  if (!chat) return
  
  // 채팅 내용을 텍스트 파일로 내보내기
  const chatContent = chat.messages.map(msg => 
    `${msg.sender === 'user' ? '사용자' : 'AI'}: ${msg.text}`
  ).join('\n')
  
  const blob = new Blob([chatContent], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${chat.title}.txt`
  a.click()
  URL.revokeObjectURL(url)
}


const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    // 스크롤 후 상태 업데이트
    nextTick(() => {
      isAtBottomState.value = true
      scrollUpState.value = false
    })
  }
}

// IntersectionObserver를 사용한 무한 스크롤
const intersectionObserver = ref(null)
const loadTrigger = ref(null)

const setupInfiniteScroll = () => {
  if (!loadTrigger.value) return
  
  intersectionObserver.value = new IntersectionObserver(
    (entries) => {
      const entry = entries[0]
      if (entry.isIntersecting && hasMoreMessages.value && !isLoadingMessages.value) {
        loadMoreMessages()
      }
    },
    {
      root: messagesContainer.value,
      rootMargin: '50px',
      threshold: 0.1
    }
  )
  
  intersectionObserver.value.observe(loadTrigger.value)
}

const cleanupInfiniteScroll = () => {
  if (intersectionObserver.value) {
    intersectionObserver.value.disconnect()
    intersectionObserver.value = null
  }
}

const loadMoreMessages = async () => {
  if (isLoadingMessages.value || !hasMoreMessages.value || !props.activeChat) return
  
  loadingStore.startOperation('chat-load-messages', '이전 메시지 로딩 중...')
  
  try {
    // 현재 스크롤 위치 저장
    const currentScrollHeight = messagesContainer.value.scrollHeight
    const currentScrollTop = messagesContainer.value.scrollTop
    
    // 실제 API 호출로 이전 메시지 로드
    const chat = chatStore.getChat(props.activeChat)
    if (chat) {
      const currentMessageCount = chat.messages.length
      const limit = messagesPerPage
      const offset = currentMessageCount
      
      // 백엔드에서 페이지네이션된 메시지 가져오기
      const response = await chatApi.getMessages(props.activeChat, { limit, offset })
      
      if (response.data && response.data.length > 0) {
        // 기존 메시지 앞에 추가 (순서대로)
        const olderMessages = response.data.map(msg => ({
          id: msg.id,
          sender: msg.sender,
          text: msg.content,
          timestamp: msg.created_at,
          images: msg.images || [], // 이미지 데이터 포함
          ...(msg.sender === 'ai' && { 
            apiName: msg.api_provider === 'openai' ? 'OpenAI' : 
                     msg.api_provider === 'anthropic' ? 'Claude' : 
                     msg.api_provider === 'google' ? 'Gemini' : 'AI', 
            model: msg.model_name 
          })
        }))
        olderMessages.forEach(msg => {
          chat.messages.unshift(msg)
        })
        
        currentPage.value++
        
        // 스크롤 위치 복원
        nextTick(() => {
          const newScrollHeight = messagesContainer.value.scrollHeight
          const scrollDifference = newScrollHeight - currentScrollHeight
          messagesContainer.value.scrollTop = currentScrollTop + scrollDifference
        })
        
        // 더 가져올 메시지가 없으면 hasMoreMessages를 false로 설정
        if (response.data.length < limit) {
          hasMoreMessages.value = false
        }
      } else {
        hasMoreMessages.value = false
      }
    }
  } catch (error) {
    console.error('메시지 로드 중 오류:', error)
    hasMoreMessages.value = false
  } finally {
    loadingStore.stopOperation('chat-load-messages')
  }
}


// activeChat가 변경될 때마다 초기화 및 메시지 로드
watch(() => props.activeChat, async (newChatId, oldChatId) => {
  
  if (newChatId && newChatId !== oldChatId) {
    currentPage.value = 1
    hasMoreMessages.value = true
    
    // 다른 채팅방으로 이동할 때는 인디케이터를 유지 (응답 대기 중인 채팅방이 따로 있을 수 있음)
    // 인디케이터는 computed에서 현재 채팅방과 대기 중인 채팅방을 비교하여 표시
    
    // 채팅 메시지 로드
    try {
      const chat = chatStore.getChat(newChatId)
      if (!chat || !chat.messages || chat.messages.length === 0) {
        await chatStore.loadChatWithMessages(newChatId)
      }
      
      // 메시지 로드 후 스크롤을 하단으로 이동
      nextTick(() => {
        scrollToBottom()
        isAtBottomState.value = true
        scrollUpState.value = false
      })
    } catch (error) {
      console.error('ChatMainArea: 메시지 로드 실패:', error)
    }
    
    nextTick(() => {
      scrollToBottom()
      isAtBottomState.value = true // 채팅 변경 시 하단 상태로 초기화
      scrollUpState.value = false // 스크롤 상태도 초기화
      // IntersectionObserver 설정
      setTimeout(() => {
        setupInfiniteScroll()
      }, 100)
    })
  } else {
    // 채팅이 변경되지 않을 때는 기존 observer 정리
    cleanupInfiniteScroll()
  }
})

// 스크롤 이벤트 핸들러
// 🚀 성능 최적화: 스크롤 이벤트를 throttle로 최적화
const handleScrollCore = () => {
  isUserScrolling.value = true
  // 스크롤 위치 상태 업데이트
  isAtBottomState.value = isAtBottom()
  scrollUpState.value = hasScrolledUp()
  
  // 스크롤이 멈춘 후 일정 시간 후에 사용자 스크롤 상태 해제
  clearTimeout(handleScrollCore.timeout)
  handleScrollCore.timeout = setTimeout(() => {
    isUserScrolling.value = false
  }, 150)
}

const handleScroll = throttle(handleScrollCore, 16) // 60fps로 제한

// 사용자가 스크롤 최하단에 있는지 확인하는 반응형 computed
const isAtBottomState = ref(true)
const scrollUpState = ref(false) // 일정 높이 이상 스크롤했는지 상태

const isAtBottom = () => {
  if (!messagesContainer.value) return true
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  const distanceFromBottom = scrollHeight - scrollTop - clientHeight
  
  // 컨텐츠가 화면보다 작으면 (스크롤이 없으면) true 반환
  if (scrollHeight <= clientHeight) return true
  
  // 실제로 하단 근처에 있을 때만 true 반환
  const isNearBottom = distanceFromBottom < 50
  const isActuallyAtBottom = scrollTop >= scrollHeight - clientHeight - 50
  
  return isNearBottom && isActuallyAtBottom
}

// 스크롤이 일정 높이 이상 올라갔는지 확인하는 함수
const hasScrolledUp = () => {
  if (!messagesContainer.value) return false
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  
  // 컨텐츠가 화면보다 작으면 버튼 표시 안함
  if (scrollHeight <= clientHeight) return false
  
  const distanceFromBottom = scrollHeight - scrollTop - clientHeight
  
  // 하단에서 800px 이상 떨어져 있을 때 버튼 표시
  // 최상단일 때는 distanceFromBottom이 크므로 버튼이 표시됨
  return distanceFromBottom > 800
}

// 스크롤 상태를 추적하는 computed
const shouldShowScrollButton = computed(() => {
  // 일정 높이 이상 스크롤했고, 채팅이 활성화되어 있을 때 표시 (로딩 상태와 무관하게)
  return scrollUpState.value && 
         props.activeChat && 
         messagesContainer.value
})

// 메시지가 변경될 때 스크롤 처리 (새 메시지만 자동 스크롤)
watch(messages, (newMessages, oldMessages) => {
  if (!oldMessages || oldMessages.length === 0) {
    // 초기 로드 시에는 최하단으로 스크롤
    nextTick(() => {
      scrollToBottom()
      isAtBottomState.value = true
      scrollUpState.value = false
    })
  } else if (newMessages.length > oldMessages.length && !isLoadingMessages.value) {
    // 새 메시지가 추가되었고, 인피니티 스크롤 중이 아닐 때
    // 사용자가 최하단 근처에 있을 때만 자동 스크롤
    if (isAtBottomState.value) {
      nextTick(() => {
        scrollToBottom()
        isAtBottomState.value = true
        scrollUpState.value = false
      })
    }
  }
}, { deep: true, immediate: true })

// 컴포넌트 언마운트 시 observer 정리
// 키보드 이벤트 리스너 설정
onMounted(async () => {
  document.addEventListener('keydown', handleEscapeKey)
  
  // 페이지 새로고침 후 activeChat이 이미 설정되어 있는 경우 메시지 로드
  // chatStore 초기화가 완료될 때까지 약간 대기
  setTimeout(async () => {
    if (props.activeChat) {
      try {
        const chat = chatStore.getChat(props.activeChat)
        if (!chat || !chat.messages || chat.messages.length === 0) {
          await chatStore.loadChatWithMessages(props.activeChat)
          
          // 메시지 로드 후 스크롤을 하단으로
          nextTick(() => {
            scrollToBottom()
          })
        } else {
          // 이미 메시지가 있는 경우에도 스크롤을 하단으로
          nextTick(() => {
            scrollToBottom()
          })
        }
      } catch (error) {
        console.error('ChatMainArea: onMounted setTimeout에서 메시지 로드 실패:', error)
      }
    }
  }, 100)
})

onUnmounted(() => {
  cleanupInfiniteScroll()
  document.removeEventListener('keydown', handleEscapeKey)
})
</script>

<style scoped>
.chat-main-area {
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
}

.welcome-screen {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: transparent;
}

.empty-chat-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.welcome-content {
  text-align: center;
  max-width: 500px;
  padding: 60px 40px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.welcome-icon {
  font-size: 64px;
  color: #4299e1;
  margin-bottom: 24px;
}

.welcome-content h2 {
  color: #2d3748;
  margin-bottom: 16px;
  font-size: 28px;
  font-weight: 700;
}

.welcome-content p {
  color: #718096;
  margin-bottom: 32px;
  font-size: 16px;
  line-height: 1.6;
}

.start-new-chat-btn {
  padding: 16px 32px;
  background: #4299e1;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 auto;
  transition: background-color 0.2s ease;
}

.start-new-chat-btn:hover {
  background: #3182ce;
}

/* 랜딩 페이지 전체 컨테이너 */
.landing-page {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(180deg, #fafbff 0%, #f8fafc 100%);
  overflow-y: auto;
  padding: 0;
}

/* 섹션 공통 스타일 */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 64px;
}

.section-title {
  font-size: 48px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 16px;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 20px;
  color: #64748b;
  font-weight: 500;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

/* Hero Section */
.hero-section {
  padding: 80px 0 120px;
  position: relative;
  overflow: hidden;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.hero-content {
  z-index: var(--z-content);
}

.hero-title {
  font-size: 64px;
  font-weight: 900;
  line-height: 1.1;
  color: #1e293b;
  margin-bottom: 24px;
  letter-spacing: -0.02em;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-description {
  font-size: 20px;
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 40px;
  font-weight: 500;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
  align-items: center;
}

.primary-cta {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 32px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.4);
}

.primary-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.5);
}

.primary-cta.large {
  padding: 20px 40px;
  font-size: 18px;
}

.secondary-cta {
  color: #64748b;
  padding: 16px 32px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  background: white;
}

.secondary-cta:hover {
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

.hero-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.stat-number {
  font-size: 32px;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* Hero Visual */
.hero-visual {
  position: relative;
  height: 600px;
}

.floating-card {
  position: absolute;
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  max-width: 280px;
  animation: float 6s ease-in-out infinite;
}

.floating-card.card-1 {
  top: 0;
  right: 0;
  animation-delay: 0s;
}

.floating-card.card-2 {
  top: 200px;
  left: 0;
  animation-delay: 2s;
}

.floating-card.card-3 {
  bottom: 0;
  right: 40px;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.ai-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.ai-badge.claude { background: linear-gradient(135deg, #ff6b6b, #ee5a52); }
.ai-badge.gpt { background: linear-gradient(135deg, #4ecdc4, #44a08d); }
.ai-badge.gemini { background: linear-gradient(135deg, #667eea, #764ba2); }

.card-title {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.card-content {
  color: #64748b;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
}



.login-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #e2e8f0;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #4a5568;
  font-size: 14px;
  justify-content: center;
}

.feature-item i {
  color: #6366f1;
  font-size: 16px;
  width: 20px;
  text-align: center;
}

@media (max-width: 600px) {
  .login-required-content {
    padding: 40px 20px;
  }
  
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #ffffff;
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  border: none;
  overflow: hidden;
  min-width: 0;
}

.chat-header {
  padding: 12px 20px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.chat-title-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 18px;
  font-weight: 600;
}

.chat-header-model-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.header-model-api {
  font-size: 11px;
  font-weight: 600;
  color: #4338ca;
  background: #e0e7ff;
  padding: 3px 6px;
  border-radius: 4px;
  line-height: 1;
  min-width: 50px;
  text-align: center;
  display: inline-block;
}

.header-model-name {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  background: #f3f4f6;
  padding: 3px 6px;
  border-radius: 4px;
  line-height: 1;
  min-width: 50px;
  text-align: center;
  display: inline-block;
}

.chat-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 10px 14px;
  background: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  color: #4a5568;
  transition: background-color 0.2s ease;
  font-size: 16px;
  min-width: 44px;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #edf2f7;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  background: #f7fafc;
  position: relative;
  min-height: 0;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #edf2f7;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

.message {
  margin-bottom: 16px;
  display: flex;
}

.user-message {
  justify-content: flex-end;
}

.ai-message {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
}

.user-message .message-content {
  background: #f1f5f9;
  color: #1f2937;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.ai-message .message-content {
  background: #ffffff;
  color: #2d3748;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.message-text {
  line-height: 1.6;
  font-size: 14px;
  text-align: left;
  word-wrap: break-word;
  /* white-space: pre-wrap; 제거 - 마크다운 렌더러가 처리 */
}

/* 마크다운 렌더러 내부 스타일 조정 */
.message-text :deep(.markdown-renderer) {
  font-size: inherit;
  line-height: inherit;
}

/* AI 메시지와 사용자 메시지의 마크다운 스타일 구분 */
.ai-message .message-text :deep(.markdown-renderer) {
  color: #374151;
}

.user-message .message-text :deep(.markdown-renderer) {
  color: inherit;
}

.message-images {
  margin-bottom: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.message-image-item {
  display: flex;
  flex-direction: column;
  width: 120px;
  gap: 4px;
}

.image-thumbnail-container {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border: none;
  background: none;
  padding: 0;
  font-family: inherit;
}

.image-thumbnail-container:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.image-thumbnail-container:active {
  transform: scale(0.98);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
  color: white;
  font-size: 18px;
}

.image-thumbnail-container:hover .image-overlay,
.image-thumbnail-container:focus .image-overlay {
  opacity: 1;
}

.image-thumbnail-container:focus {
  outline: 2px solid #6366f1;
  outline-offset: 2px;
}

.message-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border: 1px solid #e2e8f0;
  background-color: #f8f9fa;
  display: block;
}

.image-filename {
  font-size: 10px;
  color: #6b7280;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 120px;
}

/* 이미지 모달 스타일 */
.image-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  background: oklab(0 none none/.9);
  z-index: var(--z-modal);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-modal-content {
  background: transparent;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.image-modal-close-external {
  position: fixed;
  top: 30px;
  right: 30px;
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  z-index: var(--z-popover);
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.image-modal-close-external:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: scale(1.1);
}

.modal-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 0px;
  box-shadow: none;
}

/* 최근 메시지로 이동 버튼 (채팅 입력창 상단 플로팅) */
.scroll-to-bottom-btn-floating {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(59, 130, 246, 0.95);
  color: white;
  border: none;
  border-radius: 30px;
  padding: 12px 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
  animation: fadeInCenter 0.3s ease;
  white-space: nowrap;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: var(--z-sidebar);
  pointer-events: auto;
  font-family: inherit;
}

.scroll-to-bottom-btn-floating:focus {
  outline: 2px solid #ffffff;
  outline-offset: 2px;
}

.scroll-to-bottom-btn-floating:hover {
  background: rgba(37, 99, 235, 0.98);
  transform: translateX(-50%) translateY(-3px);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
}

.scroll-to-bottom-btn-floating i {
  font-size: 12px;
}

.scroll-to-bottom-btn-overlay i {
  font-size: 12px;
}

/* 이전 버튼 스타일 (사용하지 않지만 호환성을 위해 유지) */
.scroll-to-bottom-btn {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  transition: all 0.2s ease;
  z-index: var(--z-dropdown);
  animation: fadeInUp 0.3s ease;
  white-space: nowrap;
}

.scroll-to-bottom-btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

.scroll-to-bottom-btn i {
  font-size: 12px;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInCenter {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}


.chat-input-area {
  padding: 12px 20px 16px 20px;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  position: relative;
  flex-shrink: 0;
}

/* 이미지 미리보기 컨테이너 */
.image-preview-container {
  padding: 12px 20px 8px 20px;
  background: #ffffff;
}

.image-preview-wrapper {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: flex-start;
}

.image-preview-card {
  position: relative;
  background: #ffffff;
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  max-width: 160px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.image-preview-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.image-container {
  position: relative;
  overflow: hidden;
}

.preview-image {
  width: 160px;
  height: 120px;
  object-fit: cover;
  display: block;
}

.remove-image-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: all 0.2s ease;
  opacity: 0.9;
}

.remove-image-btn:hover {
  background: rgba(239, 68, 68, 0.9);
  transform: scale(1.1);
  opacity: 1;
}

.image-details {
  padding: 12px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.image-name {
  font-size: 12px;
  color: #374151;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 136px;
  line-height: 1.2;
}

.image-size {
  font-size: 11px;
  color: #9ca3af;
  font-weight: 400;
}

/* 이미지 미리보기 반응형 */
@media (max-width: 768px) {
  .image-preview-container {
    padding: 12px 16px 6px 16px;
  }
  
  .image-preview-wrapper {
    gap: 8px;
  }
  
  .image-preview-card {
    max-width: 120px;
  }
  
  .preview-image {
    width: 120px;
    height: 90px;
  }
  
  .image-details {
    padding: 8px;
  }
  
  .image-name {
    font-size: 11px;
    max-width: 104px;
  }
  
  .image-size {
    font-size: 10px;
  }
  
  .remove-image-btn {
    width: 20px;
    height: 20px;
    top: 6px;
    right: 6px;
    font-size: 10px;
  }
}

.input-container {
  display: flex;
  align-items: center;
  gap: 12px;
  max-width: 100%;
}

.upload-btn-left {
  width: 44px;
  height: 44px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 16px;
  color: #6b7280;
  flex-shrink: 0;
}

.upload-btn-left:hover {
  background: #f1f5f9;
  border-color: #cbd5e0;
}

.input-wrapper {
  flex: 1;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  padding: 12px 20px;
  transition: all 0.2s ease;
  min-height: 48px;
  display: flex;
  align-items: center;
}

.input-wrapper:focus-within {
  border-color: #4338ca;
  border-width: 2px;
  box-shadow: 0 0 0 3px rgba(67, 56, 202, 0.2);
  background: #ffffff;
}

.message-input {
  flex: 1;
  border: none;
  background: transparent;
  resize: none;
  min-height: 20px;
  max-height: 120px;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.5;
  padding: 0;
}

.message-input:focus {
  outline: none;
}

.message-input::placeholder {
  color: #9ca3af;
}

.input-actions-right {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-shrink: 0;
}


.send-btn {
  width: 44px;
  height: 44px;
  background: #4338ca;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 16px;
}

.send-btn:hover:not(:disabled) {
  background: #3730a3;
}

.send-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  color: #9ca3af;
}

.streaming-toggle {
  width: 44px;
  height: 44px;
  border: 2px solid #e2e8f0;
  background: white;
  color: #64748b;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 16px;
  margin-right: 8px;
}

.streaming-toggle:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
  color: #475569;
}

.streaming-toggle.active {
  border-color: #22c55e;
  background: #22c55e;
  color: white;
}

.streaming-toggle.active:hover {
  border-color: #16a34a;
  background: #16a34a;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #6b7280;
  font-size: 14px;
  gap: 10px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #4338ca;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 타이핑 인디케이터 스타일 */
.typing-indicator {
  margin: 10px 0;
  display: flex;
  justify-content: flex-start;
}

.typing-indicator .message {
  margin-bottom: 0;
}

.typing-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  min-height: auto;
  width: fit-content;
  max-width: 70%;
}

.typing-dots {
  display: inline-flex;
  gap: 3px;
  align-items: center;
  flex-shrink: 0;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: #6366f1;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
  display: inline-block;
}

.typing-dots span:nth-child(1) {
  animation-delay: 0s;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

.typing-text {
  font-size: 0.875rem;
  color: #6b7280;
  font-style: italic;
  margin: 0;
  line-height: 1.2;
  white-space: nowrap;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  30% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 모달 스타일 */
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
  max-width: 400px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.modal-close {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.2s ease;
}

.modal-close:hover {
  color: #374151;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #374151;
  line-height: 1.5;
}

.modal-warning {
  color: #dc2626;
  font-weight: 500;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.cancel-btn {
  background: #f3f4f6;
  color: #374151;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.delete-btn {
  background: #dc2626;
  color: #ffffff;
}

.delete-btn:hover {
  background: #b91c1c;
}

/* Features Section */
.features-section {
  padding: 120px 0;
  background: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.feature-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 40px 32px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 32px 80px rgba(0, 0, 0, 0.1);
  border-color: rgba(102, 126, 234, 0.3);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-icon {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  position: relative;
}

.feature-icon.ai-models {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.feature-icon.smart-chat {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
}

.feature-icon.customization {
  background: linear-gradient(135deg, #ff6b6b, #ee5a52);
}

.feature-icon.multimodal {
  background: linear-gradient(135deg, #feca57, #ff9ff3);
}

.feature-icon.export {
  background: linear-gradient(135deg, #a55eea, #26de81);
}

.feature-icon.security {
  background: linear-gradient(135deg, #fd79a8, #fdcb6e);
}

.feature-icon i {
  font-size: 28px;
  color: white;
}

.feature-card h3 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 16px;
  letter-spacing: -0.025em;
}

.feature-card p {
  font-size: 16px;
  color: #64748b;
  line-height: 1.7;
  margin: 0;
}

/* Models Section */
.models-section {
  padding: 120px 0;
  background: linear-gradient(180deg, #fafbff 0%, #f1f5f9 100%);
}

.models-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.model-card {
  background: white;
  border-radius: 24px;
  padding: 40px 32px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.model-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 32px 80px rgba(0, 0, 0, 0.15);
}

.model-card.claude {
  border-top: 4px solid #ff6b6b;
}

.model-card.gpt {
  border-top: 4px solid #4ecdc4;
}

.model-card.gemini {
  border-top: 4px solid #667eea;
}

.model-header {
  margin-bottom: 24px;
}

.model-logo {
  width: 64px;
  height: 64px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  font-size: 28px;
  color: white;
}

.model-card.claude .model-logo {
  background: linear-gradient(135deg, #ff6b6b, #ee5a52);
}

.model-card.gpt .model-logo {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
}

.model-card.gemini .model-logo {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.model-header h3 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.model-provider {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.model-features {
  list-style: none;
  padding: 0;
  margin: 0;
}

.model-features li {
  padding: 8px 0;
  color: #64748b;
  font-size: 16px;
  position: relative;
  padding-left: 24px;
}

.model-features li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: 600;
}

/* Final CTA Section */
.final-cta-section {
  padding: 120px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 24px;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.cta-description {
  font-size: 20px;
  line-height: 1.7;
  margin-bottom: 40px;
  opacity: 0.9;
  font-weight: 500;
}

.cta-actions {
  margin-bottom: 24px;
}

.cta-note {
  font-size: 14px;
  opacity: 0.7;
  margin: 0;
}

/* 태블릿 */
@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 48px;
    text-align: center;
  }
  
  .hero-title {
    font-size: 48px;
  }
  
  .hero-description {
    font-size: 18px;
  }
  
  .section-title {
    font-size: 40px;
  }
  
  .section-subtitle {
    font-size: 18px;
  }
  
  .features-grid,
  .models-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .hero-visual {
    height: 400px;
  }
  
  .floating-card {
    max-width: 240px;
  }
}

/* 모바일 */
@media (max-width: 768px) {
  .section-container {
    padding: 0 16px;
  }
  
  .hero-section {
    padding: 40px 0 60px;
  }
  
  .hero-title {
    font-size: 36px;
  }
  
  .hero-description {
    font-size: 16px;
  }
  
  .hero-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .hero-stats {
    justify-content: center;
    gap: 24px;
  }
  
  .hero-visual {
    height: 300px;
  }
  
  .floating-card {
    max-width: 200px;
    padding: 16px;
  }
  
  .section-title {
    font-size: 32px;
  }
  
  .section-subtitle {
    font-size: 16px;
  }
  
  .section-header {
    margin-bottom: 40px;
  }
  
  .features-section,
  .models-section {
    padding: 60px 0;
  }
  
  .features-grid,
  .models-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .feature-card,
  .model-card {
    padding: 32px 24px;
  }
  
  .feature-icon,
  .model-logo {
    width: 56px;
    height: 56px;
  }
  
  .feature-icon i,
  .model-logo i {
    font-size: 24px;
  }
  
  .feature-card h3,
  .model-header h3 {
    font-size: 20px;
  }
  
  .feature-card p,
  .model-features li {
    font-size: 14px;
  }
  
  .final-cta-section {
    padding: 80px 0;
  }
  
  .cta-title {
    font-size: 32px;
  }
  
  .cta-description {
    font-size: 16px;
  }
  
  .primary-cta.large {
    padding: 16px 32px;
    font-size: 16px;
  }
  
  .chat-main-area {
    margin: 0;
    height: 100%;
    border-radius: 0;
    box-shadow: none;
    border: none;
  }
  
  .chat-container {
    margin: 0;
    border-radius: 0;
  }
  
  .chat-header {
    padding: 10px 16px;
  }
  
  .chat-header h3 {
    font-size: 16px;
  }
  
  .chat-messages {
    padding: 12px 16px;
  }
  
  .message-content {
    max-width: 85%;
    padding: 10px 14px;
  }
  
  .message-text {
    font-size: 13px;
  }
  
  .chat-input-area {
    padding: 12px 16px;
  }
  
  .input-container {
    gap: 10px;
  }
  
  .upload-btn-left {
    width: 40px;
    height: 40px;
    font-size: 14px;
  }
  
  .input-wrapper {
    min-height: 44px;
    padding: 10px 16px;
  }
  
  .message-input {
    font-size: 13px;
  }
  
  .send-btn {
    width: 40px;
    height: 40px;
    font-size: 14px;
  }
  
  .streaming-toggle {
    width: 40px;
    height: 40px;
    font-size: 14px;
    margin-right: 6px;
  }
  
  .scroll-to-bottom-btn-floating {
    top: -50px;
    padding: 10px 20px;
    font-size: 13px;
  }
  
  .scroll-to-bottom-btn-floating i {
    font-size: 11px;
  }
}

</style>