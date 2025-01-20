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
          Uploaded wound photo
        </v-tab>
        <v-tab
            :color="localCurrentAlbum === 1 ? 'primary' : ''"
            @click="updateCurrentAlbum(1)"
          >
          <v-icon>mdi-magnify-expand</v-icon>
          AI wound area detection
        </v-tab>
      </v-tabs>
    </v-toolbar>
    <div class="photo-zone">
      <div class="photo-grid" infinite-wrapper>
        <v-hover v-slot="{ hover }" 
        v-for="(photo, index) in filteredPhotos" 
        :key="index">
          <div class="photo-item" 
          @click="openImagePopup(`${IMG_PATH}media/${photo.src}`)">
            <img :src="`${IMG_PATH}media/${photo.src}`">
            <v-card-title class="text-h6 white--text" style="">
              <v-row class="flex-column" justify="space-between">
                <div class="align-self-center">
                  <v-btn v-if="hover && !userProfile.super_user" color="primary" class="delete-btn" icon @click.stop="confirmDelete(photo.id)">
                    <v-icon>mdi-trash-can-outline</v-icon>
                  </v-btn>
                </div>
              </v-row>
            </v-card-title>
          </div>
        </v-hover>
        <infinite-loading ref="infiniteLoading" force-use-infinite-wrapper=".photo-grid" @infinite="loadMorePhotos">
          <div slot="no-more" class="infini-photo-note grey--text text--lighten-1 font-small">No more photo</div>
          <div slot="no-results" class="infini-photo-note grey--text text--lighten-1 font-small">No more photo</div>
        </infinite-loading>
      </div>
    </div>
    
    <!-- <ImagePopup :image="selectedImage" :visible="imagePopupVisible" @close="closeImagePopup" @update:visible="updateVisible"></ImagePopup> -->
    <ImagePopup
      :key="`imgpop-${popImgKey}`"
      :image="selectedImage"
      :visible="imagePopupVisible"
      @close="closeImagePopup">
    </ImagePopup>
  </v-col>
</template>

<script>
import axios from 'axios';
import ImagePopup from '@/components/ImagePopup.vue';
import InfiniteLoading from 'vue-infinite-loading';

export default {
  components: {
    ImagePopup,
    InfiniteLoading
  },
  props: {
    currentAlbum: {
      type: Number,
      required: true
    },
    selectedPatientId: {
      type: [Number, null],
      required: true
    }, 
    selectedChatroom: {
      type: [String, null],
      required: true
    }

  },
  data() {
    return {
      albums: [], // 初始化 albums 為空陣列
      selectedImage: '',
      popImgKey: 1,
      imagePopupVisible: false,
      localCurrentAlbum: this.currentAlbum,
      page: 1, // 用於追蹤當前頁數
      size: 2, // 每頁顯示的數量
      hasMore: true, // 用於追蹤是否有更多數據
      infiniteId: 0 // 用於重置 InfiniteLoading
    };
  },
  computed: {
    // currentPhotos() {
    //   return this.albums[this.currentAlbum]?.photos || [];
    // },
    filteredPhotos() {
      return this.albums[this.currentAlbum]?.photos.filter(photo => !photo.is_carer_user) || [];
    }
  },
  watch: {
    selectedChatroom(newRoomPath) {
      if (newRoomPath != null && newRoomPath != 'noSelected') {
        this.page = 1;
        this.hasMore = true;
        this.albums = [];
        if (this.$refs.infiniteLoading) {
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:reset');
        }
        // this.loadPhotosForPatient(newId);
      } else {
        this.albums = []; // 如果 selectedPatientId 為 null 或 -1，清空 albums
      }
    }
  },
  methods: {
    // loadPhotosForPatient(patientId) {
    //   alert('loadPhotosForPatient');
    //   return new Promise((resolve, reject) => {
    //     if (patientId === -1) {
    //       this.albums = [];
    //       resolve();
    //       return;
    //     }
    //     this.page = 1; // 重置頁數
    //     axios.get(`http://127.0.0.1:8000/api/chat/photo`, {
    //       params: {
    //         user_id: patientId,
    //         page: this.page,
    //         size: this.size
    //       }
    //     })
    //     .then(response => {
    //       const newPhotos = response.data.results.map(photo => ({
    //         id: photo.record_id,
    //         src: photo.media_url
    //       }));

    //       this.albums = [{ photos: newPhotos }];
    //       this.page = 2; // 下一次加載從第二頁開始
    //       this.hasMore = newPhotos.length >= this.size;
    //       resolve();
    //     })
    //     .catch(error => {
    //       console.error('Error loading photos for patient:', error);
    //       reject(error);
    //     });
    //   });
    // },
    // fetchPhotos() {
    //   if (!this.hasMore || this.selectedPatientId === -1) {
    //     return;
    //   }
    //   axios.get('http://127.0.0.1:8000/api/chat/photo', {
    //     params: {
    //       user_id: this.selectedPatientId,
    //       page: this.page,
    //       size: this.size
    //     }
    //   })
    //   .then(response => {
    //     if (this.localCurrentAlbum === 0) {
    //       const newPhotos = response.data.results.map(photo => ({
    //         id: photo.record_id,
    //         src: photo.media_url
    //       }));
    //       console.log(response.data.results);
    //       if (newPhotos.length > 0) {
    //         if (this.page === 1) {
    //           this.albums = [{ photos: newPhotos }];
    //         } else {
    //           this.albums[0].photos.push(...newPhotos);
    //         }
    //         this.page += 1; // 增加頁數
    //       } else {
    //         alert('沒有更多照片');
    //         this.hasMore = false; // 如果沒有新數據，設置 hasMore 為 false
    //       }
    //     }
    //   })
    //   .catch(error => {
    //     console.error('Error fetching photos:', error);
    //     this.hasMore = false; // 在發生錯誤時停止加載
    //   });
    // },
    loadMorePhotos($state) {
        const getJWTData = JSON.parse(localStorage.getItem('mackay'));
        console.log($state);
        let getPhotoChatroom;
        if (!this.hasMore || this.selectedChatroom == 'noSelected') {
            $state.complete();
            return;
        }
        if (this.selectedChatroom){
          getPhotoChatroom = this.selectedChatroom;
        }else if (getJWTData.selectedRoomPath){
          getPhotoChatroom = getJWTData.selectedRoomPath;
        }else{
          getPhotoChatroom = getJWTData.room_path;
        }
        axios.get(`${this.SERVER_PATH}/api/chat/photo`, {
            params: {
                user_id: this.userProfile.id,
                chatRoom: getPhotoChatroom,
                page: this.page,
                size: this.size
            }
        })
        .then(response => {
            if (this.localCurrentAlbum === 0) {
                const newPhotos = response.data.results.map(photo => ({
                    id: photo.record_id,
                    src: photo.media_url,
                    is_carer_user: photo.is_carer_user
                }));
                console.log(response.data.results);
                if (newPhotos.length > 0) {
                    if (this.page === 1) {
                      this.albums = [{ photos: newPhotos }];
                    } else {
                      this.albums[0].photos.push(...Object.values(newPhotos).filter(photo => !photo.is_carer_user));
                    }
                    this.page += 1; // 增加頁數
                    if ($state) $state.loaded();
                } else {
                    this.hasMore = false; // 如果沒有新數據，設置 hasMore 為 false
                    if ($state) $state.complete();
                }
            }
        })
        .catch(error => {
            console.error('Error fetching photos:', error);
            this.hasMore = false; // 在發生錯誤時停止加載
            if ($state) $state.complete();
        });
    },
    // loadMorePhotos($state) {
    //   console.log(this.hasMore);
      
    //   if (!this.hasMore || this.selectedPatientId === -1 || this.localCurrentAlbum === 1) {
    //     $state.complete(); // 如果沒有更多數據或條件不符，停止加載
    //     return;
    //   }
    //   this.fetchPhotos();
    //   $state.complete(); 
    //   $state.loaded();
    // },
    // 開啟圖片彈窗
    openImagePopup(imageUrl) {
      if (event.target.classList.contains('v-btn')) return;
      this.selectedImage = imageUrl;
      this.imagePopupVisible = true;
      this.popImgKey += 1;
    },
    // 關閉圖片彈窗
    closeImagePopup() {
      this.imagePopupVisible = false;
      this.selectedImage = '';
      this.popImgKey += 1;
    },
    updateVisible(val) {
      this.imagePopupVisible = val;
    },
    switchAlbum(index) {
      this.$emit('update:currentAlbum', index);
    },
    confirmDelete(photoId) {
      // let getPhotoUserId;
      // if (this.selectedPatientId){
      //   getPhotoUserId = this.selectedPatientId;
      // }else{
      //   getPhotoUserId = this.$store.state.storeUserId;
      // }
      let getPhotoUserId = this.userProfile.id;
      if (confirm('Are you sure you want to delete this photo？')) {
        axios.delete(`${this.SERVER_PATH}/api/chat/photo`, {
          data: {
            user_id: getPhotoUserId,
            record_id: photoId
          }
        })
        .then(() => {
          const album = this.albums[this.currentAlbum];
          album.photos = album.photos.filter((photo) => photo.id !== photoId);
          // alert('The photo has been deleted.');
        })
        .catch(error => {
          console.error('Error deleting photo:', error);
          // alert('Deletion failed. Please try again.');
        });
      }
    },
    updateCurrentAlbum(index) {
      this.localCurrentAlbum = index;
      this.$emit('update:currentAlbum', index);
    },
    reloadAlbums() {
      // alert('reloadAlbums');
        this.page = 1;
        this.hasMore = true;
        this.albums = [];
        if (this.$refs.infiniteLoading) {
            this.$refs.infiniteLoading.$emit('$InfiniteLoading:reset');
        }
        this.loadMorePhotos();
    }
  },
  mounted() {
    // 監聽根實例上的 'upload-success' 事件，當事件觸發時調用 reloadAlbums 方法
    this.$root.$on('upload-success', this.reloadAlbums);
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
  width: 30px;
  height: 30px;
}
.delete-btn .v-icon{
  width: 20px;
  height: 20px;
  font-size: 20px;
}
.photo-zone {
  padding: 10px;
  height: calc(100vh - 120px);
  overflow-y: auto;
}
.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  padding: 10px 0;
  /* max-height: calc(100vh - 120px);
  overflow-y: auto; */
  position: relative;
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
  object-fit: contain;
  border-radius: 8px;
  background-color: #e2e2e2;
}
.photo-item:hover img{
  opacity: 0.6;
  /* box-shadow: unset; */
 }
.infini-photo-note {
  position: absolute;
  bottom: -20px;
  left: 0; 
  right: 0;
  margin: auto;
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