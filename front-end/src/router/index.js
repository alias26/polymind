import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import LandingView from '../views/LandingView.vue'
import ChatView from '../views/ChatView.vue'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ChatSettings from '../components/chat/ChatSettings.vue'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingView,
    meta: { 
      requiresGuest: true // 비로그인 사용자만 접근 가능
    }
  },
  {
    path: '/chat',
    name: 'chat',
    component: ChatView,
    meta: { 
      requiresAuth: true // 로그인 필요
    }
  },
  {
    path: '/chat/:id',
    name: 'chat-detail',
    component: ChatView,
    props: true,
    meta: { 
      requiresAuth: true // 로그인 필요
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { 
      requiresGuest: true // 비로그인 사용자만 접근 가능
    }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView,
    meta: { 
      requiresGuest: true // 비로그인 사용자만 접근 가능
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    redirect: '/profile/account',
    meta: { 
      requiresAuth: true // 로그인 필요
    },
    children: [
      {
        path: 'account',
        name: 'profile-account',
        component: ProfileView
      },
      {
        path: 'api',
        name: 'profile-api',
        component: ProfileView
      },
      {
        path: 'preset',
        name: 'profile-preset',
        component: ProfileView
      },
      {
        path: 'prompt',
        name: 'profile-prompt',
        component: ProfileView
      }
    ]
  },
  {
    path: '/chat/:chatId/settings',
    name: 'chat-settings',
    component: ChatSettings,
    meta: { 
      requiresAuth: true // 로그인 필요
    }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: { 
      requiresGuest: true // 비로그인 사용자만 접근 가능
    }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  // 기존 HomeView는 임시로 유지 (호환성)
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: { 
      requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 라우트 가드 설정
router.beforeEach((to, from, next) => {
  // Pinia 스토어는 라우터 설정 후에 사용 가능
  const authStore = useAuthStore()
  
  // 인증 상태가 초기화되지 않았다면 초기화
  if (!authStore.isInitialized) {
    authStore.initializeAuth()
  }
  
  const isLoggedIn = authStore.isLoggedIn
  const requiresAuth = to.meta.requiresAuth
  const requiresGuest = to.meta.requiresGuest
  
  // 인증이 필요한 페이지에 비로그인 사용자가 접근하는 경우
  if (requiresAuth && !isLoggedIn) {
    next('/login')
    return
  }
  
  // 비로그인 사용자만 접근할 수 있는 페이지에 로그인 사용자가 접근하는 경우
  if (requiresGuest && isLoggedIn) {
    next('/chat')
    return
  }
  
  // 루트 경로 (/) 접근 시 인증 상태에 따른 리다이렉트
  if (to.path === '/') {
    if (isLoggedIn) {
      next('/chat')
      return
    } else {
      // 비로그인 상태에서는 랜딩 페이지 표시 (이미 설정됨)
    }
  }
  
  // 일반적인 경우 진행
  next()
})

export default router
