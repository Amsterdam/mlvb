<template>
  <div class="container mt-2">
    <header>
      <img class="logo" src="../../../static/logo-short.svg">
      <h2><b>{{title}}</b></h2>
    </header>
  </div>
</template>

<script>
export default {
  props: [
    'title'
  ]
}
</script>

<style lang="scss" scoped>
  .logo {
    height: 45px;
    margin-left: -18px;
    margin-right: 15px;
    float: left;
  }
</style>
