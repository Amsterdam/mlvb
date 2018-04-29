<template>
  <div class="col mt-1">
    <h3>Panoramabeeld</h3>
    <table>
      <tbody>
        <tr v-for="(value, key) in locationData" :key="key">
          <th>{{key}}</th><td>{{value}}</td>
        </tr>
      </tbody>
    </table>
    <marzipano :pano_url="locationData.url"></marzipano>
    <!-- <img :src="locationData.url" width='100%'/> -->
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import marziPano from './marziPano'

export default {
  computed: {
    ...mapGetters([
      'locationData'
    ])
  },
  components: {
    'marzipano': marziPano
  },
  watch: {
    'locationData' (to, from) {
      // Example of a state change watch
      // console.log('locationData has changed', from, to)
    }
  }
}
</script>
