<template>
  <div class="col-xs-6">
    <h3 class="header">
      {{title}}
    </h3>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'card',
  props: [
    'title'
  ]
}
</script>

<style scoped>
@media print {
  .card {
    page-break-after: always;
  }
}
</style>
