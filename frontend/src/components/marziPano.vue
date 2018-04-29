<!--component that uses marziPano-->
<template>
  <div style="height: 500px"></div>
</template>

<script>
import {
  Viewer,
  ImageUrlSource,
  EquirectGeometry,
  RectilinearView
} from 'marziPano'

export default {
  props: ['pano_url'],
  data () {
    return {
      viewerOpts: {
        controls: {
          mouseViewMode: 'drag' // drag|qtvr
        }
      }
    }
  },
  mounted () {
    this.panoView(this.viewerOpts, this.pano_url)
  },
  methods: {
    panoView (viewerOpts, panoUrl) {
      this.viewer = new Viewer(this.$el, viewerOpts)
      let source = ImageUrlSource.fromString(panoUrl)
      let geometry = new EquirectGeometry([{ width: 2000 }])
      let limiter = RectilinearView.limit.traditional(1024, 100 * Math.PI / 180)
      let view = new RectilinearView({ yaw: Math.PI + 180 }, limiter)
      this.scene = this.viewer.createScene({
        source: source,
        geometry: geometry,
        view: view,
        pinFirstLevel: true
      })
      // Display scene.
      this.scene.switchTo()
    }
  },
  watch: {
    'pano_url' (to, from) {
      // console.log('pano has changed', from, to)
      this.panoView(this.viewerOpts, to)
    }
  }
}
</script>
