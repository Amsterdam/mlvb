<!--Example of a component with a link and how to watch for state changes-->
<template>
  <div class="row">
    <div class="col mt-2">
      <leaflet-map></leaflet-map>
    </div>
    <div class="col mt-1">
      <pano-view></pano-view>
    </div>
  </div>
</template>

<script>
import card from './Layout/Card'
import leafletMap from './LeafletMap'
import panoView from './Pano.vue'

export default {
  name: 'mlvb',
  components: {
    'card': card,
    'leaflet-map': leafletMap,
    'pano-view': panoView
  },
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.row {
  margin-left: 30px;
  margin-right: 0px;
}
</style>
