<template>
  <v-app>
    <!-- Topbar 區域 -->
    <v-app-bar color="main-green" elevation="0" dense>
      <!-- <v-responsive class="d-sm-none">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
      </v-responsive> -->
      
      <img src="../assets/logo_dr.png" class="main-logo" alt="logo">
      <!-- <v-btn
        v-if="userProfile.super_user"
        text
        class="list-btn"
        disabled
      >
        <span class="patients-text">My Patients</span>
      </v-btn> -->
      <v-spacer>
        <template>
          <v-tabs align-with-title background-color="transparent">
          </v-tabs>
        </template>
      </v-spacer>
      <!-- 新增照片區域切換按鈕 -->
      <!-- <v-btn
        icon
        class="white--text d-md-none"
        @click="togglePhotoSection"
      >
        <v-icon>{{ isPhotoSectionOpen ? 'mdi-close' : 'mdi-image' }}</v-icon>
      </v-btn> -->
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn 
            class="dropdown-btn" 
            v-bind="attrs" 
            v-on="on" 
            rounded 
            color="normal"
            :small='getRwdType === "mobile" ? true : false'
          >
            <v-avatar :size="getRwdType !== 'mobile' ? 30 : 20">
              <v-img :src="thumb_avatar"></v-img>
            </v-avatar>
            <span class="ml-2 d-none d-sm-block">{{ username }}</span>
            <v-icon right>mdi-chevron-down</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <!-- 手機版顯示用戶名稱 -->
          <v-list-item class="d-sm-none">
            <v-list-item-title class="user-name">{{ username }}</v-list-item-title>
          </v-list-item>
          <!-- 手機版顯示分隔線 -->
          <v-divider class="d-sm-none"></v-divider>
          <!-- 登出按鈕 -->
          <v-list-item @click="logout">
            <v-list-item-title class="logoutBtn">log out</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    
    <!-- 主要內容區塊 -->
    <v-container fluid class="fill-height">
      <v-row>
        <!-- 左側：用戶列表 -->
        <v-col :cols="12" :md="8" class="chat-list-section">
          <v-toolbar flat dense class="w-100">
            <!-- 搜尋區域 -->
            <v-text-field
              v-model="searchQuery"
              prepend-inner-icon="mdi-magnify"
              label="Search for a patient"
              dense
              outlined
              color="main-green"
              placeholder="Search for a patient"
              hide-details
            ></v-text-field>
          </v-toolbar>
          <v-list>
            <v-subheader>Total: {{ patientCount }}</v-subheader>
              <template v-if="!preloading">
                <v-list-item
                  v-for="patient in visiblePatients"
                  :key="patient.id"
                  class="patient-item"
                  @click="selectPatient(patient); togglePhotoSection()"
                  :class="{ 'outlined': highlightedPatientId === patient.user_id }"
                >
                  <v-list-item-avatar :size="getRwdType === 'mobile' ? 30 : 45">
                    <v-img :src="patient.user_avatar || require('@/assets/user.png')"></v-img>
                  </v-list-item-avatar>
              
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">
                      {{ patient.user_name }}
                      <span class="grey--text text--lighten-1 font-small">{{ '(' + patient.user_id + ')'}}</span>
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      <span
                        v-if="
                          patient.last_message &&
                          patient.last_message.content_type === 'text'
                        "
                      >
                        {{ patient.last_message.content }}
                      </span>
                      <span
                        v-else-if="
                          patient.last_message &&
                          patient.last_message.content_type === 'image'
                        "
                      >
                        send a photo
                        <!-- <v-btn
                          outlined
                          color="main-green"
                          small
                          :class="['preview-btn', {'photo-preview-btn': $vuetify.breakpoint.smAndDown}]"
                          @click.stop="openImagePopup(
                            `${IMG_PATH}media/${patient.last_message.media_url}`
                          )"
                        > -->
                          <!-- 手機版：上圖下字 -->
                          <!-- <div v-if="$vuetify.breakpoint.smAndDown" class="d-flex flex-column align-center">
                            <v-icon size="16" class="mb-1">mdi-image-search-outline</v-icon>
                            <span class="preview-text">photo</span>
                          </div> -->
                          
                          <!-- 電腦版：原始樣式 -->
                          <!-- <template v-else>
                            <v-icon class="font-normal">mdi-magnify</v-icon>
                            <span class="ml-1">photo</span>
                          </template>
                        </v-btn> -->
                      </span>
                      <span v-else>no message</span>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn 
                      outlined
                      elevation="0"
                      color="main-green"
                      small
                      :class="['chat-btn', {'mobile-chat-btn': $vuetify.breakpoint.smAndDown}]"
                      @click.stop="goChatroom(patient)"
                    >
                      <!-- 手機版：上圖下字 -->
                      <div v-if="$vuetify.breakpoint.smAndDown" class="d-flex flex-column align-center">
                        <v-icon size="16" class="mb-1">mdi-chat-processing-outline</v-icon>
                        <!-- <span class="chat-text">Chat</span> -->
                      </div>
                      
                      <!-- 電腦版：原始樣式 -->
                      <template v-else>
                        Open Chat
                      </template>
                    </v-btn>
                  </v-list-item-action>
                  <v-list-item-action>
                    <v-btn
                      small
                      fab 
                      elevation="0"
                      :color="patient.pin ? 'main-green' : ''"
                      @click.stop="togglePin(patient)"
                    >
                      <v-icon :color="patient.pin ? 'white' : ''">mdi-pin</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              
                <infinite-loading 
                  :identifier="infiniteId"
                  @infinite="loadMorePatients"
                  spinner="bubbles"
                  direction="bottom"
                >
                  <div slot="no-more" class="infini-note grey--text text--lighten-1 font-small">No more data</div>
                  <div slot="no-results" class="infini-note grey--text text--lighten-1 font-small">No results found</div>
                </infinite-loading>
              </template>
            
          </v-list>
        </v-col>

        <!-- 右側：照片列表區域 -->
        <wound-photos
          class="photo-section"
          :class="{
            'photo-section--mobile': $vuetify.breakpoint.smAndDown,
            'photo-section--open': isPhotoSectionOpen && $vuetify.breakpoint.smAndDown
          }"
          :albums="albums"
          :current-album.sync="currentAlbum"
          :selected-patient-id="selectedPatientId"
          :selected-chatroom="selectedChatroom"
          @update:current-album="updateCurrentAlbum"
        ></wound-photos>
      </v-row>

      <!-- 新增的 close 懸浮按鈕 -->
      <v-btn
        v-if="$vuetify.breakpoint.smAndDown && isPhotoSectionOpen"
        fab
        color="main-green"
        class="floating-close-btn"
        @click="togglePhotoSection"
        elevation="2"
      >
        <v-icon color="white">mdi-close</v-icon>
      </v-btn>
    </v-container>

    <!-- 圖片彈出組件 -->
    <ImagePopup
      :key="`imgpop-${popImgKey}`" 
      :visible="imageDialog" 
      :image="imageSrc" 
      @close="closeImagePopup">
    </ImagePopup>
  </v-app>
</template>
  
<script>
  import axios from 'axios';
  import ImagePopup from '../components/ImagePopup.vue';
  import WoundPhotos from '../components/WoundPhotos.vue';
  import { mapMutations } from 'vuex';
// import { reject, resolve } from 'core-js/fn/promise';
  
  export default {
    components: {
      ImagePopup,
      WoundPhotos
    },

    created() {
      this.initPatientsList();
    },

    data() {
      return {
        preloading: true,
        username: '使用者',
        thumb_avatar: '',
        searchQuery: '',
        imageDialog: false,
        imageSrc: '',
        popImgKey: 1,
        patients: [],
        patientCount: 0,
        currentPage: 1,
        pageSize: 1, // 每頁資料數量
        infiniteId: +new Date(), // 確保重置 infinite-loading
        pinnedPatients: [], // 存儲已經 pin 的病患 ID
        selectedPatientId: -1, // 初始化為 -1
        selectedChatroom: 'noSelected', // 初始化為 noSelected
        highlightedPatientId: null, // 用於追蹤當前選擇的病患
        albums: [], // 初始化 albums 為空陣列
        currentAlbum: 0, // 初始化 currentAlbum
        dontRun: false,
        isPhotoSectionOpen: false
      };
    },
    computed: {
      filteredPatients() {
        // 根據使用者輸入的搜尋字串過濾病患列表
        // 如果病患的名字或 ID 包含搜尋字串，則保留該病患
        return this.patients.filter(patient => 
            patient.user_name.includes(this.searchQuery) || 
            patient.user_id.toString().includes(this.searchQuery)
        );
      },
      visiblePatients() {
        return this.filteredPatients.filter(patient => !patient.ban);
      }
    },
    methods: {
      openImagePopup(imageUrl) {
        console.log('openImagePopup', imageUrl);
        this.imageSrc = imageUrl;
        this.imageDialog = true;
        this.popImgKey += 1;
      },
      closeImagePopup() {
        this.imageDialog = false;
        this.imageSrc = '';
        this.popImgKey += 1;
      },
      initPatientsList() {
        axios.put(`${this.SERVER_PATH}api/chat/room`, {
          user_id: this.userProfile.id,
          page: this.currentPage,
          size: this.pageSize
        })
        .then(response => {
          console.log(response.data.results);
          if (response.data.results.length) {
            this.patients.push(...response.data.results);
            this.currentPage += 1;
            this.preloading = false;
            this.updatePatientCount(); // 更新 patientCount
          } else {
            this.preloading = true;
          }
        })
        .catch(error => {
          console.error("Error loading more patients:", error);
          this.updateAlert({
            show: true,
            status: 'error',
            message: 'Opps! Something Wrong'
          });
          this.preloading = false;
        });
      },
      loadMorePatients($state) {
        if (!this.preloading) {
          console.log("Loading more patients...");
          axios.put(`${this.SERVER_PATH}api/chat/room`, {
            user_id: this.userProfile.id,
            page: this.currentPage,
            size: this.pageSize
          })
          .then(response => {
            console.log(response.data.results);
            if (response.data.results.length) {
              this.patients.push(...response.data.results);
              this.currentPage += 1;
              $state.loaded();
              this.updatePatientCount(); // 更新 patientCount
              // console.log("patients.", JSON.stringify(this.patients));
            } else {
              $state.complete();
              if (!this.dontRun) {
                this.updateBanForSuperusers(); // 確保資料完整下載完後再執行
                this.dontRun = true;
              }
            }
          })
          .catch(error => {
            console.error("Error loading more patients:", error);
            this.updateAlert({
              show: true,
              status: 'error',
              message: 'Opps! Something Wrong'
            });
            $state.complete();
          });
        }
      },

      togglePin(patient) {
        const newPinState = !patient.pin;
        patient.pin = newPinState;
        axios.put(`${this.SERVER_PATH}api/chat/update_pin`, {
          user_id: this.userProfile.id,
          pin: newPinState,
          room_path: patient.room_path
        })
        .then(() => {
          // if (newPinState) {
          //   this.updateAlert({
          //     show: true,
          //     status: 'success',
          //     message: 'Item pinned!'
          //   });
          // } else {
          //   this.updateAlert({
          //     show: true,
          //     status: 'success',
          //     message: 'Item unpinned!'
          //   });
          // }
          this.startReloadPatientData();
        })
        .catch(error => {
          console.error("Error updating pin state:", error);
        });
      },

      async startReloadPatientData() {
        await this.reloadPatients();
        await this.initPatientsList();
      },

      reloadPatients() {
        // this.infiniteId += 1; // 重置 infinite-loading
        return new Promise((resolve) => {
          this.currentPage = 1;
          this.patients = [];
          this.preloading = true;
          resolve();
        })
      },

      selectPatient(patient) {
        console.log('selectPatient', patient);
        this.selectedPatientId = patient.user_id;
        this.highlightedPatientId = patient.user_id;
        this.selectedChatroom = patient.room_path;
        // 確保 selectedPatientId 的變化能夠被 WoundPhotos.vue 監聽到
      },
      // reloadPatients() {
      //   // this.infiniteId += 1; // 重置 infinite-loading
      //   this.currentPage = 1;
      //   this.patients = [];
      //   this.preloading = true;
      //   this.initPatientsList();

      //   const process = new Promise((resolve, reject) => {
      //     this.currentPage = 1;
      //     this.patients = [];
      //     this.preloading = true;

      //     return resolve(this.preloading);
      //   });

      //   process.then((value) => {
      //     if (value) {
      //       this.initPatientsList();
      //     }
      //   });
      // }
      updateCurrentAlbum(newAlbumIndex) {
        this.currentAlbum = newAlbumIndex;
      },
      goChatroom(patient) {
        console.log('goChatroom', patient);
        this.UPDATE_USER_ID(patient.user_id);
        this.UPDATE_CHAT_ROOM(patient.room_path);

        // 取得 localStorage 中的 mackay
        const mackayData = JSON.parse(localStorage.getItem('mackay') || '{}');
        
        // 更新 user_id
        mackayData.room_path = patient.room_path;
        mackayData.selectedId = patient.user_id;
        
        // 將更新後的物件存回 localStorage
        localStorage.setItem('mackay', JSON.stringify(mackayData));

        this.$router.push({ path: `/chat/${patient.room_path}` });
      },
      updatePatientCount() {
        this.patientCount = this.visiblePatients.length;
      },
      updateBanForSuperusers() {
        const roomPathsToBan = this.patients
          .filter(patient => patient.is_superuser)
          .map(patient => patient.room_path);

        if (roomPathsToBan.length > 0) {
          axios.put(`${this.SERVER_PATH}api/chat/update_ban`, {
            user_id: this.userProfile.id,
            ban: true,
            room_paths: roomPathsToBan
          })
          .then(() => {
            this.startReloadPatientData();
          })
          .catch(error => {
            console.error("Error updating ban state:", error);
          });
        }
      },
      ...mapMutations(['UPDATE_USER_ID', 'UPDATE_CHAT_ROOM']),
      togglePhotoSection() {
        this.isPhotoSectionOpen = !this.isPhotoSectionOpen;
      }
    },
    mounted() {
      // const userId = this.userProfile.id;
      // axios.put('http://127.0.0.1:8000api/chat/room', {
      //   user_id: userId,
      //   page: "1",
      //   size: "5"
      // })
      // .then(response => {
      //   this.patients = response.data.results;
      //   this.patientCount = response.data.count;
      // })
      // .catch(error => {
      //   console.error('Error fetching data:', error);
      // });
  
      if (this.userProfile.name) {
        this.username = this.userProfile.name;
      }
      if (this.userProfile.thumb) {
        this.thumb_avatar = this.userProfile.thumb;
      }
    }
  };
  </script>
  
  <style scoped>
  .v-app-bar .dropdown-btn{
    padding: 0 10px;
  }
  .fill-height {
    height: calc(100vh - 48px);
    padding: unset;
  }
  .container.fill-height > .row{
    height: 100%;
  }
  .chat-list-section {
    border-right: 1px solid #ccc;
    height: 100%;
    overflow-y: auto;
  }
  .photo-section {
    transition: transform 0.3s ease;
    flex: 0 0 33.33333%;
    max-width: 33.33333%;
    height: 100%;
    overflow-y: auto;
  }
  .photo-section--mobile {
    position: fixed;
    top: 40px;
    right: 0;
    bottom: 0;
    z-index: 1000;
    background: white;
    transform: translateX(100%);
    height: calc(100vh - 48px);
    width: 100%;
    flex: 0 0 100%;
    max-width: 100%;
  }
  .photo-section--open {
    transform: translateX(0);
  }
  @media (max-width: 960px) {
    .chat-list-section {
      flex: 0 0 100%;
      max-width: 100%;
    }
    
    .photo-section {
      flex: 0 0 100%;
      max-width: 100%;
    }
  }
  .v-toolbar__content {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }
  .main-logo {
    height: 90%;
    padding: 6px 0;
  }
  .list-btn.theme--light.v-btn.v-btn--disabled {
    background-color: #fff;
    color: #2D9CA0 !important;
    min-width: auto !important;
    padding: 0 8px !important;
    margin-left: 4px !important;
  }
  .patients-text {
    font-size: 14px;
  }
  @media (max-width: 600px) {
    .patients-text {
      font-size: 13px;
    }
    .list-btn.theme--light.v-btn.v-btn--disabled {
      padding: 0 4px !important;
    }
    .v-app-bar .dropdown-btn {
      height: 28px !important;
    }
    .main-logo {
      padding: 8px 0;
    }
  }
  .patient-item{
    margin-bottom: 2px;
  }
  .patient-item:hover {
    background-color: #d4eaed;
    border-radius: 5px;
  }
  .logoutBtn {
    cursor: pointer;
    text-align: center;
  }
  .image-popup {
    background-color: rgba(0, 0, 0, 0.8); 
    width: calc(9/12 * 100vw); 
    height: 100vh;
    position: relative;
  }
  
  .popup-img {
    width: 100%;
    height: auto;
  }
  
  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    color: white;
    z-index: 101;
  }
  .v-btn:before {
  opacity: 0 !important;
}

.v-ripple__container {
  opacity: 0 !important;
}
.infini-note {
  margin-top: 15px;          
}   
.outlined {
  outline: 2px solid #2D9CA0;
  border-radius: 5px;
}

/* 調整 z-index 確保彈出選單在照片區域上方 */
.v-menu__content {
  z-index: 1001 !important;
}

.floating-close-btn {
  position: fixed;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  width: 60px;
  height: 60px;
}

.floating-photo-btn {
  position: fixed;
  bottom: 80px; /* 位於底部導航欄上方 */
  right: 16px;
  z-index: 1000;
  width: 45px;
  height: 45px;
}

.floating-photo-btn.active {
  background-color: #e53935 !important; /* 關閉按鈕時的顏色 */
}

/* 確保懸浮按鈕的陰影效果 */
.floating-photo-btn.v-btn--fab {
  box-shadow: 0 3px 5px -1px rgba(0,0,0,.2),
              0 6px 10px 0 rgba(0,0,0,.14),
              0 1px 18px 0 rgba(0,0,0,.12);
}

/* 調整照片區域在手機版的高度，避免被按鈕遮擋 */
@media (max-width: 960px) {
  .photo-section--mobile {
    padding-bottom: 80px; /* 為懸浮按鈕留出空間 */
  }
}

.preview-btn {
  padding: 0 8px;
}

/* 手機版樣式 */
.photo-preview-btn {
  min-width: 45px !important;
  height: auto !important;
  padding: 4px 0 !important;
}

.preview-text {
  font-size: 9px;
  line-height: 1;
  text-transform: none;
}

@media (max-width: 600px) {
  .photo-preview-btn {
    min-width: 40px !important;
  }
}

.chat-btn {
  padding: 0 8px;
}

/* 手機版樣式 */
.mobile-chat-btn {
  min-width: 45px !important;
  height: auto !important;
  padding: 4px 0 !important;
}

.chat-text {
  font-size: 9px;
  line-height: 1;
  text-transform: none;
}

@media (max-width: 600px) {
  .mobile-chat-btn {
    min-width: 40px !important;
  }
}

.user-name {
  color: rgba(0, 0, 0, 0.87);
  font-size: 14px;
  padding: 8px 16px;
}

/* 調整 app-bar 高度 */
.v-app-bar.v-app-bar--dense {
  height: 40px !important;
  max-height: 40px !important;
}

.v-app-bar.v-app-bar--dense .v-toolbar__content {
  height: 40px !important;
  max-height: 40px !important;
}
  </style>