<template>
  <div>
    <h1 class="title my-title">{{resourceName}}</h1>

    <div v-if="!token" class="notification is-danger">
      You need to login first to see your jobs!
    </div>

    <div v-if="queueResult">
      <div class="title is-5">
        <span class="squeue-time">
          @{{queueTimeLabel}}&nbsp;
          <div class="field squeue-rate">
            <div class="control has-icons-left">
              <div class="select">
                <select v-model="queueRate">
                  <option value="5000">5 sec</option>
                  <option value="60000">1 min</option>
                </select>
              </div>
              <div class="icon is-small is-left">
                <v-icon name="sync"/>
              </div>
            </div>
          </div>
        </span>
        <span>Jobs in Queue: {{queueJobs.length}}</span>&nbsp;
      </div>

      <div v-if="queueError" class="notification is-danger">
        <button class="delete" @click="queueError=''"></button>
        {{queueError}}
      </div>

      <div>
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>#</th>
              <th v-for="h in queueHeader">{{h}}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(job, i) in queueJobs" class="clickable">
              <th>{{i+1}}</th>
              <td v-for="(cell, j) in job" :class="{'node-list': j==job.length-1}">{{cell}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import DateFormat from 'dateformat'

export default {
  name: 'jobs',
  data () {
    return {
      queueError: '',
      queueTime: null,
      queueResult: null,
      queueRate: 60000,
      queueInterval: null
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
    queueTimeLabel () {
      return DateFormat(this.queueTime, "h:MM:ss")
    },
    queueHeader () {
      if(this.queueResult){
        return this.queueResult.split('\n')[0].split(/\ +/)
      }
      return []
    },
    queueJobs () {
      if(this.queueResult){
        return this.queueResult.split('\n').slice(1).map(function(r){
          return r.trim().split(/\ +/).map(item => item.trim())
        })
      }
      return []
    },
  },
  watch: {
    resourceName: function (val) {
      this.queueResult = null
    },
    queueRate: function (val) {
      if(this.queueInterval){
        clearInterval(this.queueInterval)
        this.queueInterval = null
      }
      this.queueInterval = setInterval(this.requestQueueJobs, this.queueRate)
    }
  },
  methods: {
    requestQueueJobs () {
      this.$http.get(this.server + '/myapp/get_squeue').then(response => {
        if(response.body.result){
          this.queueTime = new Date(response.body.timestamp * 1000)
          this.queueResult = response.body.result

          this.queueError = ''
        }else{
          this.queueError = 'Failed to get squeue!'
        }
        this.waiting = false
      }, response => {
        this.queueError = 'Failed to get squeue!'
      })
    },
  },
  mounted () {
    if(this.token){
      this.requestQueueJobs()
      if(!this.queueInterval){
        this.queueInterval = setInterval(this.requestQueueJobs, this.queueRate)
      }
    }
  },
  beforeDestroy () {
    if(this.queueInterval){
      clearInterval(this.queueInterval)
      this.queueInterval = null
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.my-title {
  text-transform: capitalize;
}

.squeue-time {
  font-size: 1rem;
  font-weight: normal;
  color: hsl(0, 0%, 48%);
  float: right;
}

.squeue-rate {
  display: inline-block;
  position: relative;
  top: -9px;
}

.node-list {
  word-break: break-word;
}
</style>
