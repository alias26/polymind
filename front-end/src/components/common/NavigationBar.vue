<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <a href="#" @click.prevent="goToHome" class="brand-link"> PolyMind </a>
      </div>

      <div class="navbar-menu">
        <!-- 로그인 된 경우 -->
        <ul v-if="isLoggedIn" class="navbar-nav">
          <li class="nav-item profile-dropdown-container">
            <button
              @click="toggleProfileDropdown"
              class="nav-link profile-link"
              :class="{ active: showProfileDropdown }"
            >
              <div class="profile-avatar">
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path
                    d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                  />
                </svg>
              </div>
            </button>

            <!-- 드롭다운 메뉴 -->
            <div
              v-if="showProfileDropdown"
              class="profile-dropdown"
              @click.stop
            >
              <div class="dropdown-header">
                <div class="user-info">
                  <div class="user-avatar">
                    <svg
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                      />
                    </svg>
                  </div>
                  <div class="user-details">
                    <div class="user-name">
                      {{ currentUser.name || '사용자' }}
                    </div>
                    <div class="user-id">{{ currentUser.id || 'user' }}</div>
                  </div>
                </div>
              </div>

              <div class="dropdown-menu">
                <router-link
                  to="/profile"
                  class="dropdown-item"
                  @click="closeProfileDropdown"
                >
                  <i class="fas fa-user"></i>
                  <span>계정 설정</span>
                </router-link>
                <button class="dropdown-item logout-btn" @click="handleLogout">
                  <i class="fas fa-sign-out-alt"></i>
                  <span>로그아웃</span>
                </button>
              </div>
            </div>
          </li>
        </ul>

        <!-- 비로그인 상태일 때 -->
        <ul v-else class="navbar-nav">
          <li class="nav-item">
            <button class="btn-base btn-link" @click="goToLogin">
              로그인
            </button>
          </li>
          <li class="nav-item">
            <button class="btn-base btn-primary" @click="goToSignup">
              회원가입
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 로그인 상태 관리
const isLoggedIn = ref(false)
const showProfileDropdown = ref(false)
const currentUser = ref({
  name: '',
  id: '',
})

// 로그인 상태 확인 함수
const checkLoginStatus = async () => {
  const token = localStorage.getItem('access_token')
  isLoggedIn.value = !!token

  if (token) {
    try {
      // 실제 사용자 정보 API 호출
      const { authApi } = await import('@/apis/authApi')
      const userInfo = await authApi.getUserInfo()
      currentUser.value = {
        name: userInfo.name || userInfo.username || '사용자',
        id: userInfo.username || userInfo.id || 'user',
      }
    } catch (error) {
      console.error('사용자 정보 조회 실패:', error)
      // API 호출 실패 시 기본값 사용
      currentUser.value = {
        name: '사용자',
        id: 'user',
      }
    }
  } else {
    currentUser.value = { name: '', id: '' }
  }
}

// 프로필 드롭다운 토글
const toggleProfileDropdown = () => {
  showProfileDropdown.value = !showProfileDropdown.value
}

// 프로필 드롭다운 닫기
const closeProfileDropdown = () => {
  showProfileDropdown.value = false
}

// 홈으로 이동 (소개화면 표시)
const goToHome = async () => {
  try {
    // chatStore를 import하고 activeChat을 null로 설정
    const { default: chatStore } = await import('@/store/chatStore')
    chatStore.setActiveChat(null)
    
    // 홈으로 이동
    await router.push('/')
  } catch (error) {
    console.error('홈 이동 중 오류:', error)
    // 오류가 발생해도 일단 홈으로 이동
    await router.push('/')
  }
}

// 로그인 페이지로 이동
const goToLogin = () => {
  router.push('/login')
}

// 회원가입 페이지로 이동
const goToSignup = () => {
  router.push('/signup')
}

// 로그아웃 처리
const handleLogout = async () => {
  try {

    // 1. 먼저 채팅 상태 초기화 (토큰이 있을 때)
    const { default: chatStore } = await import('@/store/chatStore')
    chatStore.clearAllData()

    // 2. authStore의 logout 호출 (토큰 제거 및 상태 초기화)
    const { useAuthStore } = await import('@/store/auth')
    const authStore = useAuthStore()
    authStore.logout()

    // 3. 네비게이션 바 상태 업데이트
    isLoggedIn.value = false
    showProfileDropdown.value = false
    currentUser.value = { name: '', id: '' }

    // 4. 홈페이지로 직접 이동 (라우터 가드가 작동하기 전에)
    window.location.href = '/'

  } catch (error) {
    console.error('로그아웃 오류:', error)
    
    // 오류가 발생해도 강제로 로그아웃 상태로 만들기
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token') 
    localStorage.removeItem('remember_me')
    isLoggedIn.value = false
    showProfileDropdown.value = false
    currentUser.value = { name: '', id: '' }
    
    await router.push('/')
    window.location.reload()
  }
}

// 외부 클릭 시 드롭다운 닫기
const handleClickOutside = (event) => {
  const dropdown = event.target.closest('.profile-dropdown-container')
  if (!dropdown) {
    showProfileDropdown.value = false
  }
}

// 컴포넌트 마운트 시 로그인 상태 확인
onMounted(async () => {
  await checkLoginStatus()
  document.addEventListener('click', handleClickOutside)
})

// 컴포넌트 언마운트 시 이벤트 리스너 제거
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 로그인 상태 변경 감지 (로그인/로그아웃 시)
watch(
  () => router.currentRoute.value.path,
  async () => {
    await checkLoginStatus()
  }
)

// localStorage 변경 감지 (다른 탭에서 로그인/로그아웃 시)
window.addEventListener('storage', async () => {
  await checkLoginStatus()
})

// 사용자 정보 강제 새로고침을 위한 이벤트 리스너
window.addEventListener('userInfoUpdate', async () => {
  await checkLoginStatus()
})
</script>

<style scoped>
.navbar {
  background-color: #ffffff;
  padding: 1rem 0;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid #e5e7eb;
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  box-sizing: border-box;
}

.navbar-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 4px;
  box-sizing: border-box;
}

.navbar-menu {
  margin-right: 0;
}

.navbar-brand .brand-link {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-decoration: none;
  font-size: 1.75rem;
  font-weight: 800;
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;
  letter-spacing: -0.025em;
  line-height: 1;
  display: flex;
  align-items: center;
  height: 40px;
}

.navbar-nav {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 16px;
  align-items: center;
}

.nav-item .nav-link {
  /* color: #6b7280; */
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-weight: 500;
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;
  border: 1px solid transparent;
  display: flex;
  align-items: center;
  height: 40px;
  box-sizing: border-box;
}

.profile-link {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}

.nav-item .nav-link:hover {
  background-color: #f3f4f6;
  color: #374151;
  border-color: #e5e7eb;
}

.profile-link:hover {
  background: transparent !important;
  border: none !important;
}

.nav-item .nav-link.active:not(.profile-link) {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: white;
  box-shadow: 0 1px 3px rgba(99, 102, 241, 0.15);
  border-color: #4f46e5;
}

.profile-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(107, 114, 128, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* 네비게이션 버튼들은 공통 스타일 사용 */

.profile-dropdown-container {
  position: relative;
}

.profile-link {
  cursor: pointer !important;
  text-decoration: none !important;
}

.profile-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  min-width: 280px;
  z-index: var(--z-dropdown);
  overflow: hidden;
}

.dropdown-header {
  padding: 20px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: #6366f1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 1px;
  justify-content: center;
  align-items: flex-start;
}

.user-name {
  font-weight: 600;
  font-size: 16px;
  color: #1f2937;
  line-height: 1.3;
  margin: 0;
  padding: 0;
  display: block;
}

.user-id {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.3;
  margin: 0;
  padding: 0;
  display: block;
}

.dropdown-menu {
  padding: 8px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  min-height: 44px;
  color: #374151;
  text-decoration: none;
  transition: all 0.2s ease;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  box-sizing: border-box;
}

.dropdown-item:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.dropdown-item i {
  width: 16px;
  text-align: center;
  color: #6b7280;
}

.dropdown-item:hover i {
  color: #374151;
}

.logout-btn:hover {
  background: #fef2f2 !important;
  color: #dc2626 !important;
}

.logout-btn:hover i {
  color: #dc2626 !important;
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 1rem;
  }

  .navbar-nav {
    gap: 1rem;
  }
}
</style>
