import { createRouter, createWebHistory } from 'vue-router'

// 导入各个页面组件
import HomePage from '../views/HomePage.vue'
import DataView from '../views/DataView.vue'
import HelpPage from '../views/HelpPage.vue'
import NoticePage from '../views/NoticePage.vue'

const routes = [
  {
    path: '/',
    redirect: '/data/view' // 默认跳转到"流域数据"页面
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/data/view',
    name: 'DataView',
    component: DataView
  },
  {
    path: '/help',
    name: 'Help',
    component: HelpPage
  },
  {
    path: '/notice',
    name: 'Notice',
    component: NoticePage
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router