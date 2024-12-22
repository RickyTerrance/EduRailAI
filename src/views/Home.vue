<script setup lang="ts">
const features = [
  {
    title: '專業領域學習規劃',
    description: '提供量身定制的學習藍圖，協助學習者選擇適合的專業領域',
    image: '../src/assets/PERSONAL_L.png', // 使用 public 路徑
  },
  {
    title: '性向測業對比分析',
    description: '利用機器和深度學習技術，提供性向對比分析',
    image: '../src/assets/PREDICT.png', // 使用 public 路徑
  },
  {
    title: '學習方向疑難雜症',
    description: '解決學習中的問題，幫助學習者克服挑戰、規劃進度',
    image: '../src/assets/DATA.png', // 使用 public 路徑
  }
];
</script>


<template>
  <div class="home">
    <div class="hero">
      <img 
        src="../assets/MAIN_BACKGROUND.png" 
        alt="Education Banner"
        class="hero-image"
      >
      <div class="hero-content">
        <h1></h1>
        <p class="hero-description">
          
        </p>
      </div>
    </div>

    <div class="features">
      <div v-for="feature in features" :key="feature.title" class="feature-card">
        <div class="feature-image-container">
          <img :src="feature.image" :alt="feature.title" class="feature-image">
        </div>
        <div class="feature-content">
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </div>

    <div class="stats-section">
      <div class="stat-card">
        <h4>學習風格，自由搭配</h4>
        <div class="stat-number">模組化</div>
      </div>
      <div class="stat-card">
        <h4>AI輔助，即時監控</h4>
        <div class="stat-number">智慧化</div>
      </div>
      <div class="stat-card">
        <h4>多種圖表，分析數據</h4>
        <div class="stat-number">可視化</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 0;
}

.hero {
  position: relative;
  height: 400px;
  overflow: hidden;
  margin-bottom: 3rem;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.7);
}

.hero-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: white;
  width: 80%;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-description {
  font-size: 1.2rem;
  max-width: 600px;
  margin: 0 auto;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.feature-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.feature-image-container {
  height: 200px;
  overflow: hidden;
}

.feature-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-image {
  transform: scale(1.05);
}

.feature-content {
  padding: 1.5rem;
}

.feature-content h3 {
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.feature-content p {
  color: var(--text-color);
  line-height: 1.6;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  padding: 2rem;
  margin-top: 2rem;
  background-color: var(--accent-color);
}

.stat-card {
  background-color: var(--card-bg);
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card h4 {
  color: var(--primary-color);
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: rgb(7, 2, 31);
}
</style>