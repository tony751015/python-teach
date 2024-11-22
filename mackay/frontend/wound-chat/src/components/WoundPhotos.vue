<template>
  <v-col cols="4" class="photo-section">
    <v-toolbar flat dense>
      <v-btn
        v-for="(album, index) in albums"
        :key="index"
        outlined
        :color="currentAlbum === index ? 'primary' : ''"
        @click="switchAlbum(index)"
      >
        {{ album.name }}
      </v-btn>
    </v-toolbar>
    <div class="photo-grid">
      <v-hover v-slot="{ hover }" v-for="(photo, index) in currentPhotos" :key="index">
        <v-card
          :elevation="hover ? 12 : 2"
          :class="{ 'on-hover': hover }"
          class="photo-item"
          @click.stop="openImagePopup(photo.src)"
        >
          <v-img :src="photo.src" class="photo-image">
            <v-card-title class="text-h6 white--text">
              <v-row
                class="flex-column"
                justify="space-between"
              >
                <div class="align-self-center">
                  <v-btn
                    v-if="hover"
                    color="error"
                    icon
                    @click.stop="confirmDelete(photo.id)"
                  >
                    <v-icon>mdi-trash-can-outline</v-icon>
                  </v-btn>
                </div>
              </v-row>
            </v-card-title>
          </v-img>
        </v-card>
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
  }
};
</script>
<style scoped>
.photo-section {
  height: 100%;
  overflow-y: auto;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  padding: 10px;
}

.photo-item {
  position: relative;
  width: 100%;
  aspect-ratio: 4/3; /* 設定寬高比為 4:3 */
  transition: opacity .4s ease-in-out;
  box-shadow: unset;
}

.photo-item:hover {
  opacity: 0.6;
  box-shadow: unset;
 }

.photo-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.photo-image {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 設定填充方式為 contain */
  border-radius: 8px;
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