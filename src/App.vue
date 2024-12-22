<script setup lang="ts">
import { ref, provide } from 'vue'
import SideNav from './components/SideNav.vue'
import TopNav from './components/TopNav.vue'
import ChatAssistant from './components/ChatAssistant.vue'

const isNavCollapsed = ref(false)
provide('isNavCollapsed', isNavCollapsed)
</script>

<template>
  <div class="app">
    <SideNav v-model:collapsed="isNavCollapsed" />
    <main :class="['page-container', { 'sidenav-collapsed': isNavCollapsed }]">
      <TopNav />
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
    <ChatAssistant />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.app {
  min-height: 100vh;
  background-color: var(--secondary-color);
}

.page-container {
  padding: 0;
  margin-left: 250px;
  transition: margin-left 0.3s ease;
}

.page-container.sidenav-collapsed {
  margin-left: 60px;
}
</style>