<template>
  <div>
    <l-map style="height: 700px" :zoom="zoom" :center="center" >
      <l-tile-layer :url="url" :options="options"></l-tile-layer>
      <l-geo-json :geojson="currentTrafficSigns.geojson" :options="currentTrafficSigns.options"></l-geo-json>
    </l-map>
      <div id='bla'></div>
  </div>
</template>
<script>
// import Vue from 'vue'
import L from 'leaflet'
// import popupContent from './GeoJson2Popup'
import data from '../data/current_traffic_signs_d02ro_bb22_wgs84.json'
// import { rd, rdToWgs84 } from '../services/geojson'
import { LMap, LTileLayer, LGeoJson } from 'vue2-leaflet'

var baseIcon = L.icon({
  iconUrl: 'static/images/marker.svg',
  iconSize: [25, 30],
  iconAnchor: [16, 37],
  popupAnchor: [0, -28]
})

export default {
  name: 'example',
  components: {
    LMap,
    LTileLayer,
    LGeoJson
  },
  data () {
    return {
      zoom: 12,
      center: [52.353, 4.90],
      // crs: rd,
      url: 'https://{s}.data.amsterdam.nl/topo_wm/{z}/{x}/{y}.png',
      options: {
        minZoom: 6,
        maxZoom: 23,
        subdomains: ['t1', 't2', 't3', 't4']
      },
      currentTrafficSigns: {
        geojson: data.features,
        options: {
          pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {icon: baseIcon})
          }
        }
      }
    }
  }
}
</script>
