// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'leaflet/dist/leaflet.css'
import '../static/app.scss'

import Vue from 'vue'
import { mapGetters, mapActions } from 'vuex'

import axios from 'axios'
import VueAxios from 'vue-axios'

import App from './App'
import router from './router'
import store from './store'
import { readData } from './services/datareader'
import vSelect from 'vue-select'

Vue.use(VueAxios, axios)
Vue.config.productionTip = false

Vue.component('v-select', vSelect)

/* eslint-disable no-new */
let vueApp = new Vue({
  el: '#app',
  router,
  store,
  components: {
    App
  },
  template: '<App/>',
  computed: {
    ...mapGetters([
      'text'
    ])
  },
  methods: {
    ...mapActions({
      setText: 'setText'
    }),
    async init () {
      const url = 'https://jsonplaceholder.typicode.com/posts/1'
      let data = await readData(url)
      this.setText(data.title)
    }
  }
})

vueApp.init()
