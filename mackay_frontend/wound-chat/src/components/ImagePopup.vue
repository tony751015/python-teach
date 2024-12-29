<!-- ImagePopup.vue -->
<template>
  <v-dialog v-model='localVisible' max-width="600" persistent>
    <v-card class="image-popup">
      <v-btn small @click="close" class="close-btn">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <!-- <v-img fill :src="image" class="popup-img"></v-img> -->
       <div class="imgbox">
        <img :src="image" class="popup-img" alt="">
       </div>
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

  created() {
    this.localVisible = this.visible;
  },

  data() {
    return {
      localVisible: false,
    }
  },
  // watch: {
    // visible() {
    //   // this.localVisible = val
    //   console.log('visible')
    //   if (this.visible) {
    //     this.$nextTick(() => {
    //       const dialogContent = document.querySelector('.v-dialog__content')
    //       if (dialogContent) {
    //         dialogContent.style.display = 'flex'
    //       }
    //     })
    //   }
    // }
  // },
  methods: {
    close() {
      this.$emit('close', false)
      // this.$emit('update:visible', false)
      this.localVisible = false;
      // this.$nextTick(() => {
      //   const dialogContent = document.querySelector('.v-dialog__content')
      //   if (dialogContent) {
      //     dialogContent.style.display = 'none'
      //   }
      // })
    }
  },
  // beforeDestroy() {
  //   const dialogContent = document.querySelector('.v-dialog__content')
  //   if (dialogContent) {
  //     dialogContent.style.display = 'none'
  //   }
  // }
}
</script>
  
<style scoped>
 .image-popup {
    /* width: calc(9/12 * 100vw); 
    height: 100vh; */
    /* width: 65%; */
    /* border: 10px solid #f5f5f5; */
    position: relative;
    margin: auto;
    width: calc(100% - 20px);
    height: calc(100% - 20px);
    
 }
 .imgbox {
    width: 100%;
    height: 100%;
    border: 10px solid #f5f5f5;
    aspect-ratio: 4/3;
    overflow: auto;
 }
 .popup-img {
    width: 100%;
    /* object-fit: fill; */
 }

 .close-btn {
    position: absolute;
    top: 0px;
    right: 0px;
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