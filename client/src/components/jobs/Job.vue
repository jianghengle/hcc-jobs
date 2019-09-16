<template>
  <div>
    <div class="buttons">
      <router-link class="button" :to="'/'+resourceName+'/jobs'">
        <span class="icon">
          <v-icon name="chevron-left"/>
        </span>
        <span class="my-title">All {{resourceName}} Jobs</span>
      </router-link>
    </div>

    <div v-if="!token" class="notification is-danger">
      You need to login first to see the job detail!
    </div>

    <div v-if="jobError" class="notification is-danger">
      <button class="delete" @click="jobError=''"></button>
      {{jobError}}
    </div>

    <div v-if="jobDetail">
      <div class="columns is-multiline">
        <div class="column is-one-quarter" v-for="(f, i) in jobDetail.fields">
          <span class="has-text-weight-bold">{{f}}</span>:
          <span class="my-value">{{jobDetail.values[i]}}</span>
        </div>
      </div>

      <div>
        <div v-for="(v, k) in jobDetail.nodes">
          <div>{{k}}</div>
          <div><pre>{{v}}</pre></div>
        </div>
      </div>
    </div>
    <div v-else class="has-text-centered">
      <v-icon class="icon is-medium fa-spin" name="spinner"></v-icon>
    </div>
  </div>
</template>

<script>
import DateFormat from 'dateformat'

export default {
  name: 'job',
  data () {
    return {
      jobError: '',
      jobDetail: null,
      jobInterval: null
    }
  },
  computed: {
    token () {
      return this.$store.state.user.token
    },
    username () {
      return this.$store.state.user.username
    },
    resourceName () {
      return this.$route.params.resourceName
    },
    jobId () {
      return this.$route.params.jobId
    },
    server () {
      return this.$store.state.servers[this.resourceName]
    },
    
  },
  watch: {
    resourceName: function (val) {
      this.jobResult = null
    },
  },
  methods: {
    requestJob () {
      this.$http.get(this.server + '/myapp/get_job_detail/' + this.jobId).then(response => {
        console.log(response.body)
        if(response.body.timestamp){
          this.jobDetail = response.body
        }else{
          this.queueError = 'Failed to get job detail!'
        }
        this.waiting = false
      }, response => {
        this.queueError = 'Failed to get job detail!'
      })
    },
  },
  mounted () {
    if(this.token){
      this.requestJob()
    }
  },
  beforeDestroy () {
    if(this.jobInterval){
      clearInterval(this.jobInterval)
      this.jobInterval = null
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.my-title {
  text-transform: capitalize;
}

.my-value {
  word-break: break-word;
}
</style>
