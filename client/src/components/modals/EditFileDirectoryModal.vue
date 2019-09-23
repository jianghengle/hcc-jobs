<template>
  <div class="modal"
      :class="{'is-active': opened}">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Edit File/Directory</p>
        <button class="delete" @click="close"></button>
      </header>
      <section class="modal-card-body">
        <div v-if="error" class="notification is-danger">
          <button class="delete" @click="error=''"></button>
          {{error}}
        </div>
        <div class="field">
          <label class="label">File/Directory Name</label>
          <div class="control">
            <input class="input" type="text" placeholder="File/Directory name" v-model="newName">
          </div>
        </div>
      </section>
      <footer class="modal-card-foot">
        <a class="button is-link" :class="{'is-loading': waiting}" :disabled="!canUpdate" @click="update">Update</a>
        <a class="button is-danger" :class="{'is-loading': waiting}" :disabled="canUpdate" @click="deleteIt">Delete</a>
        <a class="button" @click="close">Cancel</a>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'edit-file-directory-modal',
  data () {
    return {
      waiting: false,
      error: '',
      newName: ''
    }
  },
  computed: {
    opened () {
      return this.$store.state.modals.editFileDirectoryModal.opened
    },
    resourceName () {
      return this.$route.params.resourceName
    },
    server () {
      return this.$store.state.info.servers[this.resourceName]
    },
    current () {
      return this.$store.state.modals.editFileDirectoryModal.current
    },
    path () {
      return this.$store.state.modals.editFileDirectoryModal.path
    },
    name () {
      return this.$store.state.modals.editFileDirectoryModal.name
    },
    canUpdate () {
      return this.newName.trim() && this.newName.trim() != this.name
    }
  },
  watch: {
    name: function (val) {
      if(val){
        this.newName = val
      }
    },
  },
  methods: {
    close(){
      this.$store.commit('modals/closeEditFileDirectoryModal')
    },
    update(){
      if(!this.canUpdate || this.waiting)
        return
      this.newName = this.newName.trim()
      this.waiting = true
      var message = {path: this.path, oldName: this.name, newName: this.newName}
      this.$http.post(this.server + '/myapp/update_file_directory', message).then(response => {
        if(response.body.parent){
          this.$store.commit('info/cacheFile', {resourceName: this.resourceName, file: response.body.parent})
          this.$store.commit('info/cacheFile', {resourceName: this.resourceName, file: response.body.child})
          if(this.current){
            var path = '/' + this.resourceName + '/fs/' + encodeURIComponent(response.body.child.path)
            this.$router.replace(path)
          }
          this.close()
          this.error = ''
        }else{
          this.error = 'Failed to update!'
        }
        this.waiting = false
      }, response => {
        this.error = 'Failed to update!'
        this.waiting = false
      })
    },
    deleteIt(){
      if(this.canUpdate || this.waiting)
        return
      var confirm = {
        title: 'Delete',
        message: 'Are you sure to delete this file or directory?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.deleteConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    deleteConfirmed () {
      this.waiting = true
      var message = {path: this.path, name: this.name}
      this.$http.post(this.server + '/myapp/delete_file_directory', message).then(response => {
        if(response.body.path){
          this.$store.commit('info/cacheFile', {resourceName: this.resourceName, file: response.body})
          if(this.current){
            var path = '/' + this.resourceName + '/fs/' + encodeURIComponent(response.body.path)
            this.$router.replace(path)
          }
          this.close()
          this.error = ''
        }else{
          this.error = 'Failed to update!'
        }
        this.waiting = false
      }, response => {
        this.error = 'Failed to update!'
        this.waiting = false
      })
    },
  },
}
</script>

<style lang="scss" scoped>

</style>