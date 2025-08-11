import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 인증 상태 관리 스토어
 * 로그인/로그아웃 상태와 사용자 정보를 중앙에서 관리
 */
export const useAuthStore = defineStore('auth', () => {
  // 상태
  const accessToken = ref(null)
  const refreshToken = ref(null)
  const user = ref(null)
  const isInitialized = ref(false)

  // Getters
  const isLoggedIn = computed(() => {
    return !!accessToken.value && !!user.value
  })

  const userInfo = computed(() => {
    return user.value || null
  })

  // Actions
  const initializeAuth = () => {
    try {
      // localStorage에서 토큰 및 사용자 정보 복구
      const storedAccessToken = localStorage.getItem('access_token')
      const storedRefreshToken = localStorage.getItem('refresh_token')
      const storedUser = localStorage.getItem('user_info')

      if (storedAccessToken) {
        accessToken.value = storedAccessToken
      }

      if (storedRefreshToken) {
        refreshToken.value = storedRefreshToken
      }

      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser)
        } catch (e) {
          console.warn('사용자 정보 파싱 실패:', e)
          localStorage.removeItem('user_info')
        }
      }

      isInitialized.value = true
    } catch (error) {
      console.error('인증 상태 초기화 중 오류:', error)
      isInitialized.value = true
    }
  }

  const login = (authData) => {
    try {
      // 토큰 저장
      if (authData.access_token) {
        accessToken.value = authData.access_token
        localStorage.setItem('access_token', authData.access_token)
      }

      if (authData.refresh_token) {
        refreshToken.value = authData.refresh_token
        localStorage.setItem('refresh_token', authData.refresh_token)
      }

      // 사용자 정보 저장
      if (authData.user) {
        user.value = authData.user
        localStorage.setItem('user_info', JSON.stringify(authData.user))
      }

      // 로그인 상태 유지 옵션
      if (authData.rememberMe) {
        localStorage.setItem('remember_me', 'true')
      }
    } catch (error) {
      console.error('로그인 상태 저장 중 오류:', error)
      throw error
    }
  }

  const logout = () => {
    try {
      // 상태 초기화
      accessToken.value = null
      refreshToken.value = null
      user.value = null

      // localStorage 정리
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_info')
      localStorage.removeItem('remember_me')

    } catch (error) {
      console.error('로그아웃 중 오류:', error)
    }
  }

  const updateTokens = (newAccessToken, newRefreshToken) => {
    if (newAccessToken) {
      accessToken.value = newAccessToken
      localStorage.setItem('access_token', newAccessToken)
    }

    if (newRefreshToken) {
      refreshToken.value = newRefreshToken
      localStorage.setItem('refresh_token', newRefreshToken)
    }
  }

  const updateUser = (userData) => {
    user.value = userData
    localStorage.setItem('user_info', JSON.stringify(userData))
  }

  const checkTokenExpiry = () => {
    // JWT 토큰 만료 검사 로직 (필요시 구현)
    // 현재는 단순히 토큰 존재 여부만 확인
    return !!accessToken.value
  }

  return {
    // State
    accessToken,
    refreshToken,
    user,
    isInitialized,
    
    // Getters
    isLoggedIn,
    userInfo,
    
    // Actions
    initializeAuth,
    login,
    logout,
    updateTokens,
    updateUser,
    checkTokenExpiry
  }
})