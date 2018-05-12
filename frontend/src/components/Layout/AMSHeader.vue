<template>
    <header>
      <div class="row  mt-3">
      <div class="col">
        <div class="row">
          <div class="col">
            <img class="logo" src="../../../static/logo-short.svg">
          </div>
          <div class="col">
            <div class="logo2">
              <img class="logo-ro" src="https://www.rijksoverheid.nl/binaries/content/gallery/rijksoverheid/channel-afbeeldingen/logos/logo-ro.svg">
              <p class="mirt">Ministerie van<br>Infrastructuur en Waterstaat</p>
            </div>
          </div>
        </div>
      </div>
      <div class="col mt-1">
        <h2 class="title"><b>{{title}}</b></h2>
      </div>
    </div>
    </header>
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
    height: 72px;
    margin-left: 0px;
    margin-top: 5px;
    margin-right: 20px;
    top: 0px;
    position: relative;
    float:left;
  }
  .logo-ro {
    height: 90px;
    margin-left: 0px;
    margin-right: 0px;
    margin-top: 10px;
    margin-bottom: -15px;
    top: -5px;
    position: relative;
    float:left;
  }
  .logo2 {
    float:left;
    position: relative;
    width: 160px;
  }
  .mirt {
    position: absolute;
    top: 55px;
    left: 45px;
    font-family: 'Times New Roman', Times, serif;
    font-size: 9px;
  }
  .title {
    font-family: 'Avenir Medium';
    font-weight: 'bold';
    text-align: right;
    margin-right: 10px;
  }
  .row {
    margin: 0px;
  }
</style>
