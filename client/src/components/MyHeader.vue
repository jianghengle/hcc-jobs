<template>
  <div>
    <nav class="navbar has-shadow is-fixed-top">
      <div class="container">
        <div class="navbar-brand">
          <router-link class="navbar-item is-size-4 has-text-weight-bold has-text-black" :to="'/'">
            MY HCC
          </router-link>
          <div class="navbar-burger burger app-burger" :class="{'is-active': menuActive}"
            @click="menuActive = !menuActive">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <div class="navbar-menu" :class="{'is-active': menuActive}">
          <div class="navbar-start is-hidden-desktop">
            <div class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                Account
              </a>
              <div class="navbar-dropdown">
                <a class="navbar-item" @click="goToPath('/')">
                  {{username ? username : 'Login'}}
                </a>
                <a class="navbar-item" v-if="username" @click="logout">
                  Logout
                </a>
              </div>
            </div>
            <div class="navbar-item has-dropdown is-hoverable">
              <a @click="goToPath('/rhino')" class="navbar-link">
                Rhino
              </a>
              <div class="navbar-dropdown">
                <a @click="goToPath('/rhino/jobs')" class="navbar-item">
                  Jobs
                </a>
                <a @click="goToPath({fs: 'rhino'})" class="navbar-item">
                  File System
                </a>
                <a @click="goToPath('/rhino/jupyter')" class="navbar-item">
                  Jupyter Notebooks
                </a>
              </div>
            </div>
            <div class="navbar-item has-dropdown is-hoverable">
              <a @click="goToPath('/crane')" class="navbar-link">
                Crane
              </a>
              <div class="navbar-dropdown">
                <a @click="goToPath('/crane/jobs')" class="navbar-item">
                  Jobs
                </a>
                <a @click="goToPath('/crane/fs/%24HOME')" class="navbar-item">
                  File System
                </a>
              </div>
            </div>
            <a class="navbar-item">
              Anvil
            </a>
            <a class="navbar-item">
              Attic
            </a>
            <div class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                Other Links
              </a>
              <div class="navbar-dropdown">
                <a class="navbar-item">
                  HCC Docs
                </a>
                <a class="navbar-item">
                  Globus Transfer
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'my-header',
  data () {
    return {
      menuActive: false
    }
  },
  computed: {
    token () {
      return this.$store.state.user.token
    },
    username () {
      return this.$store.state.user.username
    },
  },
  methods: {
    logout () {
      var confirm = {
        title: 'Logout',
        message: 'Are you sure to logout?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.logoutConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    logoutConfirmed () {
      delete Vue.http.headers.common['Authorization']
      this.$store.commit('user/reset')
      this.$router.push('/')
      this.menuActive = false
    },
    goToPath(path){
      if(path.fs){
        this.openFileSystem(path.fs)
      }else{
        this.$router.push(path)
      }
      this.menuActive = false
    },
    openFileSystem (resource) {
      var lastFilePath = this.$store.state.info.lastFilePath[resource]
      if(lastFilePath){
        this.$router.push('/' + resource + '/fs/' + encodeURIComponent(lastFilePath))
      }else{
        this.$router.push('/' + resource + '/fs/' + encodeURIComponent('$HOME'))
      }
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
