<template>
<div>
  <!-- Topbar 區域 -->
  <v-app-bar color="main-green" elevation="0" dense>
    <v-responsive class="d-sm-none">
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </v-responsive>
    
    <img src="../assets/logo_dr.png" class="main-logo" alt="logo">
    <v-spacer>
      <template>
        <v-tabs align-with-title background-color="transparent">
        </v-tabs>
      </template>
    </v-spacer>
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="dropdown-btn" v-bind="attrs" v-on="on" rounded color="normal">
          <v-avatar size="30">
            <v-img :src="thumb_avatar"></v-img>
          </v-avatar>
          <span class="ml-2">{{ username }}</span>
          <v-icon right>mdi-chevron-down</v-icon>
        </v-btn>
      </template>
      <v-list dense>
        <v-list-item>
          <v-list-item-title class="logoutBtn" @click="logout">log out</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
  
  <!-- 主要內容區塊 -->
  <v-container fluid class="fill-height">
    <v-row>
      <!-- 左側：用戶列表 -->
      <v-col cols="8" class="chat-list-section">
        <!-- 搜尋區域 -->
        <v-text-field
          v-model="searchQuery"
          prepend-icon="mdi-magnify"
          label="Search for a patient"
          dense
          outlined
          color="main-green"
          placeholder="Search for a patient"
          hide-details
        ></v-text-field>
        
        <v-list>
          <v-subheader>Patient census: {{ patientCount }}</v-subheader>
          <template v-if="!preloading">
            <v-list-item
              v-for="patient in filteredPatients"
              :key="patient.id"
              class="patient-item"
              @click="selectPatient(patient.user_id)"
              :class="{ 'outlined': highlightedPatientId === patient.user_id }"
            >
              <v-list-item-avatar size="56">
                <v-img :src="patient.user_avatar || require('@/assets/user.png')"></v-img>
              </v-list-item-avatar>
  
              <v-list-item-content>
                <v-list-item-title>
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
                    傳送了一張圖片
                    <v-btn
                      outlined
                      color="main-green"
                      small
                      class="px-1"
                      @click.stop="openImagePopup(
                        `${SERVER_PATH}static/media/${patient.last_message.media_url}`
                      )"
                    >
                      <v-icon class="font-normal">mdi-magnify</v-icon>
                      photo
                    </v-btn>
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
                  class="px-1"
                  @click.stop="goChatroom(patient)"
                >Open Chat
                  <!-- <v-icon>mdi-arrow-right-bold</v-icon> -->
                </v-btn>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn 
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
          :albums="albums"
          :current-album.sync="currentAlbum"
          :selected-patient-id="selectedPatientId"
          @update:current-album="updateCurrentAlbum"
        ></wound-photos>
      
    </v-row>
  </v-container>

  <!-- 圖片彈出組件 -->
  <ImagePopup
    :key="`imgpop-${popImgKey}`" 
    :visible="imageDialog" 
    :image="imageSrc" 
    @close="closeImagePopup">
  </ImagePopup>
</div>
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
        highlightedPatientId: null, // 用於追蹤當前選擇的病患
        albums: [], // 初始化 albums 為空陣列
        currentAlbum: 0, // 初始化 currentAlbum
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
        axios.put('http://127.0.0.1:8000/api/chat/room', {
          user_id: this.userProfile.id,
          page: this.currentPage,
          size: this.pageSize
        })
        .then(response => {
          console.log(response.data.results);
          if (response.data.results.length) {
            this.patients.push(...response.data.results);
            this.patientCount = response.data.count;
            this.currentPage += 1;
            this.preloading = false;
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
          axios.put('http://127.0.0.1:8000/api/chat/room', {
            user_id: this.userProfile.id,
            page: this.currentPage,
            size: this.pageSize
          })
          .then(response => {
            console.log(response.data.results);
            if (response.data.results.length) {
              this.patients.push(...response.data.results);
              this.patientCount = response.data.count;
              this.currentPage += 1;
              $state.loaded();
            } else {
              $state.complete();
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
        axios.put('http://127.0.0.1:8000/api/chat/update_pin', {
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

      selectPatient(userId) {
        this.selectedPatientId = userId;
        this.highlightedPatientId = userId;
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

        // 取得 localStorage 中的 mackay
        const mackayData = JSON.parse(localStorage.getItem('mackay') || '{}');
        
        // 更新 user_id
        mackayData.room_path = patient.room_path;
        mackayData.selectedId = patient.user_id;
        
        // 將更新後的物件存回 localStorage
        localStorage.setItem('mackay', JSON.stringify(mackayData));

        this.$router.push({ path: `/chat/${patient.room_path}` });
      },
      ...mapMutations(['UPDATE_USER_ID'])
    },
    mounted() {
      // const userId = this.userProfile.id;
      // axios.put('http://127.0.0.1:8000/api/chat/room', {
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
    height: 100%;
    overflow-y: auto;
  }
  .v-toolbar__content {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }
  .main-logo {
    height: 100%;
    padding: 10px 0px;
  }
  .patient-item{
    margin-bottom: 2px;
  }
  .patient-item:hover {
    background-color: #f0f0f0;
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
  </style>