<template>
  <div>
    <v-select v-model="selected" label="searchText" :options="options" @search="onSearch" placeholder="Straat, Buurt, Stadsdeel...">
      <template slot="option" slot-scope="option">
        {{ option._display || '' }}
      </template>
    </v-select>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { geoSearch, getBounds } from '../services/api/geosearch'
import store from '../store'

let searchTimeout = null
export default {
  name: 'GeoSearch',
  data () {
    return {
      selected: null,
      options: []
    }
  },
  computed: {
    ...mapGetters([
      'geosearchSelected'
    ])
  },
  watch: {
    'selected' (newValue) {
      this.onSelect(newValue)
    },
    'geosearchSelected' (to, from) {
      // Example of a state change watch
      console.log('geosearchSelected has changed on geosearch', from, to)
    }
  },
  methods: {
    onSelect: async function (selected) {
      if (selected) {
        selected.searchText = selected._display
        const [p1, p2] = await getBounds(selected)
        // should be done with mapActions
        store.state.geosearchSelected = [p1, p2]
      } else {
        this.options = []
      }
    },
    onSearch: async function (searchText) {
      if (searchTimeout) {
        clearTimeout(searchTimeout)
      }
      searchTimeout = setTimeout(async () => {
        const results = await geoSearch(searchText)
        this.options = results
      }, 250)
    }
  }
}
</script>

<style scoped>
</style>
