import api from './axiosConfig'

// 인증 관련 API 함수들
export const authApi = {
  // 로그인
  async login(credentials) {
    try {
      const response = await api.post('/auth/login', credentials)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 로그아웃
  async logout() {
    try {
      const response = await api.post('/auth/logout')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 회원가입
  async register(userData) {
    try {
      const response = await api.post('/auth/register', userData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 토큰 갱신
  async refreshToken() {
    try {
      const response = await api.post('/auth/refresh')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 사용자 정보 조회
  async getUserInfo() {
    try {
      const response = await api.get('/auth/user')
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 사용자 정보 업데이트
  async updateUserInfo(userInfo) {
    try {
      const response = await api.put('/auth/user', userInfo)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 비밀번호 변경
  async changePassword(passwordData) {
    try {
      const response = await api.post('/auth/change-password', passwordData)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 현재 비밀번호 검증
  async verifyCurrentPassword(currentPassword) {
    try {
      const response = await api.post('/auth/verify-password', {
        current_password: currentPassword
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 에러 처리
  handleError(error) {
    if (error.response) {
      const { status, data } = error.response
      
      // Pydantic validation 에러 처리
      if (data?.detail) {
        if (Array.isArray(data.detail)) {
          // Pydantic validation error array
          const errorMessages = data.detail.map(err => {
            const field = err.loc ? err.loc.join('.') : 'field'
            return `${field}: ${err.msg}`
          }).join(', ')
          return new Error(errorMessages)
        } else if (typeof data.detail === 'string') {
          // String detail message
          return new Error(data.detail)
        }
      }
      
      // FastAPI HTTPException 처리
      const message = data?.message || data?.detail || '서버 오류가 발생했습니다.'
      
      switch (status) {
        case 400:
          return new Error(message)
        case 401:
          return new Error('인증이 필요합니다.')
        case 403:
          return new Error('접근이 거부되었습니다.')
        case 404:
          return new Error('요청한 리소스를 찾을 수 없습니다.')
        case 409:
          return new Error(message)
        case 422:
          // Validation error
          return new Error(message)
        case 500:
          return new Error('서버 내부 오류가 발생했습니다.')
        default:
          return new Error(`서버 오류 (${status}): ${message}`)
      }
    } else if (error.request) {
      return new Error('네트워크 연결을 확인해주세요.')
    } else {
      return new Error('예기치 않은 오류가 발생했습니다.')
    }
  },

  // 아이디 찾기
  async findUserId(email) {
    try {
      const response = await api.post('/auth/find-user-id', { email })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 비밀번호 재설정 요청
  async requestPasswordReset(email) {
    try {
      const response = await api.post('/auth/request-password-reset', { email })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 비밀번호 재설정 실행
  async resetPassword(token, newPassword) {
    try {
      const response = await api.post('/auth/reset-password', {
        token,
        new_password: newPassword
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 이메일 인증 코드 발송
  async sendVerificationEmail(email) {
    try {
      const response = await api.post('/auth/send-verification-email', { email })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  },

  // 이메일 인증 코드 검증
  async verifyEmail(email, code) {
    try {
      const response = await api.post('/auth/verify-email', { 
        email, 
        code 
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }
}