<template>
  <div class="card mt-2">
    <h3 class="card-header">
      {{title}}
    </h3>
    <div class="card-body">
      <slot></slot>
    </div>
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
