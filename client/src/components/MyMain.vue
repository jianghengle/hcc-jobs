<template>
  <div>
    <div class="container">
      <div class="columns">
        <div class="column">
          <bar-chart></bar-chart>
        </div>
        <div class="column">
          <pie-chart></pie-chart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BarChart from './charts/BarChart'
import PieChart from './charts/PieChart'

export default {
  name: 'my-main',
  components: {
    BarChart,
    PieChart
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
