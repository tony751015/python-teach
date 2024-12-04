<template>
  <v-col cols="4" class="photo-section">
    <v-toolbar flat dense>
      <v-tabs
        v-model="localCurrentAlbum"
        centered
        grow
        show-arrows
      >
        <v-tab
            :color="localCurrentAlbum === 0 ? 'primary' : ''"
            @click="updateCurrentAlbum(0)"
          >
          <v-icon>mdi-upload</v-icon>
          已上傳傷口照片
        </v-tab>
        <v-tab
            :color="localCurrentAlbum === 1 ? 'primary' : ''"
            @click="updateCurrentAlbum(1)"
          >
          <v-icon>mdi-magnify-expand</v-icon>
          AI傷口範圍偵測
        </v-tab>
      </v-tabs>
    </v-toolbar>
    <div class="photo-grid">
      <v-hover v-slot="{ hover }" 
       v-for="(photo, index) in currentPhotos" 
       :key="index">
        <div class="photo-item" 
         @click="openImagePopup(photo.src)">
          <img :src="photo.src">
          <v-card-title class="text-h6 white--text" style="">
            <v-row class="flex-column" justify="space-between">
              <div class="align-self-center">
                <v-btn v-if="hover" color="primary" class="delete-btn" icon @click.stop="confirmDelete(photo.id)">
                  <v-icon>mdi-trash-can-outline</v-icon>
                </v-btn>
              </div>
            </v-row>
          </v-card-title>
        </div>
      </v-hover>
    </div>
    <ImagePopup :image="selectedImage" :visible="imagePopupVisible" @close="closeImagePopup" @update:visible="updateVisible"></ImagePopup>
  </v-col>
</template>

<script>
import ImagePopup from '@/components/ImagePopup.vue';

export default {
  components: {
    ImagePopup
  },
  props: {
    albums: {
      type: Array,
      required: true
    },
    currentAlbum: {
      type: Number,
      required: true
    }
  },
  computed: {
    currentPhotos() {
      return this.albums[this.currentAlbum]?.photos || [];
    }
  },
  data() {
  return {
    selectedImage: '',
    imagePopupVisible: false,
    localCurrentAlbum: this.currentAlbum
  };
},
  methods: {
  // 開啟圖片彈窗
     openImagePopup(imageUrl) {
    if (event.target.classList.contains('v-btn')) return;
      this.selectedImage = imageUrl;
      this.imagePopupVisible = true;
    },
    // 關閉圖片彈窗
    closeImagePopup() {
      this.imagePopupVisible = false;
      this.selectedImage = '';
    },
    updateVisible(val) {
      this.imagePopupVisible = val
    },
    switchAlbum(index) {
      this.$emit('update:currentAlbum', index);
    },
    confirmDelete(photoId) {
      if (confirm('確定要刪除這張照片嗎？')) {
        const album = this.albums[this.currentAlbum];
        album.photos = album.photos.filter((photo) => photo.id !== photoId);
      }
    },
    updateCurrentAlbum(index) {
      this.localCurrentAlbum = index
      this.$emit('update:currentAlbum', index)
    }
  }
};
</script>
<style scoped>
.photo-section {
  height: 100%;
  overflow-y: auto;
}
.delete-btn{
  background-color: #fff !important;
  position: absolute;
  top: 5px;
  right: 5px;
  width: 20px;
  height: 20px;
}
.delete-btn .v-icon{
  width: 15px;
  height: 15px;
  font-size: 15px;
}
.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  padding: 10px;
}

.photo-item {
  width: 100%; 
  aspect-ratio: 4/3; 
  position: relative;
  margin-bottom: -0.5rem;
  cursor: pointer;
}
.photo-item img {
  width: 100%; 
  height: 100%; 
  object-fit: fill;
  border-radius: 8px;
}
.photo-item:hover img{
  opacity: 0.6;
  /* box-shadow: unset; */
 }

.photo-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
.v-application .text-h6 {
  /* line-height: 4rem; */
  position: absolute; 
  top: 0; 
  left: 0; 
  right: 0; 
  bottom: 0;
}


.photo-hover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
.v-responsive__sizer {
  padding-bottom: 75%;
}


</style>