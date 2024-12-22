<script setup lang="ts">
import { useRoute } from 'vue-router'
import { RouterLink } from 'vue-router'

// Define allowed route paths type
type AllowedRoutePaths = '/' | '/personal-analytics' | '/personal-files' | '/blueprint' | '/socialmedia' | '/infor' | '/future' | '/group'

// Define menu item interface
interface MenuItem {
  path: AllowedRoutePaths
  label: string
  icon: string
}

// Define submenu item interface
interface SubMenuItem {
  label: string
  hash: string
}

// Define props type
interface SidenavProps {
  collapsed: boolean
}

// Props definition with type
const props = defineProps<SidenavProps>()

// Emits definition with type
const emit = defineEmits<{
  (e: 'update:collapsed', value: boolean): void
}>()

const route = useRoute()

// Typed main menu items
const mainMenuItems: MenuItem[] = [
  { path: '/', label: '首頁', icon: '🏠' },
  { path: '/personal-analytics', label: '分析結果', icon: '📊' },
  { path: '/personal-files', label: '個人檔案', icon: '🪪' },
  { path: '/group', label: '學群分析', icon: '🔍' },
  { path: '/blueprint', label: '藍圖解析', icon: '💡' },
  { path: '/socialmedia', label: '社群論壇', icon: '🌐' },
  { path: '/infor', label: '更多資訊', icon: '⚙️' },
  { path: '/future', label: '未來展望', icon: '💻' }
]

// Typed submenu items with explicit allowed route paths
const subMenuItems: Record<AllowedRoutePaths, SubMenuItem[]> = {
  '/': [],
  '/infor': [],
  '/personal-analytics': [

  ],
  '/personal-files': [
    
  ],
  '/blueprint': [
    
  ],
  '/socialmedia': [
    
  ],
  '/future': [

  ],
  '/group': [
    { label: '全學群性向分析', hash: '#Engineering' },
     /*
    { label: '藝術學群性向分析', hash: '#skills' },
    { label: '管理學群性向分析', hash: '#attendance' },
    { label: '跨域學群性向分析', hash: '#CrossDomain' }
     */
  ]
}

// Toggle navigation method
const toggleNav = () => {
  emit('update:collapsed', !props.collapsed);
};

// Default logo with explicit typing
const defaultLogo = 'src/assets/EduRail.png' as const
</script>

<template>
  <div class="sidenav" :class="{ 'collapsed': collapsed }">
    <div class="nav-content">
      <div class="brand-section" :class="{ 'collapsed': collapsed }">
        <div class="logo-container">
          <img :src="defaultLogo" alt="Brand Logo" class="brand-logo" />
        </div>

      </div>

      <button class="toggle-btn" @click="toggleNav">
        {{ collapsed ? '→' : '←' }}
      </button>
      
      <div class="nav-links">
        <div v-for="item in mainMenuItems" :key="item.path" class="nav-item">
          <RouterLink 
            :to="item.path" 
            class="nav-link"
            :class="{ active: route.path === item.path }"
          >
            <span class="icon">{{ item.icon }}</span>
            <span class="label">{{ item.label }}</span>
          </RouterLink>
          
          <div v-if="!collapsed && 
                     subMenuItems[item.path as AllowedRoutePaths]?.length && 
                     route.path === item.path" 
               class="sub-menu">
            <a v-for="subItem in subMenuItems[item.path as AllowedRoutePaths]"
               :key="subItem.hash"
               :href="item.path + subItem.hash"
               class="sub-menu-link">
              {{ subItem.label }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.sidenav {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 250px;
  background-color: var(--primary-color);
  transition: all 0.3s ease;
  z-index: 1000;
  overflow-y: auto;
}

.nav-content {
  position: relative;
  height: 100%;
  padding: 0;
}

.brand-section {
  background-color: rgb(42, 12, 61);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.brand-section.collapsed {
  padding: 1rem;
  justify-content: center;
}

.logo-container {
  width: 250px;
  height: 100px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.brand-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.brand-name {
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0;
}

.collapsed {
  width: 60px;
}

.toggle-btn {
  position: absolute;
  right: 0px;
  top: 90px;
  background-color: rgb(255, 255, 255);
  color: var(--primary-color);
  border-radius: 8%;
  width: 28px;
  height: 50px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 2;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.2rem;
  font-weight: bold;
}

.toggle-btn:hover {
  transform: scale(1.1);
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
}

.nav-item {
  display: flex;
  flex-direction: column;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--secondary-color);
  text-decoration: none;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateX(5px);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.3);
  font-weight: bold;
}

.icon {
  font-size: 1.2rem;
  min-width: 24px;
  text-align: center;
}

.collapsed .label {
  display: none;
}

.sub-menu {
  margin-left: 40px;
  margin-top: 5px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sub-menu-link {
  color: var(--secondary-color);
  text-decoration: none;
  padding: 8px;
  border-radius: 4px;
  font-size: 0.9rem;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.sub-menu-link:hover {
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.collapsed .sub-menu {
  display: none;
}
</style>