<template>
  <div id="app">
    <my-header></my-header>
    <div class="my-body">
      <router-view></router-view>
    </div>
    <my-footer></my-footer>

    <confirm-modal></confirm-modal>
  </div>
</template>

<script>
import MyHeader from './components/MyHeader'
import MyFooter from './components/MyFooter'
import ConfirmModal from './components/modals/ConfirmModal'

export default {
  name: 'App',
  components: {
    MyHeader,
    MyFooter,
    ConfirmModal,
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
$navbar-height: 84px;
@import "~bulma";
@import "~c3/c3";

.my-body {
  margin-top: 15px;
  min-height: 640px;
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
