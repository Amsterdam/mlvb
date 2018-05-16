<!--component that uses marziPano-->
<template>
  <div style="height: 400px; margin:0px;"></div>
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
    panoView (viewerOpts, panoUrl, direction) {
      this.viewer = new Viewer(this.$el, viewerOpts)
      let source = ImageUrlSource.fromString(panoUrl.url)
      let geometry = new EquirectGeometry([{ width: 2000 }])
      let limiter = RectilinearView.limit.traditional(1024, 100 * Math.PI / 180)
      let yawSet = 1
      switch (panoUrl.direction) {
        case 1:
          yawSet = -90
          break
        case 2:
          yawSet = 1
          break
        case 3:
          yawSet = 90
          break
        case 4:
          yawSet = 180
          break
      }
      let view = new RectilinearView({ yaw: (yawSet - 30) * Math.PI / 180, pitch: 12 * Math.PI / 180 }, limiter)
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
    },
    'direction' (to, from) {
      console.log('direction has changed', from, to)
    }
  }
}
</script>
