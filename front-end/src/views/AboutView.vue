<template>
  <div class="about-page">
    <div class="hero-section">
      <div class="hero-content">
        <div class="welcome-icon">✨</div>
        <h1 class="hero-title">PolyMind에 오신 것을 환영합니다!</h1>
        <p class="hero-subtitle">AI와 함께 새로운 대화를 시작해보세요</p>
        
        <div class="action-cards">
          <div class="action-card primary-card" @click="startNewChat">
            <div class="card-icon">➕</div>
            <div class="card-content">
              <h3>새 채팅 시작</h3>
              <p>AI와 새로운 대화를 시작합니다</p>
            </div>
          </div>
          
          <div class="action-card secondary-card">
            <div class="card-icon">👁️</div>
            <div class="card-content">
              <h3>최근 채팅 불러오기</h3>
              <p>이전 대화 기록을 확인합니다</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="features-section">
      <h2 class="features-title">PolyMind 기능</h2>
      <div class="features-grid">
        <div class="feature-item">
          <div class="feature-icon">🤖</div>
          <h3>다양한 AI 모델</h3>
          <p>OpenAI, Claude, Gemini 등 다양한 AI 모델과 대화할 수 있습니다</p>
        </div>
        
        <div class="feature-item">
          <div class="feature-icon">💬</div>
          <h3>실시간 대화</h3>
          <p>자연스러운 대화 흐름으로 AI와 소통할 수 있습니다</p>
        </div>
        
        <div class="feature-item">
          <div class="feature-icon">📝</div>
          <h3>채팅 기록 저장</h3>
          <p>대화 내용을 저장하고 언제든 다시 확인할 수 있습니다</p>
        </div>
        
        <div class="feature-item">
          <div class="feature-icon">⚡</div>
          <h3>빠른 응답</h3>
          <p>최적화된 시스템으로 빠르고 정확한 AI 응답을 제공합니다</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const startNewChat = () => {
  router.push('/')
}
</script>

<style scoped>
.about-page {
  min-height: calc(100vh - 72px);
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 0;
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  padding: 60px 20px;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  width: 100%;
}

.welcome-icon {
  font-size: 4rem;
  margin-bottom: 30px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 20px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: -0.025em;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #64748b;
  margin-bottom: 50px;
  font-weight: 500;
}

.action-cards {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 60px;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 30px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-width: 280px;
  max-width: 350px;
}

.primary-card {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
}

.primary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(99, 102, 241, 0.3);
}

.secondary-card {
  background: white;
  color: #374151;
  border: 2px solid #e5e7eb;
}

.secondary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  border-color: #6366f1;
}

.card-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.card-content h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 8px;
  margin-top: 0;
}

.card-content p {
  font-size: 0.95rem;
  opacity: 0.9;
  margin: 0;
  line-height: 1.5;
}

.features-section {
  padding: 80px 20px;
  background: white;
}

.features-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 800;
  color: #1f2937;
  margin-bottom: 60px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-item {
  text-align: center;
  padding: 40px 20px;
  border-radius: 16px;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  border-color: #6366f1;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-item h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 15px;
  margin-top: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.feature-item p {
  font-size: 1rem;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.25rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .action-cards {
    flex-direction: column;
    align-items: center;
  }
  
  .action-card {
    max-width: 100%;
    width: 100%;
  }
  
  .features-title {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}
</style>
