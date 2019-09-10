<template>
  <div>
    <aside class="menu my-menu">
      <p class="menu-label">
        Account
      </p>
      <ul class="menu-list">
        <li><a>Login</a></li>
        <li><a>Logout</a></li>
      </ul>
      <p class="menu-label">
        Resources
      </p>
      <ul class="menu-list">
        <li>
          <a class="is-active">Rhino</a>
          <ul>
            <li><a>Jobs</a></li>
            <li><a>Home Directory</a></li>
            <li><a>Work Directory</a></li>
          </ul>
        </li>
        <li>
          <a>Crane</a>
          <ul>
            <li><a>Jobs</a></li>
            <li><a>Home Directory</a></li>
            <li><a>Work Directory</a></li>
          </ul>
        </li>
        <li>
          <a>Common Directory</a>
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
  }
}
</script>

<style lang="scss" scoped>

.my-menu {
  width: 200px;
  padding-top: 20px;
}

</style>
