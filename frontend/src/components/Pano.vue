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
    <img :src="locationData.url" width='100%'/>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'locationData'
    ])
  },
  watch: {
    'locationData' (to, from) {
      // Example of a state change watch
      console.log('text has changed', from, to)
    }
  }
}
</script>
