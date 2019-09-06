<template>
  <div>
    <div class="field is-grouped">
      <p class="control">
        <input class="input" type="text" placeholder="Username" v-model="username">
      </p>
      <p class="control">
        <a class="button is-info" @click="squeue">
          Squeue
        </a>
      </p>
    </div>
    <div v-if="result">
      <div><em>{{squeueInfo}}</em></div>
      <div>
        <table class="table is-fullwidth is-striped is-hoverable">
          <thead>
            <tr>
              <th>Total: {{jobs ? jobs.length : '0'}}</th>
              <th v-for="h in header">{{h}}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(job, i) in jobs">
              <th>{{i+1}}</th>
              <td v-for="j in job">{{j}}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="!jobs || !jobs.length" class="has-text-centered">
          (Empty)
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'squeue',
  data () {
    return {
      username: '',
      result: ''
    }
  },
  computed: {
    rows () {
      return this.result.split('\n')
    },
    squeueInfo () {
      return this.rows[0]
    },
    header () {
      if(this.rows[1]){
        return this.rows[1].trim().split(/\ +/).map(item => item.trim())
      }
    },
    jobs () {
      if(this.rows.length > 2){
        var jobs = []
        this.rows.slice(2).forEach(function(r){
          if(r.trim()){
            var job = r.trim().split(/\ +/).map(item => item.trim())
            jobs.push(job)
          }
        })
        return jobs
      }
    }
  },
  methods: {
    squeue () {
      var url = 'http://129.93.241.22:8000/myapp/request_squeue'
      var message = {username: this.username}
      this.$http.post(url, message).then(response => {
        this.result = response.body.result
      }, response => {
        console.log('Failed to get data!')
      })
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>



</style>
