<template>
  <div>
    <h1 class="title my-title">{{resourceName}}</h1>

    <div v-if="!token" class="notification is-danger">
      You need to login first to see your jobs!
    </div>

    <div v-if="queueResult">
      <div class="title is-5">
        <span class="squeue-time">
          <a class="button" :class="{'is-loading': waiting}" @click="requestQueueJobs">
            <span class="icon">
              <v-icon name="sync"/>
            </span>
            <span>{{queueTimeLabel}}</span>
          </a>
        </span>
        <span>Jobs in Queue: {{queueJobs.length}}</span>
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
              <th v-for="h in queueHeader">{{h == 'ST' ? 'STATE' : h}}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(job, i) in queueJobs" class="clickable" @click="viewJob(job)">
              <th>{{i+1}}</th>
              <td v-for="(cell, j) in job" :class="{'node-list': j==job.length-1}">
                <span v-if="j==4"
                  :class="{'has-text-success': jobStates[cell][1]==0, 'has-text-warning': jobStates[cell][1]==1, 'has-text-danger': jobStates[cell][1]==2}">
                  {{jobStates[cell][0]}}
                </span>
                <span v-else>{{cell}}</span>
              </td>
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
      waiting: false,
      jobStates: {
        BF: ['BOOT_FAIL', 2],
        CA: ['CANCELLED', 2],
        CD: ['COMPLETED', 0],
        CF: ['CONFIGURING', 1],
        CG: ['COMPLETING', 0],
        DL: ['DEADLINE', 2],
        F: ['FAILED', 2],
        NF: ['NODE_FAIL', 2],
        OOM: ['OUT_OF_MEMORY', 2],
        PD: ['PENDING', 1],
        PR: ['PREEMPTED', 2],
        R: ['RUNNING', 0],
        RD: ['RESV_DEL_HOLD', 1],
        RF: ['REQUEUE_FED', 1],
        RH: ['REQUEUE_HOLD', 1],
        RQ: ['REQUEUED', 1],
        RS: ['RESIZING', 1],
        RV: ['REVOKED', 2],
        SI: ['SIGNALING', 1],
        SE: ['SPECIAL_EXIT', 2],
        SO: ['STAGE_OUT', 1],
        ST: ['STOPPED', 2],
        S: ['SUSPENDED', 1],
        TO: ['TIMEOUT', 2]
      }
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
        return this.queueResult.split('\n')[0].split(/\ +/).map(item => item.trim())
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
      this.requestQueueJobs()
    },
  },
  methods: {
    requestQueueJobs () {
      this.waiting = true
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
        this.waiting = false
      })
    },
    viewJob (job) {
      this.$router.push('/' + this.resourceName + '/job/' + job[0])
    }
  },
  mounted () {
    if(this.token){
      this.requestQueueJobs()
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
  font-weight: normal;
  float: right;
}

.node-list {
  word-break: break-word;
}
</style>
