// initial state
export const state = {
  token: localStorage.getItem('token'),
  username: localStorage.getItem('username')
}

// mutations
export const mutations = {

  setToken (state, token) {
    state.token = token
  },

  setUsername (state, username) {
    state.username = username
  },

  reset (state) {
    state.token = null
    state.username = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }
}

export default {
  namespaced: true,
  state,
  mutations
}
