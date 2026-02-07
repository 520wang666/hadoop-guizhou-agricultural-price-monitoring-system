import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '数据看板', requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/price/trend',
    name: 'PriceTrend',
    component: () => import('@/views/PriceTrend.vue'),
    meta: { title: '价格趋势', requiresAuth: true }
  },
  {
    path: '/price/compare',
    name: 'PriceCompare',
    component: () => import('@/views/PriceCompare.vue'),
    meta: { title: '价格对比', requiresAuth: true }
  },
  {
    path: '/market/map',
    name: 'MarketMap',
    component: () => import('@/views/MarketMap.vue'),
    meta: { title: '市场地图', requiresAuth: true }
  },
  {
    path: '/alert/list',
    name: 'AlertList',
    component: () => import('@/views/AlertList.vue'),
    meta: { title: '预警列表', requiresAuth: true }
  },
  {
    path: '/prediction',
    name: 'Prediction',
    component: () => import('@/views/Prediction.vue'),
    meta: { title: '价格预测', requiresAuth: true }
  },
  {
    path: '/report',
    name: 'Report',
    component: () => import('@/views/Report.vue'),
    meta: { title: '报表导出', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} - 农产品价格监测系统`
  
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path.path === '/login' && userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
