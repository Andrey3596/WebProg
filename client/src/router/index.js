import { createRouter, createWebHistory } from 'vue-router'

import ProfilesView    from '../views/ProfilesView.vue'
import CategoriesView  from '../views/CategoriesView.vue'
import DishesView      from '../views/DishesView.vue'
import OrdersView      from '../views/OrdersView.vue'
import OrderItemsView  from '../views/OrderItemsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/profiles' },
    { path: '/profiles',   name: 'profiles',   component: ProfilesView },
    { path: '/categories', name: 'categories', component: CategoriesView },
    { path: '/dishes',     name: 'dishes',     component: DishesView },
    { path: '/orders',     name: 'orders',     component: OrdersView },
    { path: '/orderitems', name: 'orderitems', component: OrderItemsView },
  ],
})

export default router