import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Geosearch from '@/components/Geosearch'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.ROUTER_BASE,
  routes: [
    {
      path: '/',
      name: 'mlvb',
      component: Main
    },
    {
      path: '/zoek/',
      name: 'zoek',
      component: Geosearch
    }
  ]
})
