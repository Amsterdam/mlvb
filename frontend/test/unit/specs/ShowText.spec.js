import Vue from 'vue'
import ShowText from '@/components/ShowText'

describe('ShowText.vue', () => {
  it('should render correct contents', () => {
    const Constructor = Vue.extend(ShowText)
    const vm = new Constructor().$mount()
    expect(vm.$el.textContent)
      .toEqual('')
  })
})
