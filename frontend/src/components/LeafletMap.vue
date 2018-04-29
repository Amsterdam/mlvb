<template>
    <l-map style="min-height: 600px" :zoom="zoom" :center="center" >
      <l-tile-layer :url="topoUrl" :options="mapOptions"></l-tile-layer>
      <l-geo-json :geojson="currentTrafficSigns.geojson"  :options="currentTrafficSigns.options"></l-geo-json>
      <v-geosearch :options="geosearchOptions" ></v-geosearch>
      <!--<l-marker v-for="item in currentTrafficSigns.geojson" :key="item.id" :lat-lng="item.geometry.coordinates"></l-marker>-->
    </l-map>
    <!--<div id='bla'>
      <button
        type="button"
        class="btn btn-primary"
        @click="setPanoUrl('any other text')">
        Change text
      </button>
    </div>-->
</template>
<script>
// import Vue from 'vue'
import {
  mapGetters,
  mapActions
} from 'vuex'
import L from 'leaflet'
import store from '../store'
// import PopupContent from './GeoJson2Popup'
import data from '../data/nearest_panos_d02_gele_koker_2018-04-28.json'
// import { rd, rdToWgs84 } from '../services/geojson'
import {
  LMap,
  LTileLayer,
  LGeoJson
} from 'vue2-leaflet'
import { OpenStreetMapProvider } from 'leaflet-geosearch'
import VGeosearch from './Vue2LeafletGeosearch'

var baseIcon = L.icon({
  iconUrl: 'static/images/marker.svg',
  iconSize: [25, 30],
  iconAnchor: [16, 37],
  popupAnchor: [0, -37]
})

var hooverIcon = L.icon({
  iconUrl: 'static/images/marker_hoover.svg',
  iconSize: [30, 35],
  iconAnchor: [17, 39],
  popupAnchor: [0, -37]
})

var selectedMarker = null

var selectedIcon = L.icon({
  iconUrl: 'static/images/marker_selected.svg',
  iconSize: [30, 35],
  iconAnchor: [17, 39],
  popupAnchor: [0, -37]
})

function onEachFeature (feature, layer) {
  layer.on('mouseover', function (e) {
    layer.setIcon(hooverIcon)
  })
  layer.on('mouseout', function (e) {
    if (selectedMarker !== e.target) {
      layer.setIcon(baseIcon)
    }
    if (selectedMarker === e.target) {
      layer.setIcon(selectedIcon)
    }
  })
  layer.on('click', function (e) {
    if (selectedMarker !== null) {
      selectedMarker.setIcon(baseIcon)
    }
    selectedMarker = e.target
    store.state.locationData = e.sourceTarget.feature.properties
    layer.setIcon(selectedIcon)
  })
}
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
      setMarkerSelected: 'setMarkerSelected'
    })
  },
  computed: {
    ...mapGetters([
      'markerSelected'
    ])
  },
  watch: {
    'markerSelected' (to, from) {
      // Example of a state change watch
      console.log('markerSelec has changed', from, to)
    }
  },
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
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
        provider: new OpenStreetMapProvider(),
        showMarker: false,
        style: 'bar',
        autoClose: true
      },
      currentTrafficSigns: {
        geojson: data.features,
        options: {
          pointToLayer: function (feature, latlng) {
            let marker = L.marker(latlng, {icon: baseIcon})
            return marker
          },
          onEachFeature: onEachFeature
        }
      }
    }
  }
}
</script>
