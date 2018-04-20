<template>
  <div></div>
</template>

<script>
import vegaEmbed from 'vega-embed'

import vegaSpec from './vega-example-spec'

const vegaEmbedOptions = {
  'actions': {
    'export': false,
    'source': false,
    'editor': false},
  'renderer': 'svg'
}

export default {
  mounted () {
    vegaEmbed(this.$el, vegaSpec, vegaEmbedOptions)
  }
}
</script>
