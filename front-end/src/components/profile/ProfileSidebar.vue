<template>
  <div class="sidebar">
    <nav class="sidebar-nav">
      <button 
        @click="handleTabClick('account')"
        :class="['nav-item', { active: activeTab === 'account' }]"
      >
        <span class="nav-icon">👤</span>
        <span>계정</span>
      </button>
      <button 
        @click="handleTabClick('api')"
        :class="['nav-item', { active: activeTab === 'api' }]"
      >
        <span class="nav-icon">🔑</span>
        <span>API</span>
      </button>
      <button 
        @click="handleTabClick('preset')"
        :class="['nav-item', { active: activeTab === 'preset' }]"
      >
        <span class="nav-icon">⚙️</span>
        <span>기본 프리셋</span>
      </button>
      <button 
        @click="handleTabClick('prompt')"
        :class="['nav-item', { active: activeTab === 'prompt' }]"
      >
        <span class="nav-icon">📝</span>
        <span>기본 프롬프트</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
defineProps({
  activeTab: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['tab-change'])

const handleTabClick = (tab) => {
  emit('tab-change', tab)
}
</script>

<style scoped>
.sidebar {
  width: 320px;
  height: 100%;
  background: #f8fafc;
  border-right: 1px solid #e2e8f0;
  border-left: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  padding: 24px;
  box-sizing: border-box;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  text-align: left;
  width: 100%;
}

.nav-item:hover {
  background: #e2e8f0;
  color: #475569;
}

.nav-item.active {
  background: #6366f1;
  color: white;
}

.nav-icon {
  font-size: 1.25rem;
  width: 20px;
  text-align: center;
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    position: static;
  }
  
  .sidebar-nav {
    flex-direction: row;
    overflow-x: auto;
  }
  
  .nav-item {
    white-space: nowrap;
  }
}
</style>