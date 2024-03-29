<template>
  <div>

    <div v-if="error" class="notification is-danger">
      <button class="delete" @click="error=''"></button>
      Error
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
            <router-link class="dropdown-item" v-for="fs in fileSystems" :key="'fs-' + fs.path" :to="fs.to">
              {{fs.path}}
            </router-link>
            <hr class="dropdown-divider">
            <a class="dropdown-item" @click="openNewDirectoryModal">
              New Directory
            </a>
            <a class="dropdown-item" @click="openNewFileModal">
              New File
            </a>
            <hr class="dropdown-divider">
            <a class="dropdown-item" @click="openUploadModal">
              Upload File
            </a>
            <hr class="dropdown-divider" v-if="filePath.split('/').length > 1">
            <a class="dropdown-item" v-if="filePath.split('/').length > 1" @click="openEditFileDirectoryModal(null)">
              Edit Directory
            </a>
            <hr class="dropdown-divider" v-if="selectedFiles.length || (clipboard && clipboard.length)">
            <a class="dropdown-item" v-if="selectedFiles.length" @click="copySelectFiles">
              <span>Copy Selected ({{selectedFiles.length}})</span>
            </a>
            <a class="dropdown-item" v-if="clipboard && clipboard.length" @click="pasteHere">
              <span>Paste Here ({{clipboard.length}})</span>
            </a>
            <hr class="dropdown-divider" v-if="selectedFiles.length">
            <a class="dropdown-item" v-if="selectedFiles.length" @click="openDeleteMultipleModal">
              <span class="has-text-danger">Delete Selected ({{selectedFiles.length}})</span>
            </a>
          </div>
        </div>
      </div>

      <address-bar></address-bar>
    </div>

    <div>
      <table class="table is-fullwidth is-hoverable is-striped">
        <thead>
          <tr>
            <th>{{files.length}}</th>
            <th>Type</th>
            <th>Name</th>
            <th>Size</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(f, i) in files" class="clickable" @click="viewFile(f)">
            <td onclick="event.stopPropagation()"><span class="checkbox"><input type="checkbox" v-model="selections[i]"></span></td>
            <td>
              <span class="icon" v-if="f.type=='directory'">
                <v-icon name="folder"/>
              </span>
            </td>
            <td :class="{'has-text-weight-bold':f.type=='directory'}">{{f.name}}</td>
            <td><span v-if="f.type!='directory'">{{f.size}}</span></td>
            <td>{{f.date}}</td>
            <td>
              <a class="icon" @click.stop="openEditFileDirectoryModal(f)">
                <v-icon name="edit"/>
              </a>
              <a class="icon" @click.stop="copySingleFile(f)">
                <v-icon name="copy"/>
              </a>
              <a class="icon" v-if="f.type!='directory' && !f.link" @click.stop="getDownloadLink(f)">
                <v-icon name="download"/>
              </a>
              <a class="icon" v-if="f.type!='directory' && f.link && !f.link.link">
                <v-icon class="icon is-small fa-spin" name="spinner"></v-icon>
              </a>
              <a :id="'download '+f.name" class="icon" v-if="f.type!='directory' && f.link && f.link.link" onclick="event.stopPropagation()" target="_blank" :href="f.link.link" download>
                link
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import AddressBar from './AddressBar'

export default {
  name: 'directory',
  components: {
    AddressBar
  },
  data () {
    return {
      waiting: false,
      error: '',
      selections: []
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
    directory () {
      return this.$store.state.info.fileCache[this.resourceName][this.filePath]
    },
    linkCache () {
      return this.$store.state.info.linkCache[this.resourceName]
    },
    files () {
      var rows = this.directory.content.split('\n')
      rows.shift()
      var files = []
      for(var i=0;i<rows.length;i++){
        var row = rows[i]
        var file = {}
        var parts = row.split('"')
        file.name = parts[1]
        file.path = this.directory.path + '/' + file.name
        file.date = parts[0].slice(-13 ,-1)
        var ss = parts[0].split(/\ +/)
        file.type = ss[1] > 1 ? 'directory' : 'file'
        file.size = ss[3]
        if(this.linkCache[file.path]){
          var link = this.linkCache[file.path]
          if(Date.now() - link.linkTime < 3600000){
            file.link = link
          }
        }
        files.push(file)
      }
      return files
    },
    fileSystems () {
      var vm = this
      return this.$store.state.info.fileSystems[this.resourceName].map(function(fs){
        return {
          path: fs,
          to: '/' + vm.resourceName + '/fs/directory/' + encodeURIComponent(fs)
        }
      })
    },
    selectedFiles () {
      var files = []
      for(var i=0;i<this.files.length;i++){
        if(this.selections[i]){
          files.push(this.files[i])
        }
      }
      return files
    },
    clipboard () {
      return this.$store.state.info.clipboard[this.resourceName]
    }
  },
  watch: {
    directory: function (val) {
      this.$nextTick(function(){
        this.resetSelections()
      })
    },
  },
  methods: {
    viewFile (f) {
      var path = '/' + this.resourceName + '/fs/' + f.type + '/' + encodeURIComponent(f.path)
      this.$router.push(path)
    },
    openNewFileModal () {
      this.$store.commit('modals/openNewFileModal')
    },
    openNewDirectoryModal () {
      this.$store.commit('modals/openNewDirectoryModal')
    },
    openEditFileDirectoryModal (f) {
      if(f){
        var obj = {path: this.directory.path, name: f.name, current: false}
      }else{
        var parts = this.filePath.split('/')
        var name = parts.pop()
        var obj = {path: parts.join('/'), name: name, current: true}
      }
      this.$store.commit('modals/openEditFileDirectoryModal', obj)
    },
    openUploadModal () {
      this.$store.commit('modals/openUploadModal')
    },
    getDownloadLink (f) {
      this.$store.commit('info/cacheLink', {resourceName: this.resourceName, path: f.path, link: ''})
      this.$http.get(this.server + '/myapp/get_download_link/' + f.path).then(response => {
        if(response.body.link){
          var link = this.server + response.body.link
          this.$store.commit('info/cacheLink', {resourceName: this.resourceName, path: f.path, link: link})
          this.error = ''
          this.$nextTick(function(){
            document.getElementById('download ' + f.name).click()
          })
        }else{
          this.error = 'Failed to get the file link!'
        }
      }, response => {
        this.error = 'Failed to get the file link!'
      })
    },
    resetSelections () {
      var selections = []
      for(var i=0;i<this.files.length;i++){
        if(this.selections[i]){
          selections.push(true)
        }else{
          selections.push(false)
        }
      }
    },
    openDeleteMultipleModal () {
      this.$store.commit('modals/openDeleteMultipleModal', this.selectedFiles)
    },
    copySelectFiles () {
      var obj = {}
      obj[this.resourceName] = this.selectedFiles.map(f => {return f.path})
      this.$store.commit('info/setClipboard', obj)
    },
    copySingleFile (f) {
      var obj = {}
      obj[this.resourceName] = [f.path]
      this.$store.commit('info/setClipboard', obj)
    },
    pasteHere () {
      this.$store.commit('modals/openPasteModal')
    }
  },
  mounted () {
    this.$nextTick(function(){
      this.resetSelections()
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.my-title {
  text-transform: capitalize;
}


</style>
