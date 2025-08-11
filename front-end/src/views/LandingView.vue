<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">
            다양한 AI 모델을
            <span class="gradient-text">PolyMind</span>에서 사용하세요
          </h1>
          <p class="hero-description">
            Claude, GPT, Gemini 등 주요 AI 모델들을 하나의 플랫폼에서 편리하게 사용할 수 있습니다.
            업무 효율성과 창의적 작업을 향상시켜보세요.
          </p>
          <div class="hero-actions">
            <router-link to="/signup" class="primary-cta">
              <span>무료로 시작하기</span>
              <i class="fas fa-arrow-right"></i>
            </router-link>
            <router-link to="/login" class="secondary-cta">
              로그인
            </router-link>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">5+</span>
              <span class="stat-label">AI 모델</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">편리한</span>
              <span class="stat-label">통합 관리</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">안전한</span>
              <span class="stat-label">데이터 보호</span>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-header">
              <div class="ai-badge claude">Claude</div>
              <span class="card-title">창작 도우미</span>
            </div>
            <p class="card-content">소설 줄거리를 작성해주세요...</p>
          </div>
          <div class="floating-card card-2">
            <div class="card-header">
              <div class="ai-badge gpt">GPT-4</div>
              <span class="card-title">코딩 어시스턴트</span>
            </div>
            <p class="card-content">React 컴포넌트를 최적화하는 방법...</p>
          </div>
          <div class="floating-card card-3">
            <div class="card-header">
              <div class="ai-badge gemini">Gemini</div>
              <span class="card-title">분석 전문가</span>
            </div>
            <p class="card-content">이 차트 데이터를 해석해주세요...</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">주요 기능</h2>
          <p class="section-subtitle">AI 모델 사용을 위한 필수 도구들</p>
        </div>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon ai-models">
              <i class="fas fa-brain"></i>
            </div>
            <h3>다양한 AI 모델</h3>
            <p>Claude, GPT, Gemini 등 주요 AI 모델들을 편리하게 전환하며 사용할 수 있습니다</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon smart-chat">
              <i class="fas fa-comments-dollar"></i>
            </div>
            <h3>대화 기록 관리</h3>
            <p>대화 내용을 체계적으로 저장하고 필요할 때 쉽게 찾아볼 수 있습니다</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon customization">
              <i class="fas fa-sliders-h"></i>
            </div>
            <h3>모델 설정 조정</h3>
            <p>Temperature, 토큰 수 등 AI 모델의 파라미터를 조정할 수 있습니다</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon multimodal">
              <i class="fas fa-image"></i>
            </div>
            <h3>파일 업로드</h3>
            <p>텍스트, 이미지, 문서 등 다양한 형태의 파일을 AI에 업로드할 수 있습니다</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon security">
              <i class="fas fa-shield-alt"></i>
            </div>
            <h3>보안 및 개인정보 보호</h3>
            <p>사용자의 API 키와 대화 내용은 안전하게 암호화되어 저장됩니다</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon cost-effective">
              <i class="fas fa-coins"></i>
            </div>
            <h3>비용 효율적 사용</h3>
            <p>각 모델의 특성을 활용하여 최적의 비용으로 AI를 활용할 수 있습니다</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-container">
        <div class="cta-content">
          <h2 class="cta-title">지금 시작해보세요</h2>
          <p class="cta-description">
            무료 회원가입으로 다양한 AI 모델을 체험해보세요
          </p>
          <div class="cta-actions">
            <router-link to="/signup" class="cta-button primary">
              무료 회원가입
            </router-link>
            <router-link to="/login" class="cta-button secondary">
              로그인
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// 랜딩 페이지는 정적 컨텐츠이므로 특별한 로직이 필요하지 않음
</script>

<style scoped>
/* 전체 레이아웃 */
.landing-page {
  position: fixed;
  top: 80px;
  left: 0;
  width: 100%;
  height: calc(100vh - 80px);
  background: linear-gradient(180deg, #fafbff 0%, #f8fafc 100%);
  overflow-y: auto;
  overflow-x: hidden;
  z-index: 1;
}

/* Hero Section */
.hero-section {
  padding: 80px 0 40px;
  position: relative;
  overflow: hidden;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.hero-content {
  z-index: 10;
}

.hero-title {
  font-size: 64px;
  font-weight: 900;
  line-height: 1.1;
  color: #1e293b;
  margin-bottom: 24px;
  letter-spacing: -0.02em;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-description {
  font-size: 20px;
  color: #64748b;
  line-height: 1.7;
  margin-bottom: 40px;
  font-weight: 500;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 48px;
  align-items: center;
}

.primary-cta {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 32px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.4);
}

.primary-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.5);
}

.secondary-cta {
  color: #64748b;
  padding: 16px 32px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  background: white;
}

.secondary-cta:hover {
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

.hero-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.stat-number {
  font-size: 32px;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* Hero Visual */
.hero-visual {
  position: relative;
  height: 600px;
}

.floating-card {
  position: absolute;
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  max-width: 280px;
  animation: float 6s ease-in-out infinite;
}

.card-1 {
  top: 0;
  right: 0;
  animation-delay: 0s;
}

.card-2 {
  top: 200px;
  left: 0;
  animation-delay: 2s;
}

.card-3 {
  bottom: 0;
  right: 40px;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.ai-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: white;
}

.ai-badge.claude { 
  background: linear-gradient(135deg, #ff6b6b, #ee5a52); 
}

.ai-badge.gpt { 
  background: linear-gradient(135deg, #4ecdc4, #44a08d); 
}

.ai-badge.gemini { 
  background: linear-gradient(135deg, #667eea, #764ba2); 
}

.card-title {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.card-content {
  color: #64748b;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
}

/* Features Section */
.features-section {
  padding: 40px 0 100px;
  background: #f8f9fa;
}

.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-header {
  text-align: center;
  margin-bottom: 64px;
}

.section-title {
  font-size: 48px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 16px;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.section-subtitle {
  font-size: 20px;
  color: #64748b;
  font-weight: 500;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 32px;
}

.feature-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  font-size: 1.5rem;
}

.feature-icon.ai-models { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
.feature-icon.smart-chat { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; }
.feature-icon.customization { background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; }
.feature-icon.multimodal { background: linear-gradient(135deg, #43e97b, #38f9d7); color: white; }
.feature-icon.security { background: linear-gradient(135deg, #fa709a, #fee140); color: white; }
.feature-icon.cost-effective { background: linear-gradient(135deg, #a8edea, #fed6e3); color: #333; }

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 12px;
}

.feature-card p {
  color: #636e72;
  line-height: 1.6;
}

/* CTA Section */
.cta-section {
  padding: 100px 0 100px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.cta-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 24px;
  text-align: center;
}

.cta-title {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 16px;
  letter-spacing: -0.02em;
}

.cta-description {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 32px;
  font-weight: 500;
}

.cta-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.cta-button {
  padding: 16px 32px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
}

.cta-button.primary {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 24px rgba(255, 255, 255, 0.3);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(255, 255, 255, 0.4);
}

.cta-button.secondary {
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  background: transparent;
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 48px;
    text-align: center;
  }
  
  .hero-title {
    font-size: 48px;
  }
  
  .hero-description {
    font-size: 18px;
  }
  
  .section-title {
    font-size: 40px;
  }
  
  .section-subtitle {
    font-size: 18px;
  }
}

@media (max-width: 768px) {
  .section-container {
    padding: 0 16px;
  }
  
  .hero-section {
    padding: 40px 0 60px;
  }
  
  .hero-title {
    font-size: 36px;
  }
  
  .hero-description {
    font-size: 16px;
  }
  
  .hero-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .hero-stats {
    justify-content: center;
  }
  
  .floating-card {
    position: static;
    margin-bottom: 20px;
    animation: none;
  }
}
</style>