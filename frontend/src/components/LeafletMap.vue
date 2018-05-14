<template>
<div>
  <div>
    <ul>
      <li v-for="sign in signs">
        <input v-model="sign.visible" type="checkbox"> {{sign.id}} 
      </li>
    </ul>
  </div>
  <div>
    <l-map style="min-height: 600px" :bounds= "geosearchSelected" :zoom="zoom" :center="center" >
      <l-tile-layer :url="topoUrl" :options="mapOptions"></l-tile-layer>
      <!-- <l-geo-json :geojson="currentSignsD02.geojson"  :options="currentSignsD02.options"></l-geo-json>-->
      <!--<l-geo-json :geojson="detectedSignsD02.geojson"  :options="detectedSignsD02.options"></l-geo-json>-->
      <!--<v-geosearch :options="geosearchOptions" ></v-geosearch>-->
      <!-- <l-control-layers :position="layersPosition"/>-->
      <l-layer-group v-for="sign in signs" :visible="sign.visible">
        <l-marker v-for="item in sign.features"
          :key="sign.id"
          :icon="sign.icon"
          :visible="sign.visible"
          :lat-lng="{
            lat:item.geometry.coordinates[1],
            lng:item.geometry.coordinates[0]}" @click="setLocationData(item.properties)">
        </l-marker>
      </l-layer-group>
    </l-map>
  </div>
</div>
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
  LLayerGroup,
  //LControlLayers,
  LMarker
} from 'vue2-leaflet'
// import { OpenStreetMapProvider } from 'leaflet-geosearch'
// import VGeosearch from './Vue2LeafletGeosearch'

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
      'locationData',
      'geosearchSelected'
    ])
  },
  watch: {
    'geosearchSelected' (to, from) {
      // Example of a state change watch
      console.log('geosearchSelected has changed', from, to)
    }
  },
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LMarker,
    //LControlLayers,
    // VGeosearch
    LLayerGroup
  },
  data () {
    return {
      zoom: 12,
      center: [52.353, 4.90],
      // crs: rd,
      topoUrl: 'https://{s}.data.amsterdam.nl/topo_wm/{z}/{x}/{y}.png',
      layersPosition: 'topright',
      mapOptions: {
        minZoom: 6,
        maxZoom: 23,
        subdomains: ['t1', 't2', 't3', 't4']
      },
      // geosearchOptions: {
      //  provider: new OpenStreetMapProvider({
      //    params: {
      //      viewbox: '4.58199,52.2496,5.22606,52.45936'
      //    }
      //  }),
      //  showMarker: false,
      //  style: 'bar',
      //  autoClose: true
      // },
      signs: [
        { type: 'current',
          id: 'currentD02',
          features: currentSignsD02Json.features,
          icon: L.icon({
            iconUrl: 'static/images/d02.svg',
            iconSize: [10, 10],
            iconAnchor: [5, 5],
            popupAnchor: [0, -37]
          })
        },
        { type: 'detected',
          id: 'detectedD02',
          features: detectedSignsD02Json.features,
          icon: L.icon({
            iconUrl: 'static/images/d02_ml.svg',
            iconSize: [10, 10],
            iconAnchor: [5, 5],
            popupAnchor: [0, -37]
          })
        }]
    }
  }
}
</script>
