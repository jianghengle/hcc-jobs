import Vue from 'vue'

// initial state
export const state = {
  servers: {
    account: 'https://ood-rhino.unl.edu:8000',
    rhino: 'https://ood-rhino.unl.edu:8000',
  },
  jobStates: {
    'BOOT_FAIL': ['BF', 2, false],
    'CANCELLED': ['CA', 2, false],
    'COMPLETED': ['CD', 0, false],
    'DEADLINE': ['DL', 2, false],
    'FAILED': ['F', 2, false],
    'NODE_FAIL': ['NF', 2, false],
    'OUT_OF_MEMORY': ['OOM', 2, false],
    'PENDING': ['PD', 1, true],
    'PREEMPTED': ['PR', 2, false],
    'RUNNING': ['R', 0, true],
    'REQUEUED': ['RQ', 1, true],
    'RESIZING': ['RS', 1, true],
    'REVOKED': ['RV', 2, false],
    'SUSPENDED': ['S', 1, true],
    'TIMEOUT': ['TO', 2, false]
  },
  startDate: null,
  fileSystems: {
    rhino: ['$HOME', '$WORK', '$COMMON']
  },
  fileCache: {
    rhino: {}
  },
  linkCache: {
    rhino: {}
  },
  lastFilePath: {
    rhino: null
  },
  clipboard: {}
}

// mutations
export const mutations = {
  setStartDate (state, startDate) {
    state.startDate = startDate
  },
  cacheFile (state, obj) {
    var file = obj.file
    Vue.set(state.fileCache[obj.resourceName], file.path, file)
  },
  cacheLink (state, obj) {
    var link = {link: obj.link, linkTime: Date.now()}
    Vue.set(state.linkCache[obj.resourceName], obj.path, link)
  },
  setLastFilePath (state, obj) {
    state.lastFilePath[obj.resourceName] = {fileType: obj.fileType, filePath: obj.filePath}
  },
  setClipboard (state, obj) {
    state.clipboard = obj
  }
}

export default {
  namespaced: true,
  state,
  mutations
}
