<template>
    <table>
      <tbody>
        <th colspan="2">
          <h3>Panoramabeeld</h3>
        </th>
        <tr v-for="(value, key) in locationData" :key="key">
          <th>{{key}}</th><td>{{value}}</td>
        </tr>
        <tr>
          <td colspan="2">
            <marzipano :pano_url="locationData.url"></marzipano>
          </td>
        </tr>
      </tbody>
    </table>
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
<style lang="scss" scoped>
h3
 {
    font-family: 'Avenir Medium';
    font-weight: bold;
 }
 th {
  font-family: 'Avenir Medium';
  padding-right: 20px;
  padding-bottom: 5px;
  vertical-align: top;
 }
 td {
   padding-bottom: 10px;
 }
</style>
