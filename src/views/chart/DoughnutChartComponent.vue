<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

// Register Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  ArcElement
)

// Define a more precise interface for chart dataset
interface DoughnutDataset {
  data: number[]
  backgroundColor: string[]
}

// Define props interface
interface Props {
  chartData: {
    labels: string[]
    datasets: DoughnutDataset[]
  }
}

// Chart options
const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
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
        data: [],
        backgroundColor: ['rgba(0,0,0,0.1)']
      }
    ]
  })
})
</script>

<template>
  <Doughnut 
    :data="data" 
    :options="options" 
  />
</template>