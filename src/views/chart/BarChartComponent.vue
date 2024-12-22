<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

// Register Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
)

// Define a more precise interface for chart dataset
interface BarDataset {
  label: string
  data: number[]
  backgroundColor: string | string[]
  borderColor: string
}

// Define props interface
interface Props {
  chartData: {
    labels: string[]
    datasets: BarDataset[]
  }
}

// Chart options
const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

// Transform chartData to the format vue-chartjs expects
const data = computed(() => ({
  labels: props.chartData.labels,
  datasets: props.chartData.datasets
}))

// Define props with default empty data
const props = withDefaults(defineProps<Props>(), {
  chartData: () => ({
    labels: [],
    datasets: [
      {
        label: 'Default Dataset',
        data: [],
        backgroundColor: 'rgba(0,0,0,0.1)',
        borderColor: 'rgba(0,0,0,0.5)'
      }
    ]
  })
})
</script>

<template>
  <Bar 
    :data="data" 
    :options="options" 
  />
</template>