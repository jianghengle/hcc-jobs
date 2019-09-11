<template>
  <div>
    <h1 class="title my-title">{{resourceName}}</h1>
    <div>

      <div>Jobs in Queue: </div>
      <div v-if="queueError" class="notification is-danger">
        <button class="delete" @click="queueError=''"></button>
        {{queueError}}
      </div>

      <div v-if="queueResult">
        {{queueResult}}
      </div>
    </div>
  </div>
</template>

<script>


export default {
  name: 'jobs',
  data () {
    return {
      queueError: '',
      queueResult: null
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
    server () {
      return this.$store.state.servers[this.resourceName]
    },
    queueHeader () {

    },
  },
  methods: {
    requestQueueJobs () {
      this.$http.get(this.server + '/myapp/get_squeue').then(response => {
        if(response.body.result){
          this.queueResult = response.body.result
          this.queueError = ''
        }else{
          this.queueError = 'Failed to get squeue!'
        }
        this.waiting = false
      }, response => {
        this.queueError = 'Failed to get squeue!'
      })
    }
  },
  mounted () {
    this.requestQueueJobs()
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.my-title {
  text-transform: capitalize;
}

</style>
