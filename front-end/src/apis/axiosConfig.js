import axios from 'axios'

// Axios 인스턴스 생성
const api = axios.create({
  baseURL: (process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000') + '/api/v1',
  timeout: 300000, // 5분 (300초) 타임아웃 설정
  headers: {
    'Content-Type': 'application/json',
  },
})

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    // 필요시 인증 토큰 추가
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 응답 인터셉터
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 인증 관련 오류 처리 (401 Unauthorized, 403 Forbidden)
    if (error.response?.status === 401 || error.response?.status === 403) {
      // 프로덕션에서는 상세 오류 정보 로깅 최소화
      if (process.env.NODE_ENV === 'development') {
        console.warn(`인증 오류 (${error.response.status})`)
      }
      
      // 토큰이 유효하지 않은 경우에만 토큰 제거
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    }
    return Promise.reject(error)
  }
)

export default api