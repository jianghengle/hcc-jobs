// initial state
export const state = {
  windowWidth: 0,
}

// mutations
export const mutations = {

  setWindowWidth (state, windowWidth) {
    state.windowWidth = windowWidth
  },
}

export default {
  namespaced: true,
  state,
  mutations
}
