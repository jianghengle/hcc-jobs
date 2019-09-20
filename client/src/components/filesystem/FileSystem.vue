<template>
  <div>
    <h1 class="title my-title">{{resourceName}}</h1>

    <div v-if="!token" class="notification is-danger">
      You need to login first to see your files!
    </div>

    <div v-if="error" class="notification is-danger">
      <button class="delete" @click="error=''"></button>
      Failed to get the directory or file.
    </div>

    <div v-if="file">
      <directory v-if="file.type == 'directory'"></directory>
      <text-file v-if="file.type == 'text file'"></text-file>
      <symbolic-link v-if="file.type == 'symbolic link'"></symbolic-link>
      <binary-file v-if="file.type == 'binary file'"></binary-file>
    </div>
    <div v-else class="has-text-centered">
      <v-icon class="icon is-medium fa-spin" name="spinner"></v-icon>
    </div>
  </div>
</template>

<script>
import Directory from './Directory'
import TextFile from './TextFile'
import SymbolicLink from './SymbolicLink'
import BinaryFile from './BinaryFile'

export default {
  name: 'file-system',
  components: {
    Directory,
    TextFile,
    SymbolicLink,
    BinaryFile
  },
  data () {
    return {
      error: '',
    }
  },
  computed: {
    token () {
      return this.$store.state.user.token
    },
    resourceName () {
      return this.$route.params.resourceName
    },
    server () {
      return this.$store.state.info.servers[this.resourceName]
    },
    filePath () {
      return decodeURIComponent(this.$route.params.filePath)
    },
    file () {
      return this.$store.state.info.fileCache[this.resourceName][this.filePath]
    }
  },
  watch: {
    resourceName: function (val) {
      this.requestFile()
    },
    filePath: function (val) {
      this.requestFile()
    },
  },
  methods: {
    requestFile () {
      this.$http.get(this.server + '/myapp/get_file/' + this.filePath).then(response => {
        if(response.body.type){
          this.$store.commit('info/cacheFile', {resourceName: this.resourceName, file: response.body})
          this.error = ''
        }else{
          this.error = 'Failed to get the file!'
        }
      }, response => {
        this.error = 'Failed to get the file!'
      })
    },
  },
  mounted () {
    if(this.token){
      this.requestFile()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.my-title {
  text-transform: capitalize;
}


</style>
