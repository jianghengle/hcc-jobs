<template>
  <div class="chart-container">
    <h5 class="title is-5 has-text-centered">CPU Hours by Resources</h5>
    <div id="barChart"></div>
  </div>
</template>

<script>
import c3 from 'c3'

export default {
  name: 'bar-chart',
  data () {
    return {
      data: null,
      chart: null
    }
  },
  methods: {
    requestData () {
      var url = 'http://129.93.241.22:8000/myapp/get_csv/data.csv'
      this.$http.get(url).then(response => {
        this.data = response.body.data
        this.drawChart()
      }, response => {
        console.log('Failed to get data!')
      })
    },
    drawChart () {
      var x = this.data[0][0]
      var columns = this.data.slice()
      this.chart = c3.generate({
        bindto: '#barChart',
        data: {
          x: x,
          columns: columns,
          type: 'bar',
        },
        axis: {
          x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d'
            }
          }
        }
      })
    }
  },
  mounted () {
    this.requestData()
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.chart-container {
  margin-top: 20px;
}

</style>
