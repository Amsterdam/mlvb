<!--Example of a component with a link and how to watch for state changes-->
<template>
  <div>
    <leaflet-map></leaflet-map>
    <card>
       <div v-for="feature in currentSigns.features" v-bind:key="feature.mslink">{{feature}}</div>
    </card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import card from './Layout/Card'
import leafletMap from './leafletMap'
import currentSigns from '.././data/current_traffic_signs_d02ro_bb22.json'

export default {
  name: 'mlvb',
  components: {
    'card': card,
    'leaflet-map': leafletMap
  },
  data () {
    return {
      currentSigns: currentSigns
    }
  },
  computed: {
    ...mapGetters([
      'text'
    ])
  },
  methods: {
    ...mapActions({
      setText: 'setText'
    })
  },
  watch: {
    'text' (to, from) {
      // Example of a state change watch
      console.log('text has changed', from, to)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
