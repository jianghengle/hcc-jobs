// initial state
export const state = {
  confirmModal: {
    opened: false,
    title: '',
    message: '',
    button: '',
    callback: null
  },
  newFileModal: {
    opened: false
  },
  newDirectoryModal: {
    opened: false
  },
  editFileDirectoryModal: {
    opened: false,
    path: null,
    name: null,
    current: false
  },
  uploadModal: {
    opened: false
  },
  deleteMultipleModal: {
    opened: false,
    files: null
  },
  pasteModal: {
    opened: false
  },
}

// mutations
export const mutations = {

  openConfirmModal (state, confirm) {
    state.confirmModal.opened = true
    state.confirmModal.title = confirm.title
    state.confirmModal.message = confirm.message
    state.confirmModal.button = confirm.button
    state.confirmModal.callback = confirm.callback
  },

  closeConfirmModal (state) {
    state.confirmModal.opened = false
    state.confirmModal.title = ''
    state.confirmModal.message = ''
    state.confirmModal.button = ''
    state.confirmModal.callback = null
  },

  openNewFileModal (state) {
    state.newFileModal.opened = true
  },

  closeNewFileModal (state) {
    state.newFileModal.opened = false
  },

  openNewDirectoryModal (state) {
    state.newDirectoryModal.opened = true
  },

  closeNewDirectoryModal (state) {
    state.newDirectoryModal.opened = false
  },

  openEditFileDirectoryModal (state, obj) {
    state.editFileDirectoryModal.path = obj.path
    state.editFileDirectoryModal.name = obj.name
    state.editFileDirectoryModal.current = obj.current
    state.editFileDirectoryModal.opened = true
  },

  closeEditFileDirectoryModal (state) {
    state.editFileDirectoryModal.opened = false
    state.editFileDirectoryModal.path = null
    state.editFileDirectoryModal.name = null
    state.editFileDirectoryModal.current = null
  },

  openUploadModal (state) {
    state.uploadModal.opened = true
  },

  closeUploadModal (state) {
    state.uploadModal.opened = false
  },

  openDeleteMultipleModal (state, files) {
    state.deleteMultipleModal.files = files
    state.deleteMultipleModal.opened = true
  },

  closeDeleteMultipleModal (state) {
    state.deleteMultipleModal.opened = false
    state.deleteMultipleModal.files = null
  },

  openPasteModal (state) {
    state.pasteModal.opened = true
  },

  closePasteModal (state) {
    state.pasteModal.opened = false
  },
}

export default {
  namespaced: true,
  state,
  mutations
}
