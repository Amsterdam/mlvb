<template>
  <div class="menu mt-3">
    <div class="d-flex justify-content-center">
      <geo-search-bar class="geo-search"></geo-search-bar>
    </div>
  </div>
</template>

<script>
import GeoSearchBar from '../Geosearch'
export default {
  components: {GeoSearchBar}
}
</script>

<style lang="scss" scoped>
@import "~stijl/dist/scss/ams-colorpalette";
.nav {
  background-color: #f5f3f3;
}
.menu {
  background-color: #f5f3f3;
  height: 45px;
}
.geo-search {
  background-color: white;
  width: 75%;
  height: 35px;
  margin: 5px;
  margin-left: 60px;
}
</style>
