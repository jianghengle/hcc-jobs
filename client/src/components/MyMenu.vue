<template>
  <div class="menu-container">
    <aside class="menu my-menu">
      <p class="menu-label">
        Account
      </p>
      <ul class="menu-list">
        <li><router-link :to="'/'" :class="{'is-active': routeName=='Account'}">{{username ? username : 'Login'}}</router-link></li>
        <li v-if="username"><a @click="logout">Logout</a></li>
      </ul>
      <p class="menu-label">
        Resources
      </p>
      <ul class="menu-list">
        <li>
          <router-link :to="'/rhino'" :class="{'is-active': routePath=='/rhino'}">Rhino</router-link>
          <ul>
            <li><router-link :to="'/rhino/jobs'" :class="{'is-active': routePath.startsWith('/rhino/job')}">Jobs</router-link ></li>
            <li><a>File System</a></li>
          </ul>
        </li>
        <li>
          <a>Crane</a>
          <ul>
            <li><a>Jobs</a></li>
            <li><a>File System</a></li>
          </ul>
        </li>
        <li>
          <a>Anvil</a>
        </li>
        <li>
          <a>Attic</a>
        </li>
      </ul>
      <p class="menu-label">
        Others Links
      </p>
      <ul class="menu-list">
        <li><a>HCC Docs</a></li>
        <li><a>Globus Transfers</a></li>
      </ul>
    </aside>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'my-menu',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  computed: {
    username () {
      return this.$store.state.user.username
    },
    routeName () {
      return this.$route.name
    },
    routePath () {
      return this.$route.path
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
    },
  }
}
</script>

<style lang="scss" scoped>

.menu-container {
  padding: 20px;

  .my-menu {
    width: 200px;
  }
}


</style>
