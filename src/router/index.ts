import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PersonalAnalytics from '../views/PersonalAnalytics.vue'
import PersonalFiles from '../views/PersonalFile.vue'
import Blueprint from '../views/Blue.vue'
import Social from '../views/Media.vue'
import Infor from '../views/infor.vue'
import Future from '../views/Future.vue'
import LGroup from '../views/LGroup.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/personal-analytics',
      name: 'PersonalAnalytics',
      component: PersonalAnalytics
    },
    {
      path: '/personal-files',
      name: 'PersonalFiles',
      component: PersonalFiles
    },
    {
      path: '/blueprint',
      name: 'Blueprint',
      component: Blueprint
    },
    {
      path: '/socialmedia',
      name: 'SocialMedia',
      component: Social
    },
    {
      path: '/infor',
      name: 'Infor',
      component: Infor
    },
    {
      path: '/future',
      name: 'Future',
      component: Future
    },
    {
      path: '/group',
      name: 'LGroup',
      component: LGroup
    }
  ]
})

export default router