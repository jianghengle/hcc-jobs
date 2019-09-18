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

      <div v-if="nodeList">
        <table class="table is-fullwidth">
          <thead>
            <tr><th class="is-size-5">Monitor Nodes</th></tr>
          </thead>
          <tbody>
            <tr v-for="node in nodeList">
              <td>
                <div class="node-row">
                  <a class="button is-white is-small is-pulled-right" @click="node.open = !node.open">
                    <span class="icon is-small has-text-grey-light">
                      <v-icon v-if="node.open" name="chevron-up"/>
                      <v-icon v-if="!node.open" name="chevron-down"/>
                    </span>
                  </a>
                  <strong class="is-size-5">{{node.name}}</strong>&nbsp;&nbsp;|&nbsp;&nbsp;<em class="has-text-weight-bold">{{node.totalProc}}</em> processes &nbsp;&nbsp;|&nbsp;&nbsp; <em class="has-text-weight-bold">{{node.totalRes}} MB</em> memory
                </div>
                <div class="node-row" v-if="node.open"><pre>{{node.topResult}}</pre></div>
                <div class="columns">
                  <div class="column is-half">
                    <v-chart :options="node.cpuChart" autoresize />
                  </div>
                  <div class="column is-half">
                    <v-chart :options="node.resChart" autoresize />
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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
      jobInterval: null,
      nodes: null,
      nodeList: null
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
  methods: {
    requestJob () {
      this.$http.get(this.server + '/myapp/get_job_detail/' + this.jobId).then(response => {
        if(response.body.timestamp){
          this.jobDetail = response.body
          this.makeNodes()
        }else{
          this.queueError = 'Failed to get job detail!'
        }
        this.waiting = false
      }, response => {
        this.queueError = 'Failed to get job detail!'
      })
    },
    makeNodes () {
      if(!this.jobDetail.nodes){
        this.nodes = null
        this.nodeList = null
        return
      }

      var timestamp = this.jobDetail.timestamp
      var nodes = {}
      for(name in this.jobDetail.nodes){
        var topResult = this.jobDetail.nodes[name]
        var node = {name: name, topResult: topResult}
        var ps = this.getProcesses(name, topResult, timestamp)
        node.ps = ps
        this.makeCharts(node)
        node.totalProc = Object.keys(ps).length
        node.totalRes = Object.values(ps).reduce(function(total, p){
          return total + p.res
        }, 0)
        node.open = false
        if(this.nodes && this.nodes[name]){
          node.open = this.nodes[name].open
        }
        nodes[name] = node
      }
      this.nodes = nodes
      var nodeList = Object.values(nodes)
      nodeList.sort(function(a, b) {
        return a.name.localeCompare(b.name)
      })
      this.nodeList = nodeList
    },
    getProcesses (nodeName, topResult, timestamp) {
      var ps = {}
      var rows = topResult.split('\n').map(r => r.trim())
      var start = rows.indexOf('') + 2
      for(var i=start;i<rows.length;i++){
        var row = rows[i].split(/\ +/)
        var status = row[7]
        if(status != 'R')
          continue
        var pid = row[0]
        var res = parseInt(row[5])
        var unit = row[5][row[5].length-1].toLowerCase()
        if(unit == 'm'){
          res *= 1024
        }else if(unit == 'g'){
          res *= 1024*1024
        }else if(unit == 't'){
          res *= 1024*1024*1024
        }
        res = Math.round(res / 1024)
        var cpu = row[8]
        var mem = row[9]
        var date = new Date(timestamp*1000)
        var p = {pid: pid, res: res, cpu: cpu, mem: mem, cpus: [[date, cpu]], ress: [[date, res]]}
        if(this.nodes && this.nodes[nodeName] && this.nodes[nodeName].ps[pid]){
          var oldP = this.nodes[nodeName].ps[pid]
          p.cpus = oldP.cpus.concat(p.cpus)
          p.ress = oldP.ress.concat(p.ress)
        }
        ps[pid] = p
      }
      return ps
    },
    makeCharts (node) {
      var cpuSeries = []
      var resSeries = []
      Object.keys(node.ps).forEach(function(pid){
        var p = node.ps[pid]
        cpuSeries.push({name: pid, type: 'line', smooth: true, data: p.cpus, areaStyle: {opacity: 0.1}})
        resSeries.push({name: pid, type: 'line', smooth: true, data: p.ress, areaStyle: {opacity: 0.1}})
      })
      node.cpuChart = {
        title: { text: 'CPU %', top: 10 },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'time', splitLine: { show: false }, axisLabel: {show: false }},
        yAxis: { type: 'value', min: 0, max: 120 },
        series: cpuSeries
      }
      node.resChart = {
        title: { text: 'Memory (MB)', top: 10},
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'time', splitLine: { show: false }, axisLabel: {show: false }},
        yAxis: { type: 'value' },
        series: resSeries
      }
    }
  },
  mounted () {
    if(this.token){
      this.requestJob()
      this.jobInterval = setInterval(this.requestJob, 2000)
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

.node-row {
  margin-bottom: 5px;
}

.echarts {
  width: 100%;
}
</style>
