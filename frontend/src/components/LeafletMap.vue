<template>
<div>
  <div>
    <ul>
      <li v-for="sign in signs" :key="sign.signId">
        <img :src="sign.signImage" class="sign">
        <input v-model="sign.visible" title="sign.signDescription" type="checkbox">
        <span class="signSelector">{{sign.signId}}</span>
      </li>
    </ul>
  </div>
  <div>
    <l-map style="min-height: 600px" :bounds="geosearchSelected" :zoom="zoom" :center="center">
      <div class="leaflet-bottom leaflet-left">
        <div id="legend" class="map-overlay">
          <div v-for="sign in signs" :key="sign.signId" v-if="sign.visible">
            <div v-for="signType in sign.data" :key="signType.id" class="mb-1">
              <button class="btn btn-sm btn-light">
                <img class="icon" :src="signType.icon">
              </button>
              {{signType.type}}
            </div>
          </div>
        </div>
      </div>
      <l-tile-layer :url="topoUrl" :options="mapOptions"></l-tile-layer>
      <!-- <l-geo-json :geojson="currentSignsD02.geojson"  :options="currentSignsD02.options"></l-geo-json>-->
      <!--<l-geo-json :geojson="detectedSignsD02.geojson"  :options="detectedSignsD02.options"></l-geo-json>-->
      <!--<v-geosearch :options="geosearchOptions" ></v-geosearch>-->
      <!-- <l-control-layers :position="layersPosition"/>-->
      <l-layer-group v-for="sign in signs" :key="sign.signId" :visible="sign.visible">
        <l-layer-group v-for="signType in sign.data" :key="signType.id">
          <l-marker v-for="item in signType.features"
            :key="item.id"
            :icon="iconSet(signType.icon, signType.iconSize)"
            :visible="sign.visible"
            :lat-lng="{
              lat:item.geometry.coordinates[1],
              lng:item.geometry.coordinates[0]}" @click="setLocationData(item.properties)">
          </l-marker>
        </l-layer-group>
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
import currentSignsD02Json from '../data/nearest_panos_d02_gele_koker_2018-05-28.json'
import detectedSignsD02Json from '../data/2018-05-28-detections-vluchtheuvel-bakens-amsterdam.json'
import firstrunD02Json from '../data/2018-05-11-detections-vluchtheuvel-bakens-panos.json'
// import { rd, rdToWgs84 } from '../services/geojson'
import {
  LMap,
  LTileLayer,
  LGeoJson,
  LLayerGroup,
  // LControlLayers,
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
    }),
    iconSet (iconUrl, iconSize) {
      return L.icon(
        { iconUrl: iconUrl,
          iconSize: iconSize,
          iconAnchor: [5, 5],
          popupAnchor: [0, -37]}
      )
    }
  },
  computed: {
    ...mapGetters([
      'locationData',
      'geosearchSelected',
      'iconUrl',
      'iconSize'
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
    // LControlLayers,
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
      signs: [{
        signId: 'D02 first run',
        signName: 'Vluchtheuvelbaken',
        signDescription: 'Gebod voor alle bestuurders het bord voorbij te gaan aan de zijde die de pijl aangeeft',
        signImage: 'http://wetten.overheid.nl/afbeelding?toestandid=BWBR0004825/2017-07-01_0&naam=27629.png',
        visible: false,
        data: [
          { type: 'uit administratie',
            id: 'currentD02',
            features: currentSignsD02Json.features,
            icon: 'static/images/d02.svg',
            iconSize: [10, 10]
          },
          { type: 'gedetecteerd',
            id: 'detectedD02',
            features: firstrunD02Json.features,
            icon: 'static/images/d02_ml.svg',
            iconSize: [7, 7]
          }]}, {
        signId: 'D02 second run',
        signName: 'Vluchtheuvelbaken',
        signDescription: 'Gebod voor alle bestuurders het bord voorbij te gaan aan de zijde die de pijl aangeeft',
        signImage: 'http://wetten.overheid.nl/afbeelding?toestandid=BWBR0004825/2017-07-01_0&naam=27629.png',
        visible: true,
        data: [
          { type: 'uit administratie',
            id: 'currentD02',
            features: currentSignsD02Json.features,
            icon: 'static/images/d02.svg',
            iconSize: [10, 10]
          },
          { type: 'gedetecteerd',
            id: 'detectedD02',
            features: detectedSignsD02Json.features,
            icon: 'static/images/d02_ml.svg',
            iconSize: [7, 7]
          }]
      }]
    }
  }
}
</script>
<style lang="scss" scoped>
  @import "~stijl/dist/scss/ams-colorpalette";
  .signSelector {
    font-weight: bold;
  }
  .sign {
    width: 30px;
    height: 30px;
  }
  .icon {
    width: 10px;
    height: 10px;
  }
  ul {
    margin-left: 0px;
    margin-bottom: 10px;
    padding: 0px;
  }
  li {
    margin: 0px 10px 10px 0px;
    font-family: 'Avenir Medium';
    list-style: none;
    float:left;
  }
  .map-overlay {
    background-color: #fff;
    box-shadow: 2px 2px #888888;
    padding: 10px 10px 5px 10px ;
    margin: 15px;
  }
</style>
