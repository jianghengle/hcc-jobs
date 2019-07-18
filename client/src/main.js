// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import VueResource from 'vue-resource'
Vue.use(VueResource)

import 'vue-awesome/icons/sign-in-alt'
import 'vue-awesome/icons/sign-out-alt'
import 'vue-awesome/icons/angle-left'
import 'vue-awesome/icons/angle-right'
import 'vue-awesome/icons/angle-down'
import 'vue-awesome/icons/chevron-up'
import 'vue-awesome/icons/chevron-down'
import 'vue-awesome/icons/chevron-left'
import 'vue-awesome/icons/spinner'
import 'vue-awesome/icons/edit'
import 'vue-awesome/icons/trash'
import 'vue-awesome/icons/upload'
import 'vue-awesome/icons/plus'
import 'vue-awesome/icons/folder'
import 'vue-awesome/icons/file-alt'
import 'vue-awesome/icons/file-image'
import 'vue-awesome/icons/file-audio'
import 'vue-awesome/icons/file-video'
import 'vue-awesome/icons/brands/youtube'
import 'vue-awesome/icons/brands/markdown'
import Icon from 'vue-awesome/components/Icon'
Vue.component('v-icon', Icon)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
