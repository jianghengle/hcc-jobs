<template>
  <div>

    <div v-if="error" class="notification is-danger">
      <button class="delete" @click="error=''"></button>
      {{error}}
    </div>

    <div v-if="waiting" class="has-text-centered">
      <v-icon class="icon is-medium fa-spin" name="spinner"></v-icon>
    </div>
    
    <div>
      <div class="dropdown is-pulled-right is-right is-hoverable">
        <div class="dropdown-trigger">
          <button class="button default-btn dropdown-trigger-button" aria-haspopup="true" aria-controls="dropdown-menu">
            <span>Actions</span>
            <span class="icon is-small">
              <v-icon name="chevron-down" scale="0.8"></v-icon>
            </span>
          </button>
        </div>
        <div class="dropdown-menu" id="dropdown-menu" role="menu">
          <div class="dropdown-content">
            <a class="dropdown-item" @click="openEditFileDirectoryModal">
              Edit File Name
            </a>
          </div>
        </div>
      </div>

      <address-bar></address-bar>
    </div>

    <div class="my-container">
      <a class="button" v-if="!link" @click="getDownloadLink">
        <span class="icon is-small">
          <v-icon name="download"></v-icon>
        </span>
        <span>Get Download Link</span>
      </a>
      <a class="button is-loading" v-if="link && !link.link">
        <span>Get Download Link</span>
      </a>
      <a v-if="link && link.link" :href="link.link" target="_blank" download>{{binaryFile.name}}</a>
    </div>
  </div>
</template>

<script>
import AddressBar from './AddressBar'

export default {
  name: 'binary-file',
  components: {
    AddressBar
  },
  data () {
    return {
      waiting: false,
      error: ''
    }
  },
  computed: {
    resourceName () {
      return this.$route.params.resourceName
    },
    server () {
      return this.$store.state.info.servers[this.resourceName]
    },
    filePath () {
      return decodeURIComponent(this.$route.params.filePath)
    },
    binaryFile () {
      return this.$store.state.info.fileCache[this.resourceName][this.filePath]
    },
    link () {
      var link = this.$store.state.info.linkCache[this.resourceName][this.filePath]
      if(link){
        if(Date.now() - link.linkTime < 3600000){
          return link
        }
      }
    },
  },
  methods: {
    openEditFileDirectoryModal () {
      var parts = this.filePath.split('/')
      var name = parts.pop()
      var obj = {path: parts.join('/'), name: name, current: true}
      this.$store.commit('modals/openEditFileDirectoryModal', obj)
    },
    getDownloadLink () {
      this.$store.commit('info/cacheLink', {resourceName: this.resourceName, path: this.filePath, link: ''})
      this.$http.get(this.server + '/myapp/get_download_link/' + this.filePath).then(response => {
        if(response.body.link){
          var link = this.server + response.body.link
          this.$store.commit('info/cacheLink', {resourceName: this.resourceName, path: this.filePath, link: link})
          this.error = ''
        }else{
          this.error = 'Failed to get the file link!'
        }
      }, response => {
        this.error = 'Failed to get the file link!'
      })
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.my-title {
  text-transform: capitalize;
}

.my-container{
  padding-top: 15px;

  .my-editor{
    border-radius: 5px;
  }
}

</style>
