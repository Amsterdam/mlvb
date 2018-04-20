<!--Example of a component that uses D3-->
<template>
  <div></div>
</template>

<script>
import * as d3 from 'd3'

export default {
  mounted () {
    const svg = d3.select(this.$el)
      .append('svg')

    svg.append('circle')
      .style('stroke', 'gray')
      .style('fill', 'white')
      .attr('r', 40)
      .attr('cx', 50)
      .attr('cy', 50)
      .on('mouseover', function () { d3.select(this).style('fill', 'aliceblue') })
      .on('mouseout', function () { d3.select(this).style('fill', 'white') })
  }
}
</script>
