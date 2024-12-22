<script setup lang="ts">
import { onMounted } from 'vue'
import * as Papa from 'papaparse'

// 定義數據接口
interface CSVData {
  group_name: string
  introduction: string
  learning_content: string
  related_groups: string
  compare_subjects: string
  important_subjects: string
  compare_contents: string
  important_contents: string
  chart_description: string
}

// 全局變量
let csvData: CSVData[] = []

// 加載 CSV 數據
const loadCSVData = async () => {
  try {
    const response = await fetch('/backend/college_details_ALL.csv')
    const text = await response.text()

    Papa.parse(text, {
      complete: (result) => {
        csvData = result.data.slice(1) as CSVData[] // 跳過標題行
        console.log(csvData);  // 檢查資料是否正確
      },
      header: true,
      skipEmptyLines: true
    })
  } catch (error) {
    console.error('加載數據失敗:', error)
  }
}

// 掛載時加載數據
onMounted(() => {
  loadCSVData()
})
</script>

<template>
  <div class="analytics">
    <h1>學群資料分析</h1>

    <div class="cards-grid">
      <!-- 遍歷所有學群 -->
      <div v-for="(item, index) in csvData" :key="index" class="card">
        <h2>{{ item.group_name }}</h2>
        <p><strong>介紹:</strong> {{ item.introduction }}</p>
        <p><strong>學習內容:</strong> {{ item.learning_content }}</p>
        <p><strong>相關學群:</strong> {{ item.related_groups }}</p>
        <p><strong>對比學科:</strong> {{ item.compare_subjects }}</p>
        <p><strong>重要學科:</strong> {{ item.important_subjects }}</p>
        <p><strong>對比內容:</strong> {{ item.compare_contents }}</p>
        <p><strong>圖表描述:</strong> {{ item.chart_description }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analytics {
  padding: 20px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.card {
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card h2 {
  color: var(--primary-color);
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.card p {
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.card strong {
  color: var(--primary-color);
}
</style>
