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
            <a class="dropdown-item" @click="openEditFileDirectoryModal">
              Edit File Name
            </a>
          </div>
        </div>
      </div>

      <address-bar></address-bar>
    </div>

    <div class="my-container">
      <pre>{{symbolicLink.content}}</pre>
    </div>
  </div>
</template>

<script>
import AddressBar from './AddressBar'

export default {
  name: 'symbolic-link',
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
    symbolicLink () {
      return this.$store.state.info.fileCache[this.resourceName][this.filePath]
    },
  },
  methods: {
    openEditFileDirectoryModal () {
      var parts = this.filePath.split('/')
      var name = parts.pop()
      var obj = {path: parts.join('/'), name: name, current: true}
      this.$store.commit('modals/openEditFileDirectoryModal', obj)
    },
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
}

</style>
