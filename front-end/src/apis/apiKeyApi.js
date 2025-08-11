import api from './axiosConfig'

// API 키 관련 API 함수들
export const apiKeyApi = {
  // API 키 저장
  async saveApiKey(provider, apiKey) {
    try {
      const response = await api.post('/api-keys', {
        provider,
        apiKey,
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // API 키 조회
  async getApiKey(provider) {
    try {
      const response = await api.get(`/api-keys/${provider}`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 모든 API 키 조회
  async getAllApiKeys() {
    try {
      const response = await api.get('/api-keys')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // API 키 삭제
  async deleteApiKey(provider) {
    try {
      const response = await api.delete(`/api-keys/${provider}`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 모든 API 키 삭제
  async deleteAllApiKeys() {
    try {
      const response = await api.delete('/api-keys')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // API 키 유효성 검사 (서버사이드)
  async validateApiKey(provider, apiKey) {
    try {
      const response = await api.post('/api-keys/validate', {
        provider,
        apiKey,
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 복호화된 API 키 조회
  async getDecryptedApiKey(provider) {
    try {
      const response = await api.get(`/api-keys/${provider}/decrypted`)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // API 키 존재 여부 확인 (마스킹된 정보만)
  async checkApiKeyExists(provider) {
    try {
      const response = await api.get(`/api-keys/${provider}`)
      return response.data
    } catch (error) {
      if (error.response?.status === 404) {
        return null
      }
      throw this.handleError(error)
    }
  },

  // 에러 처리
  handleError(error) {
    if (error.response) {
      // 서버 응답 에러
      const { status, data } = error.response
      const message = data?.message || '서버 오류가 발생했습니다.'
      
      // 백엔드에서 detail 메시지를 사용
      const detailMessage = data?.detail || message
      
      switch (status) {
        case 400:
          return new Error(detailMessage)
        case 401:
          return new Error('인증이 필요합니다.')
        case 403:
          return new Error('접근이 거부되었습니다.')
        case 404:
          return new Error('요청한 리소스를 찾을 수 없습니다.')
        case 409:
          return new Error('이미 존재하는 API 키입니다.')
        case 500:
          return new Error('서버 내부 오류가 발생했습니다.')
        default:
          return new Error(`서버 오류 (${status}): ${detailMessage}`)
      }
    } else if (error.request) {
      // 네트워크 오류
      return new Error('네트워크 연결을 확인해주세요.')
    } else {
      // 기타 오류
      return new Error('예기치 않은 오류가 발생했습니다.')
    }
  }
}