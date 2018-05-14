<template>
  <footer class="container-fluid mt-4 pt-2 pb-1">
    <div class="row">
        <div class="col mt-2">
          <h4>Disclaimer</h4>
          <p>
            Deze website is gemaakt door de beide Datalabs van de Gemeente Amsterdam en het Ministerie van infrastructuur en waterstaat.<br>
            Voor meer informatie, kijk op <a href="https://www.github.com/amsterdam/mlvb">https://www.github.com/amsterdam/mlvb</a>
          </p>
        </div>
      <div class="col mt-1">
        <ul>
          <li><a href="https://www.amsterdam.nl/privacyverklaring/">Privacy en cookies</a></li>
          <li><a href="https://www.amsterdam.nl/overdezesite/">Over deze site</a></li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AMSFooter',
  props: [
    'title'
  ],
  data () {
    return {
      author: 'datapunt@amsterdam.nl'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
div {font-family: 'Avenir Medium'; }
.col {
  margin-left:30px;
}
.col.mt-1 {
  margin: 0px;
}
li {
  list-style:none;
  padding:5px;
  bottom: 10px;
  right: 0px;
  text-align: right;
}
ul {
  float: right;
}
.row {
  margin: 0px;
}
</style>
