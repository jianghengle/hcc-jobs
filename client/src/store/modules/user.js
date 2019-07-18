// initial state
export const state = {
  token: localStorage.getItem('token')
}

// mutations
export const mutations = {

  setToken (state, token) {
    state.token = token
  },

  reset (state) {
    state.token = null
    localStorage.removeItem('token')
  }
}

export default {
  namespaced: true,
  state,
  mutations
}
