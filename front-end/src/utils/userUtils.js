// 사용자 정보 업데이트 유틸리티

/**
 * 사용자 정보를 강제로 새로고침하도록 이벤트를 발생시킵니다.
 * 로그인 성공 후 네비게이션바의 사용자 정보를 즉시 업데이트할 때 사용합니다.
 */
export function refreshUserInfo() {
  const event = new CustomEvent('userInfoUpdate')
  window.dispatchEvent(event)
}

/**
 * 로그인 성공 후 토큰을 저장하고 사용자 정보를 업데이트합니다.
 * @param {Object} tokenData - API로부터 받은 토큰 데이터
 */
export function handleLoginSuccess(tokenData) {
  // 토큰 저장
  localStorage.setItem('access_token', tokenData.access_token)
  localStorage.setItem('refresh_token', tokenData.refresh_token)
  
  // 사용자 정보 새로고침 이벤트 발생
  refreshUserInfo()
}