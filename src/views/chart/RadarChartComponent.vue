<script setup lang="ts">
import { computed } from 'vue'
import { Radar } from 'vue-chartjs'
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js'

// Register necessary Chart.js components
ChartJS.register(
  RadialLinearScale, 
  PointElement, 
  LineElement,
  Filler,
  Tooltip, 
  Legend
)

// Define a more precise interface for chart dataset
interface RadarDataset {
  label: string
  data: number[]
  backgroundColor: string
  borderColor: string
}

// Define props interface
interface Props {
  chartData: {
    labels: string[]
    datasets: RadarDataset[]
  }
}

// Default options with fill and connection
const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
      labels: {
        font: {
          size: 14,
        },
        color: '#333',
      },
    },
  },
  elements: {
    line: {
      borderWidth: 3,
      fill: true,
    }
  },
  scales: {
    r: {
      angleLines: {
        display: true,
        color: 'rgba(0,0,0,0.1)'
      },
      grid: {
        color: 'rgba(0,0,0,0.1)'
      },
      pointLabels: {
        font: {
          size: 12,
          color: '#333'
        }
      },
      suggestedMin: 0,
      suggestedMax: 100
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
  <Radar 
    :data="data" 
    :options="options" 
  />
</template>