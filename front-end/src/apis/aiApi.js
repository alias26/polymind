import api from './axiosConfig'

// AI 채팅 관련 API 함수들
export const aiApi = {

  // 스트리밍 방식으로 채팅 응답 생성
  async generateChatResponseStream(chatRequest, onChunk, onComplete, onError) {
    try {
      // 요청 데이터 준비
      const requestData = {
        message: chatRequest.message,
        provider: chatRequest.provider,
        model: chatRequest.model || null,
        max_tokens: chatRequest.max_tokens || 1000,
        temperature: chatRequest.temperature || 0.7,
        include_history: chatRequest.include_history !== false,
        system_prompt: chatRequest.system_prompt || null
      }
      
      // 이미지 처리 (현재 스트리밍에서는 JSON만 지원)
      if (chatRequest.images && chatRequest.images.length > 0) {
        const validImages = chatRequest.images
          .filter(img => img && img.data && img.data.trim() !== '') // null, undefined, 빈 문자열 제외
          .map(img => ({
            data: img.data,
            content_type: img.content_type || 'image/jpeg',
            filename: img.filename || 'image.jpg',
            size: img.size || Math.ceil(img.data.length * 0.75) // Base64 크기 추정
          }))
        
        if (validImages.length > 0) {
          requestData.images = validImages
        }
      }
      
      // SSE 연결 설정 (이제 /stream 없이 기본 채팅 엔드포인트)
      const apiUrl = `${process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'}/api/v1/ai/chat/${chatRequest.chat_id}`
      
      // POST 요청을 위한 설정
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Accept': 'text/event-stream',
          'Cache-Control': 'no-cache'
        },
        body: JSON.stringify(requestData)
      })
      
      if (!response.ok) {
        const errorText = await response.text()
        console.error('[aiApi] 스트리밍 요청 실패:', response.status, response.statusText, errorText)
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      // 스트림 읽기
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullContent = ''
      
      try {
        // eslint-disable-next-line no-constant-condition
        while (true) {
          const { done, value } = await reader.read()
          
          if (done) {
            break
          }
          
          // 청크 디코딩
          const chunk = decoder.decode(value, { stream: true })
          const lines = chunk.split('\n')
          
          for (const line of lines) {
            if (line.trim() === '') continue
            
            if (line.startsWith('data: ')) {
              try {
                const jsonStr = line.substring(6) // 'data: ' 제거
                if (jsonStr.trim() === '') continue
                
                const data = JSON.parse(jsonStr)
                
                switch (data.type) {
                  case 'start':
                    break
                    
                  case 'chunk':
                    if (data.content) {
                      fullContent += data.content
                      onChunk?.(data.content, fullContent)
                    }
                    break
                    
                  case 'end':
                    onComplete?.(data.full_content || fullContent)
                    return { content: data.full_content || fullContent }
                    
                  case 'error':
                    console.error('[aiApi] 서버 오류:', data.error)
                    onError?.(new Error(data.error))
                    return
                    
                  default:
                    console.warn('[aiApi] 알 수 없는 이벤트 타입:', data.type)
                }
              } catch (parseError) {
                console.error('[aiApi] JSON 파싱 오류:', parseError, 'Raw line:', line)
              }
            }
          }
        }
      } finally {
        reader.releaseLock()
      }
      
      // 스트림이 완료되었지만 end 이벤트가 없었던 경우
      if (fullContent) {
        onComplete?.(fullContent)
        return { content: fullContent }
      }
      
    } catch (error) {
      console.error('[aiApi] 스트리밍 오류:', error)
      onError?.(error)
      throw this.handleError(error)
    }
  },

  // 단순 텍스트 생성 (테스트용)
  async generateText(textRequest) {
    try {
      const response = await api.post('/ai/generate', textRequest)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 사용 가능한 AI 서비스 목록 조회
  async getAvailableProviders() {
    try {
      const response = await api.get('/ai/providers')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // AI 서비스 상태 체크
  async getHealthStatus() {
    try {
      const response = await api.get('/ai/health')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 레거시 메서드들 (현재는 스트리밍만 지원하므로 제거됨)
  // chatWithGpt, chatWithClaude, chatWithGemini 등은 
  // generateChatResponseStream 메서드 사용을 권장

  // 에러 처리
  handleError(error) {
    
    if (error.response) {
      const { status, data } = error.response
      const message = data?.detail || data?.message || '서버 오류가 발생했습니다.'
      
      switch (status) {
        case 400:
          // API 키 관련 오류인지 확인
          if (message.includes('API key')) {
            return new Error(`API 키 오류: ${message}`)
          }
          return new Error(message)
        case 401:
          return new Error('인증이 필요합니다. 로그인을 확인해주세요.')
        case 403:
          return new Error('접근이 거부되었습니다. API 키를 확인해주세요.')
        case 404:
          if (message.includes('Chat not found')) {
            return new Error('채팅을 찾을 수 없습니다.')
          }
          if (message.includes('API key')) {
            return new Error('해당 AI 서비스의 API 키가 설정되지 않았습니다.')
          }
          return new Error('요청한 리소스를 찾을 수 없습니다.')
        case 429:
          return new Error('API 호출 한도를 초과했습니다. 잠시 후 다시 시도해주세요.')
        case 500:
          return new Error('AI 서비스 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
        case 502:
          return new Error('서버 게이트웨이 오류입니다. 잠시 후 다시 시도해주세요.')
        case 503:
          return new Error('서비스가 일시적으로 사용할 수 없습니다. 잠시 후 다시 시도해주세요.')
        case 504:
          return new Error('서버 응답 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.')
        default:
          return new Error(`서버 오류 (${status}): ${message}`)
      }
    } else if (error.request) {
      // 네트워크 연결 문제 또는 타임아웃
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        return new Error('요청 시간이 초과되었습니다. AI 응답이 오래 걸리고 있습니다. 잠시 후 다시 시도해주세요.')
      } else if (error.code === 'ERR_NETWORK') {
        return new Error('네트워크 연결을 확인해주세요. 인터넷 연결 상태를 확인하거나 서버가 실행 중인지 확인해주세요.')
      } else {
        return new Error('서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.')
      }
    } else {
      // 요청 설정 오류
      return new Error(`예기치 않은 오류가 발생했습니다: ${error.message}`)
    }
  }
}