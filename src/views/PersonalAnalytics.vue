<script setup lang="ts">
import { Bar, Radar, Doughnut, Scatter } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, RadialLinearScale, ArcElement, Title, Tooltip, Legend } from 'chart.js'
import { ref, onMounted } from 'vue'
import * as Papa from 'papaparse'

// 註冊 Chart.js 組件
ChartJS.register(
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  BarElement, 
  RadialLinearScale, 
  ArcElement, 
  Title, 
  Tooltip, 
  Legend
)

// 定義數據接口
interface CSVData {
  user_sn: number
  review_mean_time_spent: number
  review_mean_finish_rate: number
  prac_mean_items_ans_time: number
  prac_mean_binary_res_Q: number
  exam_mean_ans_time_num: number
  exam_mean_binary_res: number
  user_exam_count: number
  user_prac_count: number
  user_review_count: number
  organization_id: number
  total_score: number
  pr: number
  correct_rate: number
  mission_count: number
  question_count: number
}

// 圖表配置
const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,  // 明確指定 position 為字串字面量
      labels: {
        font: {
          size: 14,
        },
        color: '#333',
      },
    },
    tooltip: {
      backgroundColor: 'rgba(0,0,0,0.7)',
      titleFont: { size: 16 },
      bodyFont: { size: 12 },
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: '作業完成率 (%)',
        font: {
          size: 16,
        },
        color: '#333',
      },
      ticks: {
        font: {
          size: 12,
        },
      },
      min: 0,   // 設置 x 軸最小值
      max: 100, // 設置 x 軸最大值
    },
    y: {
      title: {
        display: true,
        text: '平均答題時間 (秒)',
        font: {
          size: 16,
        },
        color: '#333',
      },
      ticks: {
        font: {
          size: 12,
        },
        beginAtZero: true,
      },
    },
  },
  elements: {
    point: {
      radius: 5,
    },
    line: {
      tension: 0.4,
      borderWidth: 2,
    },
    bar: {
      borderWidth: 1,
    }
  },
}


// 定義圖表數據 Refs
const reviewCompletionVsScoreData = ref<{
  datasets: {
    label: string
    data: { x: number, y: number }[]
    backgroundColor: string
    borderColor: string
    pointRadius: number
    pointBackgroundColor: string
  }[]
}>({
  datasets: [
    {
      label: '其他用戶',
      data: [],
      backgroundColor: 'rgba(200, 200, 200, 0.5)',
      borderColor: 'gray',
      pointRadius: 3,
      pointBackgroundColor: 'rgba(200, 200, 200, 0.5)',
    },
    {
      label: '當前用戶',
      data: [],
      backgroundColor: 'rgba(66, 165, 245, 1)',
      borderColor: '#42A5F5',
      pointRadius: 8,
      pointBackgroundColor: '#42A5F5',
    }
  ]
})

const learningEfficiencyData = ref<{
  labels: string[]
  datasets: {
    label: string
    data: number[]
    backgroundColor: string
    borderColor: string
  }[]
}>({
  labels: ['正確率', '任務完成數', '題目數量', '總得分', 'PR值'],
  datasets: [{
    label: '學習效率指標',
    data: [],
    backgroundColor: 'rgba(255, 140, 66, 0.6)',
    borderColor: '#FF8C42',
  }]
})

const practiceData = ref<{
  labels: string[]
  datasets: {
    label: string
    data: number[]
    backgroundColor: string[]
    borderColor: string
  }[]
}>({
  labels: ['二元題正確率', '實作題平均答題時間', '練習次數', '考試次數', '複習次數'],
  datasets: [{
    label: '練習與測驗表現',
    data: [],
    backgroundColor: [
      'rgba(66, 165, 245, 0.6)', 
      'rgba(255, 140, 66, 0.6)', 
      'rgba(102, 187, 106, 0.6)',
      'rgba(255, 89, 89, 0.6)',
      'rgba(171, 71, 188, 0.6)'
    ],
    borderColor: '#42A5F5',
  }]
})
const attendanceData = ref<{
  labels: string[]
  datasets: {
    data: number[]
    backgroundColor: string[]
  }[] }>( {
  labels: ['出席', '請假', '缺席'],
  datasets: [{
    data: [],
    backgroundColor: ['#FF8C42', '#FFB088', '#FFD4B8'],
  }]
})
// 全局變量
let csvData: CSVData[] = []

// Refs
const selectedUser = ref<number | null>(null)
const filteredData = ref<CSVData[]>([])
const uniqueUserIDs = ref<number[]>([])

// 加載 CSV 數據
const loadCSVData = async () => {
  try {
    const response = await fetch('/data.csv')
    const text = await response.text()

    Papa.parse(text, {
      complete: (result) => {
        csvData = result.data.slice(1) as CSVData[]  // 跳過標題行
        uniqueUserIDs.value = Array.from(new Set(csvData.map(user => user.user_sn)))
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

// 根據用戶篩選數據
const filterDataByUser = () => {
  if (selectedUser.value !== null) {
    filteredData.value = csvData.filter((user) => user.user_sn === selectedUser.value);
    const selectedUserData = filteredData.value[0]
    updateChartData(selectedUserData);
  } else {
    alert('請選擇用戶！');
  }
}

// 更新圖表數據
const updateChartData = (selectedUserData: CSVData) => {
  // 作業完成率與測驗成績關聯分析
  const allUserData = csvData.filter(user => user.user_sn !== selectedUserData.user_sn)
  reviewCompletionVsScoreData.value = {
    datasets: [
      {
        label: '其他用戶',
        data: allUserData.map(user => ({
          x: user.review_mean_finish_rate || 0, 
          y: user.exam_mean_ans_time_num || 0
        })),
        backgroundColor: 'rgba(200, 200, 200, 0.5)',
        borderColor: 'gray',
        pointRadius: 3,
        pointBackgroundColor: 'rgba(200, 200, 200, 0.5)',
      },
      {
        label: '當前用戶',
        data: [{
          x: selectedUserData.review_mean_finish_rate || 0, 
          y: selectedUserData.exam_mean_ans_time_num || 0
        }],
        backgroundColor: 'rgba(66, 165, 245, 1)',
        borderColor: '#42A5F5',
        pointRadius: 8,
        pointBackgroundColor: '#42A5F5',
      }
    ]
  }

  // 學習效率指標
  learningEfficiencyData.value = {
    labels: ['正確率', '任務完成數', '題目數量', '總得分', 'PR值'],
    datasets: [{
      label: '學習效率指標',
      data: [
        selectedUserData.correct_rate || 0,
        selectedUserData.mission_count || 0,
        selectedUserData.question_count || 0,
        selectedUserData.total_score || 0,
        selectedUserData.pr || 0
      ],
      backgroundColor: 'rgba(255, 140, 66, 0.6)',
      borderColor: '#FF8C42',
    }]
  }

  // 練習與測驗表現
  practiceData.value = {
    labels: ['二元題正確率', '實作題平均答題時間', '練習次數', '考試次數', '複習次數'],
    datasets: [{
      label: '練習與測驗表現',
      data: [
        selectedUserData.prac_mean_binary_res_Q || 0,
        selectedUserData.prac_mean_items_ans_time || 0,
        selectedUserData.user_prac_count || 0,
        selectedUserData.user_exam_count || 0,
        selectedUserData.user_review_count || 0
      ],
      backgroundColor: [
        'rgba(66, 165, 245, 0.6)', 
        'rgba(255, 140, 66, 0.6)', 
        'rgba(102, 187, 106, 0.6)',
        'rgba(255, 89, 89, 0.6)',
        'rgba(171, 71, 188, 0.6)'
      ],
      borderColor: '#42A5F5',
    }]
  }
  attendanceData.value = {
      labels: ['出席', '請假', '缺席'],
      datasets: [{
        data: [
         selectedUserData.user_exam_count,
         selectedUserData.user_prac_count,
         selectedUserData.user_review_count,
        ],
        backgroundColor: ['#FF8C42', '#FFB088', '#FFD4B8'],
      }]
    }
}
</script>

<template>
  <div class="analytics">
    <h1>個人學習成效查詢</h1>

    <div class="user-password-container">
      <select v-model="selectedUser" @change="filterDataByUser">
        <option value="" disabled selected>選擇用戶</option>
        <option v-for="userId in uniqueUserIDs" :key="userId" :value="userId">
          User {{ userId }}
        </option>
      </select>
    </div>

    <div class="charts-grid">
      <div class="chart-container" v-if="filteredData.length">
        <h3>作業完成率與測驗成績關聯分析</h3>
        <Scatter :data="reviewCompletionVsScoreData" :options="options" />
      </div>


      <div class="chart-container" v-if="filteredData.length">
        <h3>練習與測驗表現</h3>
        <Bar :data="practiceData" :options="options" />
      </div>
      <div class="chart-container" v-if="filteredData.length">
        <h3>學習效率指標</h3>
        <Radar :data="learningEfficiencyData" :options="options" />
      </div>

      <div class="chart-container" v-if="filteredData.length">
        <h3>出席紀錄</h3>
        <Doughnut :data="attendanceData" :options="options" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.analytics {
  padding: 20px;
}

.chart-container {
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 800px;
  height:auto;  /* 調整為較高的固定高度，您可以根據需要增加高度 */
  max-width: 800px;
  margin: 0 auto;
  overflow: hidden;
}

.chart-container canvas {
  width: 100%;
  height: 100%;
  object-fit: contain;  /* 保持圖表比例，不會變形 */
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
  grid-template-rows: auto auto;  /* 調整為自動適應行高 */
}
h1 {
  color: var(--primary-color);
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

h3 {
  color: var(--primary-color);
  margin-bottom: 1rem;
  font-size: 1.5rem; /* 增大字體 */
  font-weight: bold; /* 加粗字體 */
  text-align: center; /* 使子標題居中 */
}

select {
  padding: 8px;
  font-size: 1rem;
}

.user-password-container {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 10px;
}
</style>
