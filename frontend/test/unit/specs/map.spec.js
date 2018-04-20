import { amsMap } from '@/services/map'

describe('map', () => {
  it('should provide for a map of Amsterdam', () => {
    document.body.innerHTML =
      '<div id="map">' +
      '</div>'
    const el = document.getElementById('map')
    expect(amsMap(el)).toBeTruthy()
  })
})
