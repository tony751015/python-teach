import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import ChatList from '../views/ChatList.vue'
import WoundChat from '../views/WoundChat.vue'
import WoundLogin from '@/views/WoundLogin.vue'

Vue.use(VueRouter)

const routes = [
  // {
  //   path: '/',
  //   name: 'home',
  //   component: HomeView
  // },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path:'/',
    name:'woundLogin',
    component: WoundLogin
  },
  {
    path: '/chat',
    name: 'ChatList',
    component: ChatList
  },
  {
    path: '/chat/:id',
    name: 'WoundChat',
    component: WoundChat
  }
  
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
