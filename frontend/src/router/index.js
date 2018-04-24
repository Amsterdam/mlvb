import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.ROUTER_BASE,
  routes: [
    {
      path: '/',
      name: '',
      component: Main
    }
  ]
})
