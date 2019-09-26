<template>
  <div class="modal"
      :class="{'is-active': opened}">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Delete Multiple Files</p>
        <button class="delete" @click="close"></button>
      </header>
      <section class="modal-card-body">
        <div v-if="error" class="notification is-danger">
          <button class="delete" @click="error=''"></button>
          {{error}}
        </div>
        <div class="content">
          <p>Are you sure to delete the files below?</p>
          <ul>
            <li v-for="f in files">{{f.name}}</li>
          </ul>
        </div>
      </section>
      <footer class="modal-card-foot">
        <a class="button is-danger" :class="{'is-loading': waiting}" @click="deleteMultiple">Yes, delete them all.</a>
        <a class="button" @click="close">Cancel</a>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'delete-multiple-modal',
  data () {
    return {
      waiting: false,
      error: ''
    }
  },
  computed: {
    opened () {
      return this.$store.state.modals.deleteMultipleModal.opened
    },
    resourceName () {
      return this.$route.params.resourceName
    },
    server () {
      return this.$store.state.info.servers[this.resourceName]
    },
    files () {
      return this.$store.state.modals.deleteMultipleModal.files
    },
    filePath () {
      return decodeURIComponent(this.$route.params.filePath)
    },
  },
  methods: {
    close(){
      this.$store.commit('modals/closeDeleteMultipleModal')
    },
    deleteMultiple(){
      if(this.waiting)
        return
      
      var vm = this
      var promises = []
      for(var i=0;i<vm.files.length;i++){
        let message = {path: vm.filePath, name: vm.files[i].name}
        var promise = vm.$http.post(vm.server + '/myapp/delete_file_directory', message).then(response => {
          if(response.body.path){
            vm.$store.commit('info/cacheFile', {resourceName: vm.resourceName, file: response.body})
          }else{
            vm.error = 'Failed to delete some files!'
          }
        }, response => {
          vm.error = 'Failed to delete some files!'
        })
        promises.push(promise)
      }

      Promise.all(promises).then((response) => {
        vm.waiting = false
        vm.close()
      }, (response) => {
        vm.waiting = false
        vm.error = 'Some deletes failed...'
      })
    }
  },
}
</script>

<style lang="scss" scoped>

</style>