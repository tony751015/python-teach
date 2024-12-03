<template>
<v-dialog
  v-model="dialog"
  hide-overlay
  persistent
  width="300"
>
  <v-card
    color="point-1"
    
  >
    <v-card-text class="loading-text">
      {{ showText }}
      <v-progress-linear
        indeterminate
        color="main-green"
        class="mb-0"
      ></v-progress-linear>
    </v-card-text>
  </v-card>
</v-dialog>
</template>

<script>
  export default {
    props: {
      showText: String,
      active: Boolean,
    },
    

    data() {
      return {
        dialog: this.active
      }
    }
  }
</script>

<style scoped>
  .loading-text {
    color:#2D9CA0 !important;
  }
</style>