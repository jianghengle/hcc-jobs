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
            <input class="input" type="password" placeholder="password" v-model="password" @keyup.enter="login">
            <span class="icon is-small is-left">
              <v-icon name="lock"/>
            </span>
          </div>
        </div>

        <div class="field">
          <div class="control">
            <label class="checkbox">
              <input type="checkbox" v-model="rememberMe">
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

    <div v-if="token && user" class="user-info-container">
      <p class="title is-5 has-text-weight-bold">Welcome {{user.username}} </p>
      <strong>Please click the menu items to access the resources.</strong>
      <div class="user-info">
        <table class="table is-fullwidth">
          <tbody>
            <tr>
              <th>Username</th>
              <td>{{user.username}}</td>
            </tr>
            <tr>
              <th>Full Name</th>
              <td>{{user.fullname}}</td>
            </tr>
            <tr>
              <th>Email</th>
              <td>{{user.email}}</td>
            </tr>
            <tr>
              <th>Description</th>
              <td>{{user.description}}</td>
            </tr>
            <tr>
              <th>Groups</th>
              <td>
                <div v-for="g in user.groups">{{g}}</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="box change-password-box">
        <article class="media">
          <div class="media-content">
            <p class="title is-5">Change Password</p>
            <div class="field">
              <label class="label">New Password</label>
              <div class="control">
                <input class="input" type="password" placeholder="New password" v-model="newPassword">
              </div>
            </div>
            <div class="field">
              <label class="label">Retype New Password</label>
              <div class="control">
                <input class="input" type="password" placeholder="Retype new password" v-model="newPasswordAgain">
              </div>
            </div>
            <div v-if="changePasswordError" class="notification is-danger">
              <button class="delete" @click="changePasswordError=''"></button>
              {{changePasswordError}}
            </div>
            <div class="field is-grouped">
              <div class="control">
                <button class="button is-link" :disabled="!canChangePassword" :class="{'is-loading': changePasswordWaiting}" @click="changePassword">Change Password</button>
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'account',
  data () {
    return {
      username: '',
      password: '',
      rememberMe: false,
      error: '',
      waiting: false,
      user: null,
      newPassword: '',
      newPasswordAgain: '',
      changePasswordError: '',
      changePasswordWaiting: false
    }
  },
  computed: {
    server () {
      return this.$store.state.info.servers.account
    },
    token () {
      return this.$store.state.user.token
    },
    canChangePassword () {
      return this.newPassword && this.newPassword.length >= 8 && this.newPassword == this.newPasswordAgain
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
          var token = session.token + '$' + btoa(this.password)
          Vue.http.headers.common['Authorization'] = token
          this.$store.commit('user/setToken', token)
          this.$store.commit('user/setUsername', session.uid)
          if (this.rememberMe) {
            localStorage.setItem('token', token)
            localStorage.setItem('username', session.uid)
          }
          this.error = ''
          this.username = ''
          this.password = ''
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
    changePassword () {
      var confirm = {
        title: 'Change Password',
        message: 'Are you sure to change your password? After password changed successfully, you would be logged out and you need to re-login using your new password',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.changePasswordConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    changePasswordConfirmed () {
      if(!this.canChangePassword || this.changePasswordWaiting)
        return
      this.changePasswordWaiting = true
      var message = {newPassword: this.newPassword.trim()}
      this.$http.post(this.server + '/myapp/change_password', message).then(response => {
        if(response.body.ok){
          delete Vue.http.headers.common['Authorization']
          this.$store.commit('user/reset')
          this.newPassword = ''
          this.newPasswordAgain = ''
        }else{
          this.changePasswordError = 'Failed to change password: ' + response.body.err
        }
        this.changePasswordWaiting = false
      }, response => {
        this.error = 'Failed to change password!'
        this.changePasswordWaiting = false
      })
    }
  },
  mounted () {
    if(this.token){
      this.$http.get(this.server + '/myapp/get_user').then(response => {
        if(response.body){
          this.user = response.body
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
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.login-form {
  max-width: 600px;
  margin: auto;
}

.user-info-container {
  max-width: 600px;
  margin: auto;

  .user-info {
    margin-top: 20px;
  }

  .change-password-box {
    margin-top: 50px;
    box-shadow: none;
    padding: 0px;
  }
}

</style>
