<template>
  <div class="modal"
      :class="{'is-active': opened}">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">New File</p>
        <button class="delete" @click="close"></button>
      </header>
      <section class="modal-card-body">
        <div v-if="error" class="notification is-danger">
          <button class="delete" @click="error=''"></button>
          {{error}}
        </div>
        <div class="field">
          <label class="label">File Name</label>
          <div class="control">
            <input class="input" type="text" placeholder="New file name" v-model="filename">
          </div>
        </div>
      </section>
      <footer class="modal-card-foot">
        <a class="button is-link" :class="{'is-loading': waiting}" @click="createFile">Create New File</a>
        <a class="button" @click="close">Cancel</a>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'new-file-modal',
  data () {
    return {
      waiting: false,
      error: '',
      filename: ''
    }
  },
  computed: {
    opened () {
      return this.$store.state.modals.newFileModal.opened
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
  },
  methods: {
    close(){
      this.$store.commit('modals/closeNewFileModal')
    },
    createFile(){
      this.filename = this.filename.trim()
      this.waiting = true
      var message = {path: this.filePath, filename: this.filename}
      this.$http.post(this.server + '/myapp/create_file', message).then(response => {
        if(response.body.path){
          this.$store.commit('info/cacheFile', {resourceName: this.resourceName, file: response.body})
          this.close()
          this.error = ''
        }else{
          this.error = 'Failed to create the file!'
          this.$store.commit('user/reset')
        }
        this.waiting = false
      }, response => {
        this.error = 'Failed to create the file!'
        this.waiting = false
      })
    }
  },
}
</script>

<style lang="scss" scoped>

</style>