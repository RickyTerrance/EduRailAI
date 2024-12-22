<script setup lang="ts">
import { ref } from 'vue';

interface TeamMember {
  name: string;
  role: string;
  description: string;
  photo?: File;
  photoUrl?: string;
}

const teamMembers = ref<TeamMember[]>([
 {
    name: '大語言模型智慧助理',
    role: 'LLM 技術專家',
    description: '負責提供基於大語言模型的智慧問答功能，涵蓋自然語言處理、語音交互與數據分析，為團隊提供創新技術支援。',
    photoUrl: '/src/assets/1.png'
  },
  {
    name: '學習風格分析',
    role: '學習行為分析與個性化推薦',
    description: '專注於分析學生的學習風格，根據學生的學習習慣與偏好提供個性化的學習內容和建議。此模組透過數據挖掘技術，幫助提升學生的學習效果與參與度。',
    photoUrl: '/src/assets/3.png'
  },
  {
    name: 'AI筆記系統',
    role: '智慧筆記與知識管理',
    description: '開發基於AI的筆記系統，能夠自動化整理、摘要與標註學習內容，並根據學生的需求提供智能化的學習回顧和推薦，提升學習效率。',
    photoUrl: '/src/assets/4.png'
  },
    {
    name: '模組化預測分析系統',
    role: '系統設計與數據建模',
    description: '負責開發可拓展的模組化預測分析系統，支援多場景的數據處理、模型訓練與結果可視化，提升系統的實用性與效率。',
    photoUrl: '/src/assets/2.png'
  },

]);

const handlePhotoUpload = (event: Event, index: number) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    const file = input.files[0];
    teamMembers.value[index].photo = file;
    teamMembers.value[index].photoUrl = URL.createObjectURL(file);
  }
};
</script>

<template>
  <div class="team">
    <h1>未來展望</h1>
    <div class="team-grid">
      <div
        v-for="(member, index) in teamMembers"
        :key="member.name"
        class="team-card"
      >
        <div class="photo-container">
          <div v-if="!member.photoUrl" class="photo-placeholder">
            <label :for="'photo-upload-' + index" class="upload-label">
              <span class="upload-icon">📷</span>
              <span>匯入照片</span>
            </label>
            <input
              :id="'photo-upload-' + index"
              type="file"
              accept="image/*"
              class="photo-input"
              @change="(e) => handlePhotoUpload(e, index)"
            />
          </div>
          <img
            v-else
            :src="member.photoUrl"
            :alt="member.name"
            class="member-photo"
          />
        </div>
        <div class="member-info">
          <h3>{{ member.name }}</h3>
          <h4>{{ member.role }}</h4>
          <p>{{ member.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.team {
  padding: 20px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  margin-top: 20px;
}

.team-card {
  background-color: var(--card-bg);
  border-radius: 16px;
  overflow: hidden;
  width: 750px; /* 卡片寬度 */
  height: 650px; /* 卡片高度，增加整體高度以容納更大的照片 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.photo-container {
  height: 380px; /* 增加圖片容器高度 */
  width: 100%;
  background-color: #f8f9fa;
  position: relative;
}

.photo-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  cursor: pointer;
}

.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.upload-icon {
  font-size: 2rem;
}

.photo-input {
  display: none;
}

.member-photo {
  width: 100%;
  height: 110%;
  object-fit: cover;
}

.member-info {
  padding: 1.5rem; /* 調整內邊距 */
  line-height: 1.6; /* 增加行間距，提升可讀性 */
  letter-spacing: 0.05rem; /* 增加字間距，讓文字更精緻 */
  text-align: center; /* 文字居中對齊，可選 center, left, right, justify */
  border-top: 2px solid var(--primary-color); /* 增加上方分隔線 */
  background-color: #f9f9f9; /* 添加淺色背景讓區塊更突出 */
  border-radius: 0 0 16px 16px; /* 圓角，只應用於區塊底部 */
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); /* 增加一點陰影讓區塊更有層次感 */
}

.member-info h3 {
  color: var(--primary-color); 
}

.team-card h3 {
  color: var(--primary-color);
  margin-bottom: 10px;
  font-weight: 800;
  font-size: 1.2rem; 
}

.team-card h4 {
  color: var(--text-color);
  margin: 5px 0;
  font-weight: 600;
  line-height: 2;
  font-size: 1rem; /* 調整標題大小 */
}

.team-card p {
  color: var(--text-color);
  line-height: 1.6; /* 增加行間距 */
  font-size: 1rem; /* 調整文字大小 */
  letter-spacing: 0.01rem; /* 微調字間距 */
  text-align: left; /* 讓段落文字置左 */
  margin: 10px 0; /* 增加段落上下間距 */
}

@media (max-width: 768px) {
  .team-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
}

</style>
