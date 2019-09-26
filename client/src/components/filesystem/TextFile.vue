<template>
  <div>

    <div v-if="error" class="notification is-danger">
      <button class="delete" @click="error=''"></button>
      {{error}}
    </div>

    <div v-if="success" class="notification is-success">
      <button class="delete" @click="success=''"></button>
      {{success}}
    </div>
    
    <div>
      <div class="is-pulled-right">
        <a class="button is-danger update-button" :class="{'is-loading': waiting}" :disabled="!changed" @click="updateText">Update</a>
        <div class="dropdown is-right is-hoverable">
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
              <hr class="dropdown-divider">
              <a class="dropdown-item" @click="sbatchFile">
                Submit Job (sbatch)
              </a>
            </div>
          </div>
        </div>
      </div>
      <address-bar></address-bar>
    </div>

    <div class="my-container">
      <prism-editor v-model="text" :line-numbers="true" language="shell" class="my-editor"></prism-editor>
    </div>
  </div>
</template>

<script>
import AddressBar from './AddressBar'
import PrismEditor from "vue-prism-editor";

export default {
  name: 'text-file',
  components: {
    AddressBar,
    PrismEditor
  },
  data () {
    return {
      waiting: false,
      error: '',
      text: '',
      success: ''
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
    textFile () {
      return this.$store.state.info.fileCache[this.resourceName][this.filePath]
    },
    changed () {
      return this.text != this.textFile.content
    }
  },
  methods: {
    openEditFileDirectoryModal () {
      var parts = this.filePath.split('/')
      var name = parts.pop()
      var obj = {path: parts.join('/'), name: name, current: true}
      this.$store.commit('modals/openEditFileDirectoryModal', obj)
    },
    updateText () {
      if(!this.changed || this.waiting)
        return
      this.waiting = true
      this.$http.post(this.server + '/myapp/update_text/' + this.filePath, {text: this.text}).then(response => {
        if(response.body.path){
          this.$store.commit('info/cacheFile', {resourceName: this.resourceName, file: response.body})
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
    sbatchFile () {
      var confirm = {
        title: 'Submit Job',
        message: 'Are you sure to submit a new job (sbatch this file)?',
        button: 'Yes, I am sure.',
        callback: {
          context: this,
          method: this.sbatchFileConfirmed,
          args: []
        }
      }
      this.$store.commit('modals/openConfirmModal', confirm)
    },
    sbatchFileConfirmed () {
      this.waiting = true
      this.success = ''
      this.$http.post(this.server + '/myapp/submit_job', {path: this.filePath}).then(response => {
        if(response.body.ok){
          this.success = response.body.result
          this.error = ''
        }else{
          this.error = 'Failed to update!'
        }
        this.waiting = false
      }, response => {
        this.error = 'Failed to submit job!'
        this.waiting = false
      })
    }
  },
  mounted () {
    this.text = this.textFile.content
  }
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

.update-button {
  margin-right: 5px;
}

</style>
