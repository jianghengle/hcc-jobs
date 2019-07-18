<template>
  <div class="chart-container">
    <h5 class="title is-5 has-text-centered">Total CPU Hours by Resources</h5>
    <div id="pieChart"></div>
  </div>
</template>

<script>
import c3 from 'c3'

export default {
  name: 'pie-chart',
  data () {
    return {
      data: null,
      chart: null
    }
  },
  methods: {
    requestData () {
      var url = xHTTPx + '/myapp/get_csv/data.csv'
      this.$http.get(url).then(response => {
        this.data = response.body.data
        this.drawChart()
      }, response => {
        console.log('Failed to get data!')
      })
    },
    drawChart () {
      var columns = this.data.slice(1)
      this.chart = c3.generate({
        bindto: '#pieChart',
        data: {
          columns: columns,
          type: 'pie',
        },
        pie: {
          label: {
            format: function (value, ratio, id) {
              return value.toString()
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
