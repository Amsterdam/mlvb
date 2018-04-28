<template>
  <div>
    <p>
      Coordinate: {{ coordinates }}
      Mslink: {{ mslink }}
      Bordcode: {{ bordnummer }}
      Pano_url: {{ pano_url }}
      <!--<img :src="pano_url" width='300px'>-->
    </p>
  </div>
</template>
<script>
export default {
  name: 'GeoJson2Popup',
  props: ['mslink', 'coordinates', 'bordnummer', 'pano_url']
}
</script>
