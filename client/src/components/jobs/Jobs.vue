<template>
  <div>
    <h1 class="title my-title">{{resourceName}}</h1>
    <div>
      <div>Jobs in Queue: </div>
    </div>
  </div>
</template>

<script>


export default {
  name: 'jobs',
  data () {
    return {
      queueJobs: null,
    }
  },
  computed: {
    token () {
      return this.$store.state.user.token
    },
    resourceName () {
      return this.$route.params.resourceName
    },
  },
  methods: {
    requestQueueJobs () {
      
    }
  },
  mounted () {
    
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.my-title {
  text-transform: capitalize;
}

</style>
