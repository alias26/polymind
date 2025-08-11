<template>
  <div class="profile-container">
    
    <div class="profile-layout">
      <!-- 좌측 사이드바 -->
      <ProfileSidebar 
        :active-tab="activeTab" 
        @tab-change="handleTabChange"
      />
      
      <!-- 우측 콘텐츠 -->
      <div class="content">
        <!-- 계정 설정 -->
        <ProfileAccountView v-if="activeTab === 'account'" />
        
        <!-- API 설정 -->
        <ProfileApiView v-if="activeTab === 'api'" />
        
        <!-- 프리셋 설정 -->
        <ProfilePresetView v-if="activeTab === 'preset'" />
        
        <!-- 기본 프롬프트 설정 -->
        <ProfilePromptView v-if="activeTab === 'prompt'" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import ProfileSidebar from '@/components/profile/ProfileSidebar.vue'
import ProfileAccountView from '@/views/profile/ProfileAccountView.vue'
import ProfileApiView from '@/views/profile/ProfileApiView.vue'
import ProfilePresetView from '@/views/profile/ProfilePresetView.vue'
import ProfilePromptView from '@/views/profile/ProfilePromptView.vue'

const router = useRouter()
const route = useRoute()

// 현재 라우트 기반으로 활성 탭 계산
const activeTab = computed(() => {
  const currentPath = route.path
  if (currentPath.includes('/profile/api')) return 'api'
  if (currentPath.includes('/profile/preset')) return 'preset'
  if (currentPath.includes('/profile/prompt')) return 'prompt'
  return 'account'
})

// 탭 변경 함수
const handleTabChange = (tab) => {
  router.push(`/profile/${tab}`)
}
</script>

<style scoped>
.profile-container {
  height: calc(100vh - 72px);
  display: flex;
  flex-direction: column;
  background: #ffffff;
  overflow: hidden;
  justify-content: center;
}

.profile-layout {
  flex: 1;
  display: flex;
  height: 100%;
  overflow: hidden;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  gap: 0;
}

.content {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  overflow-y: auto;
  margin: 24px 24px 24px 24px;
}







@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }
  
  .profile-title {
    font-size: 2rem;
  }
  
  .profile-layout {
    flex-direction: column;
  }
  
  
  
}
</style>