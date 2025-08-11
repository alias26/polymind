import api from './axiosConfig'

export const userPreferencesApi = {
  // 사용자 설정 조회
  getUserPreferences: async () => {
    try {
      const response = await api.get('/user/preferences/')
      return response.data
    } catch (error) {
      throw userPreferencesApi.handleError(error)
    }
  },

  // 사용자 설정 업데이트
  updateUserPreferences: async (preferences) => {
    try {
      const response = await api.put('/user/preferences/', preferences)
      return response.data
    } catch (error) {
      throw userPreferencesApi.handleError(error)
    }
  },

  // 사용자 설정 삭제
  deleteUserPreferences: async () => {
    try {
      const response = await api.delete('/user/preferences/')
      return response.data
    } catch (error) {
      throw userPreferencesApi.handleError(error)
    }
  },

  // 에러 처리
  handleError(error) {
    if (error.response) {
      // 서버 응답 에러
      const { status, data } = error.response
      const message = data?.detail || data?.message || '서버 오류가 발생했습니다.'
      
      switch (status) {
        case 400:
          return new Error(`잘못된 요청: ${message}`)
        case 401:
          return new Error('인증이 필요합니다.')
        case 403:
          return new Error('접근이 거부되었습니다.')
        case 404:
          return new Error('사용자 설정을 찾을 수 없습니다.')
        case 500:
          return new Error('서버 내부 오류가 발생했습니다.')
        default:
          return new Error(`서버 오류 (${status}): ${message}`)
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