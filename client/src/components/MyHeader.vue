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
          <!--<div class="navbar-start">
            <router-link class="navbar-item" :to="'/about'">
              About
            </router-link>
          </div>
          <div class="navbar-end">
            <a class="navbar-item" v-if="!token" @click="login">
              <v-icon name="sign-in-alt"/>&nbsp;Login
            </a>
            <a class="navbar-item" v-if="token">
              <v-icon name="sign-out-alt"/>&nbsp;Logout
            </a>
          </div>-->
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
    }
  },
  methods: {
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
