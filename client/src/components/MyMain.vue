<template>
  <div>
    <div v-if="!token">
      <center class="title is-4">Welcome to Holand Computing Center!</center>

      <div class="login-form">
        <div v-if="error" class="notification is-danger">
          <button class="delete" @click="error=''"></button>
          {{error}}
        </div>

        <div class="field">
          <label class="label">Username</label>
          <div class="control has-icons-left">
            <input class="input" type="text" placeholder="HCC username" v-model="username">
            <span class="icon is-small is-left">
              <v-icon name="user"/>
            </span>
          </div>
        </div>

        <div class="field">
          <label class="label">Password</label>
          <div class="control has-icons-left">
            <input class="input" type="password" placeholder="password" v-model="password">
            <span class="icon is-small is-left">
              <v-icon name="lock"/>
            </span>
          </div>
        </div>

        <div class="field">
          <div class="control">
            <label class="checkbox">
              <input type="checkbox">
              Remember me
            </label>
          </div>
        </div>

        <div class="field is-grouped">
          <div class="control">
            <button class="button is-link" :class="{'is-loading': waiting}" @click="login">Submit</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <center class="title is-4">Hi {{user.username}}! Please click the menu to access the resources.</center>
      {{user}}

    </div>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'my-main',
  data () {
    return {
      username: '',
      password: '',
      rememberMe: false,
      error: '',
      waiting: false,
      user: null
    }
  },
  computed: {
    server () {
      return this.$store.state.servers.account
    },
    token () {
      return this.$store.state.user.token
    }
  },
  methods: {
    login () {
      this.username = this.username.trim()
      this.waiting = true
      var message = {username: this.username, password: this.password}
      this.$http.post(this.server + '/myapp/login_user', message).then(response => {
        if(response.body.user){
          this.user = response.body.user
          var session = response.body.session
          Vue.http.headers.common['Authorization'] = session.token
          this.$store.commit('user/setToken', session.token)
          this.$store.commit('user/setUsername', session.uid)
          if (this.rememberMe) {
            localStorage.setItem('token', session.token)
            localStorage.setItem('username', session.uid)
          }
          this.error = ''
        }else{
          this.error = 'Failed to authorize user!'
          this.$store.commit('user/reset')
        }
        this.waiting = false
      }, response => {
        this.error = 'Failed to authorize user!'
        this.$store.commit('user/reset')
        this.waiting = false
      })
    },
    mounted () {
      if(this.token){
        this.$http.get(this.server + '/myapp/get_user').then(response => {
          if(response.body.user){
            this.user = response.body.user
            this.error = ''
          }else{
            this.error = 'Failed to get user!'
            this.$store.commit('user/reset')
          }
          this.waiting = false
        }, response => {
          this.error = 'Failed to get user!'
          this.$store.commit('user/reset')
          this.waiting = false
        })
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.login-form {
  max-width: 600px;
  margin: auto;
}

</style>
