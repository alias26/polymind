import api from './axiosConfig'

/**
 * 채팅 관리 API
 */
export const chatApi = {
  /**
   * 채팅 목록 조회
   */
  async getChats() {
    try {
      const response = await api.get('/chats/')
      return response.data
    } catch (error) {
      console.error('채팅 목록 조회 실패:', error)
      throw error
    }
  },

  /**
   * 새 채팅 생성
   * @param {Object} chatData - { title: string, selectedModel?: string, systemPrompt?: string, temperature?: number, maxTokens?: number }
   */
  async createChat(chatData) {
    try {
      const requestData = {
        title: chatData.title || '새 채팅',
        model: chatData.selectedModel, // 선택된 모델 그대로 사용
        system_prompt: chatData.systemPrompt || null,
        temperature: chatData.temperature || 0.7,
        max_tokens: chatData.maxTokens || 2048
        // api_key 필드 제거
      }
      
      
      const response = await api.post('/chats/', requestData)
      return response.data
    } catch (error) {
      console.error('채팅 생성 실패:', error)
      throw error
    }
  },

  /**
   * 특정 채팅 조회
   * @param {string} chatId 
   */
  async getChat(chatId) {
    try {
      const response = await api.get(`/chats/${chatId}`)
      return response.data
    } catch (error) {
      console.error('채팅 조회 실패:', error)
      throw error
    }
  },

  /**
   * 채팅 정보 업데이트
   * @param {string} chatId 
   * @param {Object} updateData - { title?: string, selectedModel?: string, systemPrompt?: string, temperature?: number, maxTokens?: number }
   */
  async updateChat(chatId, updateData) {
    try {
      const requestData = {}
      
      // 정의된 필드만 추가
      if (updateData.title !== undefined) requestData.title = updateData.title
      if (updateData.selectedModel !== undefined) requestData.model = updateData.selectedModel
      if (updateData.systemPrompt !== undefined) requestData.system_prompt = updateData.systemPrompt
      if (updateData.temperature !== undefined) requestData.temperature = updateData.temperature
      if (updateData.maxTokens !== undefined) requestData.max_tokens = updateData.maxTokens
      
      const response = await api.put(`/chats/${chatId}`, requestData)
      return response.data
    } catch (error) {
      console.error('채팅 업데이트 실패:', error)
      throw error
    }
  },

  /**
   * 채팅 삭제
   * @param {string} chatId 
   */
  async deleteChat(chatId) {
    try {
      const response = await api.delete(`/chats/${chatId}`)
      return response.data
    } catch (error) {
      console.error('채팅 삭제 실패:', error)
      throw error
    }
  },

  /**
   * 채팅의 메시지 목록 조회 (페이지네이션 지원)
   * @param {string} chatId 
   * @param {Object} params - { limit?: number, offset?: number }
   */
  async getMessages(chatId, params = {}) {
    try {
      const queryParams = new URLSearchParams()
      if (params.limit) queryParams.append('limit', params.limit)
      if (params.offset) queryParams.append('offset', params.offset)
      
      const url = `/chats/${chatId}/messages${queryParams.toString() ? '?' + queryParams.toString() : ''}`
      const response = await api.get(url)
      return { data: response.data }
    } catch (error) {
      console.error('메시지 조회 실패:', error)
      throw error
    }
  },

  /**
   * 채팅에 메시지 추가
   * @param {string} chatId 
   * @param {Object} messageData - { content: string, role: 'user' | 'assistant' }
   */
  async addMessage(chatId, messageData) {
    try {
      // role을 sender로 매핑하고, assistant는 ai로 변환
      const sender = messageData.role === 'assistant' ? 'ai' : messageData.role
      
      const response = await api.post(`/chats/${chatId}/messages`, {
        content: messageData.content,
        sender: sender
      })
      return response.data
    } catch (error) {
      console.error('메시지 추가 실패:', error)
      throw error
    }
  },

  /**
   * 채팅의 모든 메시지 삭제
   * @param {string} chatId 
   */
  async clearMessages(chatId) {
    try {
      const response = await api.delete(`/chats/${chatId}/messages`)
      return response.data
    } catch (error) {
      console.error('메시지 클리어 실패:', error)
      throw error
    }
  },

  /**
   * AI 응답 생성
   * @param {Object} requestData - { messages: Array, model: string, provider?: string }
   */
  async generateAIResponse(requestData) {
    try {
      const response = await api.post('/ai/generate', {
        messages: requestData.messages,
        model: requestData.model,
        provider: requestData.provider,
        max_tokens: requestData.maxTokens || 1000,
        temperature: requestData.temperature || 0.7
      })
      return response.data
    } catch (error) {
      console.error('AI 응답 생성 실패:', error)
      throw error
    }
  },

  /**
   * 다중 AI 서비스 응답 생성
   * @param {Object} requestData 
   */
  async generateMultiAIResponse(requestData) {
    try {
      const response = await api.post('/ai/generate/multi', requestData)
      return response.data
    } catch (error) {
      console.error('다중 AI 응답 생성 실패:', error)
      throw error
    }
  },

  /**
   * 사용 가능한 AI 제공자 목록 조회
   */
  async getProviders() {
    try {
      const response = await api.get('/ai/providers')
      return response.data
    } catch (error) {
      console.error('AI 제공자 목록 조회 실패:', error)
      throw error
    }
  },

  /**
   * AI 서비스 상태 확인
   */
  async checkAIHealth() {
    try {
      const response = await api.get('/ai/health')
      return response.data
    } catch (error) {
      console.error('AI 서비스 상태 확인 실패:', error)
      throw error
    }
  }
}

export default chatApi