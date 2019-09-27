<template>
  <div>
    <h1 class="title my-title">{{resourceName}}</h1>

    <div v-if="!token" class="notification is-danger">
      You need to login first to see your jupyter notebooks!
    </div>

    <div v-if="!jupyters == null" class="has-text-centered">
      <v-icon class="icon is-medium fa-spin" name="spinner"></v-icon>
    </div>
    <div v-else>
      <div class="jupyter-title">
        <span class="is-pulled-right">
          <a class="button is-link" :class="{'is-loading': waiting}" @click="launchNew">
            Launch New
          </a>
        </span>
        <span class="is-size-5 has-text-weight-bold">Jupiter Notebooks</span>
      </div>

      <div>
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>#</th>
              <th>Jupyter Notebook</th>
              <th>Started At</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(jupyter, i) in jupyters">
              <th>{{i+1}}</th>
              <td><a :href="jupyter.link" target="_blank">Notebook Link</a></td>
              <td :class="{'has-text-danger': jupyter.expired}">{{jupyter.startTimeLabel}}<span v-if="jupyter.expired">&nbsp;(Expired)</span></td>
              <td>
                <a class="icon has-text-danger" @click="stopJupyter(i)">
                  <v-icon name="trash"/>
                </a>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="waiting">
          <v-icon class="icon is-medium fa-spin" name="spinner"></v-icon>
        </div>

        <div v-if="error" class="notification is-danger">
          <button class="delete" @click="error=''"></button>
          {{error}}
        </div>

        <div class="has-text-centered" v-if="jupyters && !jupyters.length">
          (Empty)
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DateFormat from 'dateformat'

export default {
  name: 'jupyter',
  data () {
    return {
      jupyters: null,
      error: '',
      waiting: false
    }
  },
  computed: {
    token () {
      return this.$store.state.user.token
    },
    resourceName () {
      return this.$route.params.resourceName
    },
    server () {
      return this.$store.state.info.servers[this.resourceName]
    },
    serverWithoutPort () {
      var parts = this.server.split(':')
      if(parts.length == 3){
        return parts[0] + ':' + parts[1]
      }
      if(parts.length == 2){
        return this.server
      }
    }
  },
  watch: {
    resourceName: function (val) {
      this.jupyters = null
      this.requestJupyters()
    },
  },
  methods: {
    requestJupyters () {
      this.$http.get(this.server + '/myapp/get_jupyters/' + this.resourceName).then(response => {
        if(response.body.jupyters){
          var jupyters = response.body.jupyters.map(this.makeJupyter)
          jupyters.sort((a, b) => a.startedAt - b.startedAt)
          this.jupyters = jupyters
        }else{
          this.error = 'Failed to get jupyters!'
        }
      }, response => {
        this.error = 'Failed to get jupyters!'
      })
    },
    launchNew () {
      this.waiting = true
      var message = {cluster: this.resourceName}
      this.$http.post(this.server + '/myapp/start_jupyter', message).then(response => {
        if(response.body.id){
          this.jupyters.push(this.makeJupyter(response.body))
        }else{
          this.error = 'Failed to launch new!'
        }
        this.waiting = false
      }, response => {
        this.error = 'Failed to launch new!'
        this.waiting = false
      })
    },
    makeJupyter (jupyter) {
      jupyter.link = this.serverWithoutPort + ':' + jupyter.port + '/?token=' + jupyter.token
      jupyter.startTime = new Date(jupyter.startedAt * 1000)
      jupyter.startTimeLabel = DateFormat(jupyter.startTime, 'ddd mmm dd HH:MM')
      jupyter.expired = Date.now() -jupyter.startTime > 86400000
      return jupyter
    },
    stopJupyter (idx) {
      var jupyter = this.jupyters[idx]
      var confirm = {
        title: 'Stop Notebook',
        message: 'Are you sure to stop the notebook started at ' + jupyter.startTimeLabel + '?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.stopJupyterConfirmed,
          args: [idx]
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    stopJupyterConfirmed (idx) {
      var jupyter = this.jupyters[idx]
      this.waiting = true
      var message = {jupyterId: jupyter.id}
      this.$http.post(this.server + '/myapp/stop_jupyter', message).then(response => {
        if(response.body.ok){
          this.jupyters.splice(idx, 1)
        }else{
          this.error = 'Failed to stop notebook'
        }
        this.waiting = false
      }, response => {
        this.error = 'Failed to stop notebook!'
        this.waiting = false
      })
    }
  },
  mounted () {
    if(this.token){
      this.requestJupyters()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.my-title {
  text-transform: capitalize;
}

.jupyter-title {
  margin-bottom: 10px;
}
</style>
