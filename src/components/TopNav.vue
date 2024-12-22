<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeSection = ref('')

// 使用明確的類型定義
type SectionItem = { id: string; label: string }
type SectionsMap = {
  [key: string]: SectionItem[]
}

const sections: SectionsMap = {
  '/personal-analytics': [
    { id: 'progress', label: '學習進度' },
    { id: 'skills', label: '技能評估' },
    { id: 'attendance', label: '出席統計' },
    { id: 'performance', label: '綜合表現' }
  ],
  '/predictive-analysis': [
    { id: 'knn', label: 'KNN分析' },
    { id: 'kmeans', label: 'K-means分群' },
    { id: 'mlp', label: '深度學習預測' },
    { id: 'decision-tree', label: '決策樹' },
    { id: 'random-forest', label: '隨機森林' }
  ]
}

watch(() => route.path, (newPath) => {
  // 使用可選鏈和空值合併運算符
  activeSection.value = sections[newPath]?.[0]?.id ?? ''
})

const scrollToSection = (sectionId: string) => {
  activeSection.value = sectionId
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <nav v-if="sections[route.path]" class="top-nav">
    <div class="nav-sections">
      <button
        v-for="section in sections[route.path]"
        :key="section.id"
        :class="{ active: activeSection === section.id }"
        @click="scrollToSection(section.id)"
      >
        {{ section.label }}
      </button>
    </div>
  </nav>
</template>

<style scoped>
.top-nav {
  position: sticky;
  top: 0;
  background-color: white;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.nav-sections {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

button {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  color: var(--text-color);
  font-weight: 600;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

button:hover {
  background-color: var(--accent-color);
  transform: translateY(-2px);
}

button.active {
  background-color: var(--primary-color);
  color: white;
}
</style>