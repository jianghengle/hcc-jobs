<template>
  <div class="modal" :class="{'is-active': opened}">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Upload Files</p>
        <button class="delete" @click="close"></button>
      </header>
      <section class="modal-card-body">
        <div v-if="error" class="notification is-danger">
          <button class="delete" @click="error=''"></button>
          {{error}}
        </div>
        <div v-if="opened" class="file files-input">
          <label class="file-label">
            <input class="file-input" type="file" multiple @change="onFileChange">
            <span class="file-cta">
              <span class="file-icon">
                <v-icon name="upload"></v-icon>
              </span>
              <span class="file-label">
                Choose file
              </span>
            </span>
          </label>
        </div>
        <div v-if="Object.keys(uploads).length">
          <table class="table is-narrow is-fullwidth">
            <thead>
              <tr>
                <th>File Name</th>
                <th class="number-cell">Size</th>
                <th class="number-cell">Progress</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(v, k) in uploads">
                <td>{{v.filename}}</td>
                <td class="number-cell">{{v.size}}</td>
                <td class="number-cell">{{v.percentage}}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
      <footer class="modal-card-foot">
        <a class="button is-link" :class="{'is-loading': waiting}" @click="upload" :disabled="!files || !files.length">Upload</a>
        <a class="button" @click="close">Cancel</a>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'upload-modal',
  data () {
    return {
      waiting: false,
      error: '',
      files: null,
      uploads: {},
    }
  },
  computed: {
    opened () {
      return this.$store.state.modals.uploadModal.opened
    },
    filePath () {
      return decodeURIComponent(this.$route.params.filePath)
    },
    resourceName () {
      return this.$route.params.resourceName
    },
    server () {
      return this.$store.state.info.servers[this.resourceName]
    },
    canUpload () {
      return this.files.length
    }
  },
  watch: {
    opened: function (val) {
      if(val){
        this.files = []
        this.uploads = {}
        this.waiting = false
        this.error = ''
      }
    },
  },
  methods: {
    close(){
      Object.values(this.uploads).forEach(function(upload){
        if(!upload.done && upload.request){
          upload.request.abort()
        }
      })
      this.$store.commit('modals/closeUploadModal')
    },
    onFileChange(e){
      var files = e.target.files || e.dataTransfer.files
      if (!files.length)
        return
      this.files = files
      var uploads = {}
      for(var i=0;i<files.length;i++){
        var file = files[i]
        uploads[file.name] = {
          filename: file.name,
          size: file.size,
          loaded: 0,
          percentage: 0,
          done: false,
          request: null
        }
      }
      this.uploads = uploads
    },
    upload(){
      if(this.waiting || !this.files.length) return
      this.waiting = true

      var vm = this
      var promises = []
      for(var i=0;i<vm.files.length;i++){
        let file = vm.files[i]
        if(vm.uploads[file.name].done)
          continue

        var formData = new FormData()
        formData.append('file', file)
        var promise = vm.$http.post(vm.server + '/myapp/upload_file/' + vm.filePath, formData, {
          before: request => {
            vm.uploads[file.name].request = request
          },
          progress: e => {
            var upload = vm.uploads[file.name]
            upload.loaded = e.loaded
            upload.percentage = Math.round((e.loaded / e.total) * 100)
          }
        }).then((response) => {
          var upload = vm.uploads[file.name]
          upload.loaded = upload.size
          upload.percentage = 100
          upload.done = true
          upload.request = null
          vm.$store.commit('info/cacheFile', {resourceName: vm.resourceName, file: response.body})
        }, (response) => {
          var upload = vm.uploads[file.name]
          upload.loaded = 0
          upload.percentage = 0
          upload.request = null
        })
        promises.push(promise)
      }

      Promise.all(promises).then((response) => {
        vm.waiting = false
        vm.close()
      }, (response) => {
        vm.waiting = false
        vm.error = 'Some uploads failed...'
      })
    }
  },
}
</script>

<style lang="scss" scoped>
.files-input {
  margin-bottom: 10px;
}

.number-cell {
  text-align: right;
}


</style>