<!-- ImagePopup.vue -->

<template>
    <v-dialog v-model="localVisible" max-width="none" persistent :key="localVisible">
      <v-card class="image-popup">
        <v-btn small @click="close" class="close-btn">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-img contain :src="image" class="popup-img"></v-img>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  export default {
    props: {
      image: {
        type: String,
        required: true
      },
      visible: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        localVisible: false
      }
    },
    watch: {
      visible(val) {
        this.localVisible = val
        if (val) {
          this.$nextTick(() => {
            const dialogContent = document.querySelector('.v-dialog__content')
            if (dialogContent) {
              dialogContent.style.display = 'flex'
            }
          })
        }
      }
    },
    methods: {
      close() {
        this.$emit('close')
        this.$emit('update:visible', false)
        this.$nextTick(() => {
          const dialogContent = document.querySelector('.v-dialog__content')
          if (dialogContent) {
            dialogContent.style.display = 'none'
          }
        })
      }
    },
    beforeDestroy() {
      const dialogContent = document.querySelector('.v-dialog__content')
      if (dialogContent) {
        dialogContent.style.display = 'none'
      }
}
  }
  </script>
  
<style scoped>
 .image-popup {
    
    /* width: calc(9/12 * 100vw); 
    height: 100vh; */
    width: 65%;
    border: 10px solid #f5f5f5;
    position: relative;
    margin: auto;
 }

 .popup-img {
     width: 100%;
     height: 0;
     padding-top: calc(100% * (3 / 4));
     object-fit: contain;
 }

 .close-btn {
    position: absolute;
    top: -10px;
    right: -10px;
    /* color: white; */
    z-index: 104;
    box-shadow: unset;
    padding: 0;
    /* background-color: #f5f5f5; */
 }

 .v-dialog__content {
    z-index: 105;
    background-color: rgba(0, 0, 0, 0.8); 
 }
</style>