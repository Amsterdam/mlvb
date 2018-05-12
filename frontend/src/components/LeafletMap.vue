<template>
    <l-map style="min-height: 600px" :zoom="zoom" :center="center" >
      <l-tile-layer :url="topoUrl" :options="mapOptions"></l-tile-layer>
      <!-- <l-geo-json :geojson="currentSignsD02.geojson"  :options="currentSignsD02.options"></l-geo-json>-->
      <!--<l-geo-json :geojson="detectedSignsD02.geojson"  :options="detectedSignsD02.options"></l-geo-json>-->
      <v-geosearch :options="geosearchOptions" ></v-geosearch>
      <l-marker v-for="item in currentSignsD02.features"
        :key="item.id"
        :icon="currentSignsD02.icon"
        :lat-lng="{
          lat:item.geometry.coordinates[1],
          lng:item.geometry.coordinates[0]}" @click="setLocationData(item.properties)">
      </l-marker>
      <l-marker v-for="item in detectedSignsD02.features"
        :key="item.id"
        :icon="detectedSignsD02.icon"
        :lat-lng="{
          lat:item.geometry.coordinates[1],
          lng:item.geometry.coordinates[0]}" @click="setLocationData(item.properties)">
      </l-marker>
    </l-map>
</template>
<script>
// import Vue from 'vue'
import {
  mapGetters,
  mapActions
} from 'vuex'
import L from 'leaflet'
// import store from '../store'
// import PopupContent from './GeoJson2Popup'
import currentSignsD02Json from '../data/nearest_panos_d02_gele_koker_2018-04-28.json'
import detectedSignsD02Json from '../data/2018-05-11-detections-vluchtheuvel-bakens-panos.json'
// import { rd, rdToWgs84 } from '../services/geojson'
import {
  LMap,
  LTileLayer,
  LGeoJson,
  LMarker
} from 'vue2-leaflet'
import { OpenStreetMapProvider } from 'leaflet-geosearch'
import VGeosearch from './Vue2LeafletGeosearch'

// function onEachFeature (feature, layer) {
//   let PopUpContent = Vue.extend(PopupContent)
//   let popup = new PopUpContent({
//     propsData: {
//       coordinates: feature.geometry.coordinates,
//       mslink: feature.properties.mslink,
//       bordnummer: feature.properties.mldnr,
//       pano_url: feature.properties.url
//     }
//   })
//   layer.bindPopup(popup.$mount().$el)
// }

export default {
  name: 'example',
  methods: {
    ...mapActions({
      setLocationData: 'setLocationData'
    })
  },
  computed: {
    ...mapGetters([
      'locationData'
    ])
  },
  watch: {
    'markerSelected' (to, from) {
      // Example of a state change watch
      console.log('markerSelected has changed', from, to)
    }
  },
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LMarker,
    VGeosearch
  },
  data () {
    return {
      zoom: 12,
      center: [52.353, 4.90],
      // crs: rd,
      topoUrl: 'https://{s}.data.amsterdam.nl/topo_wm/{z}/{x}/{y}.png',
      mapOptions: {
        minZoom: 6,
        maxZoom: 23,
        subdomains: ['t1', 't2', 't3', 't4']
      },
      geosearchOptions: {
        provider: new OpenStreetMapProvider({
          params: {
            city: 'Amsterdam'
          }
        }),
        showMarker: false,
        style: 'bar',
        autoClose: true
      },
      currentSignsD02: {
        features: currentSignsD02Json.features,
        icon: L.icon({
          iconUrl: 'static/images/d02.svg',
          iconSize: [10, 10],
          iconAnchor: [5, 5],
          popupAnchor: [0, -37]
        })
      },
      detectedSignsD02: {
        features: detectedSignsD02Json.features,
        icon: L.icon({
          iconUrl: 'static/images/d02_ml.svg',
          iconSize: [10, 10],
          iconAnchor: [5, 5],
          popupAnchor: [0, -37]
        })
      }
    }
  }
}
</script>
