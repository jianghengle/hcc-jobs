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

    <div v-if="waiting" class="has-text-centered">
      <v-icon class="icon is-medium fa-spin" name="spinner"></v-icon>
    </div>
    <div v-else>
      <div v-if="file">
        <directory v-if="file.type == 'directory'" :directory="file"></directory>
      </div>
    </div>
  </div>
</template>

<script>
import Directory from './Directory'

export default {
  name: 'file-system',
  components: {
    Directory
  },
  data () {
    return {
      waiting: false,
      error: '',
      file: null,
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
      this.waiting = true
      this.$http.get(this.server + '/myapp/get_file/' + this.filePath).then(response => {
        if(response.body.type){
          this.file = response.body
          this.error = ''
        }else{
          this.error = 'Failed to get the file!'
        }
        this.waiting = false
      }, response => {
        this.error = 'Failed to get the file!'
        this.waiting = false
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
