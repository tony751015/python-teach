import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'
// import ChatList from '../views/ChatList.vue'
// import WoundChat from '../views/WoundChat.vue'
// import WoundLogin from '../views/WoundLogin.vue'

const ChatList = () => import('../views/ChatList.vue');
const WoundChat = () => import('../views/WoundChat.vue');
const WoundLogin = () => import('../views/WoundLogin.vue');
const Error404 = () => import('../views/Error404.vue');
const Error500 = () => import('../views/Error500.vue');

Vue.use(VueRouter)

const routes = [
  // {
  //   path: '/',
  //   name: 'home',
  //   component: HomeView
  // },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // },
  {
    path:'/',
    name:'woundLogin',
    component: WoundLogin
  },
  {
    path: '/chat',
    name: 'chat-list',
    component: ChatList
  },
  {
    path: '/chat/:id',
    name: 'chat-room',
    component: WoundChat
  },
  {
    path: '/404',
    name: 'error404',
    component: Error404,
  },
  {
    path: '/500',
    name: 'error500',
    component: Error500,
  },
  {
    path: '*',
    redirect: { name: 'error404' },
  },
]

const router = new VueRouter({
  mode: 'history',
  routes,
  // scrollBehavior(to, from, savedPosition) {
  //   let returnValue;

  //   if (savedPosition) {
  //     returnValue = savedPosition;
  //   }

  //   return returnValue;
  // },
})

export default router
