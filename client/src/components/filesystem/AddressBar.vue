<template>
  <div>
    <nav class="breadcrumb" aria-label="breadcrumbs">
      <ul class="my-flex-wrap">
        <li v-for="(p, i) in paths" :class="{'is-active': i==paths.length-1}">
          <router-link :to="p.path">{{p.name}}</router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>


export default {
  name: 'address-bar',
  computed: {
    resourceName () {
      return this.$route.params.resourceName
    },
    filePath () {
      return decodeURIComponent(this.$route.params.filePath)
    },
    paths () {
      var paths = []
      var prefix = ''
      var routePrefix = '/' + this.resourceName + '/fs/directory/'
      this.filePath.split('/').forEach(function(part){
        var path = {name: part}
        if(!prefix){
          prefix = part
        }else{
          prefix = prefix + '/' + part
        }
        path.path = routePrefix + encodeURIComponent(prefix)
        paths.push(path)
      })
      return paths
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.my-flex-wrap {
  flex-wrap: wrap;
  flex-shrink: inherit;
}

</style>
