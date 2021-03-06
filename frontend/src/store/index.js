import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // Register all state data in the state object
    text: 'NoText',
    locationData: {
      url: 'https://data.amsterdam.nl/panorama/2017/04/11/TMX7316010203-000255/pano_0000_001822/equirectangular/panorama_2000.jpg',
      mdlnr: 'D02ro_BB22',
      mslink: 48036,
      pano_id: 719891,
      stadsdeel: 'Zuid'
    },
    geosearchSelected: [[ 52.36152, 4.901259 ], [ 52.37182, 4.92294788 ]]
  },
  actions: {
    // Actions are available to manipulate the state
    // A component has access to these actions data by using mapActions, e.g.:
    //   methods: {
    //     ...mapActions({
    //       setText: 'setText'
    //     })
    //  }
    // See also main.js
    setText (store, text) {
      store.commit('text', text)
    },
    setLocationData (store, object) {
      store.commit('locationData', object)
    },
    setGeosearchSelected (store, object) {
      store.commit('geosearchSelected', object)
    }
  },
  mutations: {
    // The real manipulation of the state is by means of a mutation
    // Mutations are triggered by commits, this is normally done in an action
    text (state, text) {
      state.text = text
    },
    locationData (state, object) {
      state.locationData = object
    },
    geosearchSelected (state, object) {
      state.markerSelected = object
    }
  },
  getters: {
    text: state => {
      // Provide access to state data, or part of the state data
      // A component has access to the state data by using mapGetters, e.g.:
      //   computed: {
      //     ...mapGetters([
      //       'text'
      //     ])
      //   }
      // See also HelloWorld.vue
      return state.text
    },
    locationData: state => {
      return state.locationData
    },
    geosearchSelected: state => {
      return state.geosearchSelected
    }
  }
})
