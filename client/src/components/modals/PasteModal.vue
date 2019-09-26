<template>
  <div class="modal"
      :class="{'is-active': opened}">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Paste Files</p>
        <button class="delete" @click="close"></button>
      </header>
      <section class="modal-card-body">
        <div v-if="error" class="notification is-danger">
          <button class="delete" @click="error=''"></button>
          {{error}}
        </div>
        <div class="content">
          <p>Are you sure to paste the files below into {{filePath}}?</p>
          <ul>
            <li v-for="f in files">{{f}}</li>
          </ul>
        </div>
      </section>
      <footer class="modal-card-foot">
        <a class="button is-link" :class="{'is-loading': waiting}" @click="pasteHere">Yes, paste here.</a>
        <a class="button" @click="close">Cancel</a>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'paste-modal',
  data () {
    return {
      waiting: false,
      error: ''
    }
  },
  computed: {
    opened () {
      return this.$store.state.modals.pasteModal.opened
    },
    resourceName () {
      return this.$route.params.resourceName
    },
    server () {
      return this.$store.state.info.servers[this.resourceName]
    },
    files () {
      return this.$store.state.info.clipboard[this.resourceName]
    },
    filePath () {
      return decodeURIComponent(this.$route.params.filePath)
    },
  },
  methods: {
    close(){
      this.$store.commit('modals/closePasteModal')
    },
    pasteHere(){
      if(this.waiting)
        return
      
      var vm = this
      var promises = []
      for(var i=0;i<vm.files.length;i++){
        let message = {src: vm.files[i], dest: this.filePath}
        var promise = vm.$http.post(vm.server + '/myapp/paste_file_directory', message).then(response => {
          if(response.body.path){
            vm.$store.commit('info/cacheFile', {resourceName: vm.resourceName, file: response.body})
          }else{
            vm.error = 'Failed to paste some files!'
          }
        }, response => {
          vm.error = 'Failed to paste some files!'
        })
        promises.push(promise)
      }

      vm.waiting = true
      Promise.all(promises).then((response) => {
        vm.waiting = false
        vm.close()
      }, (response) => {
        vm.waiting = false
        vm.error = 'Some pastes failed...'
      })
    }
  },
}
</script>

<style lang="scss" scoped>

</style>