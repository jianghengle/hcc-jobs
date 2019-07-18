import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'
import ui from './modules/ui'
import modals from './modules/modals'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user: user,
    ui: ui,
    modals: modals
  }
})
