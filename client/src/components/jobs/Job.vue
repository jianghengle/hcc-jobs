<template>
  <div>
    <h1 class="title my-title">{{resourceName}}</h1>

    <div v-if="!token" class="notification is-danger">
      You need to login first to see the job detail!
    </div>

    <div class="title is-5">
      <span>Job: {{jobId}}</span>
    </div>

    <div v-if="jobError" class="notification is-danger">
      <button class="delete" @click="jobError=''"></button>
      {{jobError}}
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
      this.$http.get(this.server + '/myapp/get_squeue').then(response => {
        if(response.body.job){
          

          this.queueError = ''
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


</style>
