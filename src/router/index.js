import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import RecipesView from '../views/RecipesView.vue'
import PlansView from '../views/PlansView.vue'

const routes = [
  { path: '/', component: DashboardView },
  { path: '/recipes', component: RecipesView},
  { path: '/plans', component: PlansView}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router