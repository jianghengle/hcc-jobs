<template>
  <div id="app">
    <my-header></my-header>
    <div class="my-body container">
      <div class="columns">
        <div class="column is-narrow is-paddingless is-hidden-touch">
          <div class="main-column">
            <my-menu></my-menu>
          </div>
        </div>
        <div class="column is-paddingless" style="display: grid">
          <div class="main-column">
            <div class="main-content">
              <router-view></router-view>
            </div>
          </div>
        </div>
      </div>
    </div>

    <new-file-modal></new-file-modal>
    <new-directory-modal></new-directory-modal>
    <edit-file-directory-modal></edit-file-directory-modal>
    <upload-modal></upload-modal>
    <delete-multiple-modal></delete-multiple-modal>
    <confirm-modal></confirm-modal>
  </div>
</template>

<script>
import Vue from 'vue'
import MyHeader from './components/MyHeader'
import MyMenu from './components/MyMenu'
import ConfirmModal from './components/modals/ConfirmModal'
import NewFileModal from './components/modals/NewFileModal'
import NewDirectoryModal from './components/modals/NewDirectoryModal'
import EditFileDirectoryModal from './components/modals/EditFileDirectoryModal'
import UploadModal from './components/modals/UploadModal'
import DeleteMultipleModal from './components/modals/DeleteMultipleModal'


export default {
  name: 'App',
  components: {
    MyHeader,
    MyMenu,
    ConfirmModal,
    NewFileModal,
    NewDirectoryModal,
    EditFileDirectoryModal,
    UploadModal,
    DeleteMultipleModal
  },
  computed: {
    token () {
      return this.$store.state.user.token
    }
  },
  methods: {
    handleResize () {
      this.$store.commit('ui/setWindowWidth', window.innerWidth)
    },
  },
  created () {
    if(this.token) {
      Vue.http.headers.common['Authorization'] = this.token
    }
  },
  mounted () {
    this.handleResize()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.handleResize)
  }
}
</script>

<style lang="scss">
@import "~bulma/sass/utilities/initial-variables";

@import "~bulma";
@import "~c3/c3";

.my-body {
  margin-top: 15px;
  height: calc(100vh - 52px);
}

.main-column {
  height: calc(100vh - 52px);
  overflow-y: auto;

  .main-content {
    padding: 20px;
  }
}

.clickable {
  cursor: pointer;
}

.date-picker-wrapper {
  display: inline-block;
}

.date-picker-input{
  cursor: pointer;
  height: 35px;
  width: 120px;
  text-align: center;
  font-size: 1rem;
}
</style>
