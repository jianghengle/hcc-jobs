<template>
  <div>
    <h1 class="title">Rhino</h1>
    <div>Rhino is intended for large memory (RAM) computing needs. Rhino has 4 AMD Interlagos CPUs (64 cores) per node, with either 192GB or 256GB RAM per node in the default partition. For extremely large RAM needs, there is also a ‘highmem’ partition with 2 x 512GB and 2 x 1TB nodes.</div>

    <div class="field is-grouped my-buttons">
      <p class="control">
        <router-link :to="'/rhino/jobs'" class="button is-link is-outlined">
          See Your Jobs
        </router-link>
      </p>
      <p class="control">
        <router-link :to="'/rhino/fs/%24HOME'" class="button is-link is-outlined">
          See You Files
        </router-link>
      </p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'rhino',
  data () {
    return {
      message: ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

.my-buttons {
  margin-top: 20px;
}

</style>
