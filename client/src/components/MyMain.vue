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
      <div class="columns">
        <div class="column is-half">
          <div class="echart-figure">
            <v-chart :options="option" autoresize />
          </div>
        </div>
        <div class="column is-half">
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
  data () {
    return {
      option: {
        title: {
          text: '饼图程序调用高亮示例',
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: ['直接访问', '邮件营销', '联盟广告', '视频广告', '搜索引擎'],
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: '65%',
            center: ['50%', '60%'],
            data: [
              { value: 335, name: '直接访问' },
              { value: 310, name: '邮件营销' },
              { value: 234, name: '联盟广告' },
              { value: 135, name: '视频广告' },
              { value: 1548, name: '搜索引擎' }
            ],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.echart-figure{
  display: inline-block;
  position: relative;
  margin: 2em auto;
  border: 1px solid rgba(0, 0, 0, .1);
  border-radius: 8px;
  box-shadow: 0 0 45px rgba(0, 0, 0, .2);
  padding: 1.5em 2em;
  width: 100%;
  min-width: calc(40vw + 4em);

  .echarts {
    width: 100%;
    min-width: 400px;
    height: 300px;
  }
}

</style>
