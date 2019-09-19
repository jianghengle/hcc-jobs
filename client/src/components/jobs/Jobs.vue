<template>
  <div>
    <h1 class="title my-title">{{resourceName}}</h1>

    <div v-if="!token" class="notification is-danger">
      You need to login first to see your jobs!
    </div>

    <div v-if="queueResult">
      <div class="jobs-title">
        <span class="squeue-time">
          <a class="button" :class="{'is-loading': waiting}" @click="requestQueueJobs">
            <span class="icon">
              <v-icon name="sync"/>
            </span>
            <span>{{queueTimeLabel}}</span>
          </a>
        </span>
        <span><span class="is-size-5 has-text-weight-bold">{{queueJobs.length}}</span>&nbsp;&nbsp;jobs after</span>&nbsp;
        <datepicker
          wrapper-class="date-picker-wrapper"
          input-class="date-picker-input"
          format="yyyy-MM-dd"
          :value="date"
          v-on:selected="dateSelected">
        </datepicker>
      </div>

      <div v-if="queueError" class="notification is-danger">
        <button class="delete" @click="queueError=''"></button>
        {{queueError}}
      </div>

      <div v-if="waiting" class="has-text-centered">
        <v-icon class="icon is-medium fa-spin" name="spinner"></v-icon>
      </div>
      <div v-else>
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>#</th>
              <th v-for="h in queueHeader">{{h}}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(job, i) in queueJobs" class="clickable" @click="viewJob(job)">
              <th>{{i+1}}</th>
              <td v-for="(cell, j) in job" :class="{'node-list': j==job.length-1}">
                <span v-if="j==2">
                  <span v-if="jobStates[cell]"
                    :class="{'has-text-success': jobStates[cell][1]==0, 'has-text-warning': jobStates[cell][1]==1, 'has-text-danger': jobStates[cell][1]==2}">
                    {{cell}}
                  </span>
                  <span v-else class="has-text-danger">{{cell}}</span>
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
import Datepicker from 'vuejs-datepicker'

export default {
  name: 'jobs',
  components: {
    Datepicker
  },
  data () {
    return {
      queueError: '',
      queueTime: null,
      queueResult: null,
      waiting: false,
      date: new Date(),
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
      return this.$store.state.info.servers[this.resourceName]
    },
    jobStates () {
      return this.$store.state.info.jobStates
    },
    queueTimeLabel () {
      return DateFormat(this.queueTime, "h:MM:ss")
    },
    queueHeader () {
      if(this.queueResult){
        return this.queueResult.fields
      }
      return []
    },
    queueJobs () {
      if(this.queueResult && this.queueResult.values && this.queueResult.values.length && this.queueResult.values[0]){
        var jobs = this.queueResult.values.map(function(r){
          var job = r.trim().split('|')
          job.pop()
          job[3] = job[3].replace('T', ' ')
          return job
        })
        jobs.sort(function(a, b){
          return b[3].localeCompare(a[3])
        })
        return jobs
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
      var date = DateFormat(this.date, 'yyyy-mm-dd')
      this.$http.get(this.server + '/myapp/get_jobs/' + date).then(response => {
        if(response.body.timestamp){
          this.queueTime = new Date(response.body.timestamp * 1000)
          this.queueResult = response.body
          this.queueError = ''
        }else{
          this.queueError = 'Failed to get jobs!'
        }
        this.waiting = false
      }, response => {
        this.queueError = 'Failed to get jobs!'
        this.waiting = false
      })
    },
    viewJob (job) {
      this.$router.push('/' + this.resourceName + '/job/' + job[0])
    },
    dateSelected (newDate) {
      this.date = newDate
      this.requestQueueJobs()
      this.$store.commit('info/setStartDate', newDate)
    },
  },
  mounted () {
    if(this.$store.state.info.startDate){
      this.date = this.$store.state.info.startDate
    }
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

.jobs-title {
  margin-bottom: 10px;
}

.squeue-time {
  font-weight: normal;
  float: right;
}

.node-list {
  word-break: break-word;
}
</style>
