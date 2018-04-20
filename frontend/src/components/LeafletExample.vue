<!--Example of a component that uses Leaflet-->
<template>
  <div>
    <h2>Amsterdam</h2>
    <div :ref="mapRef" class="map"></div>
  </div>
</template>

<script>
import { amsMap } from '@/services/map.js'

export default {
  data () {
    return {
      mapRef: `${this._uid}.leafletExample`
    }
  },
  mounted () {
    amsMap(this.$refs[this.mapRef])
  }
}
</script>

<style scoped>
.map {
  height: 300px
}
</style>
