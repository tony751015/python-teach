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
      <v-container class="chat-list-container">
        <!-- 搜尋區域 -->
        <v-text-field
          v-model="searchQuery"
          prepend-icon="mdi-magnify"
          label="Search for a chat"
          dense
          outlined
          color="main-green"
          placeholder="Search for a chat"
          hide-details
        ></v-text-field>
        
        <!-- 用戶列表 -->
        <v-list>
          <v-subheader>病患總數 {{ patientCount }}</v-subheader>
          
          <!-- <v-list-item
            v-for="patient in filteredPatients"
            :key="patient.id"
            class="patient-item"
          >
            <v-list-item-avatar size="56">
              <v-img :src="patient.user_avatar || 'default-avatar.jpg'"></v-img>
            </v-list-item-avatar>
            
            <v-list-item-content>
              <v-list-item-title>{{ patient.user_name }}</v-list-item-title>
              <v-list-item-subtitle>
                <span v-if="patient.last_message && patient.last_message.content_type === 'text'">
                  {{ patient.last_message.content }}
                </span>
                <span v-else-if="patient.last_message && patient.last_message.content_type === 'image'">
                  傳送了一張圖片
                  <v-btn icon @click="openImagePopup(`${SERVER_PATH}media/${patient.last_message.media_url}`)">
                    <v-icon>mdi-image</v-icon>
                  </v-btn>
                </span>
                <span v-else>
                  無訊息
                </span>
              </v-list-item-subtitle>
            </v-list-item-content>
            
            <v-list-item-action>
              <v-btn icon>
                <v-icon>mdi-pin</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item> -->
          <v-list-item
            v-for="patient in filteredPatients"
            :key="patient.id"
            class="patient-item"
          >
            <v-list-item-avatar size="56">
              <v-img :src="patient.user_avatar || require('@/assets/user.png')"></v-img>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{ patient.user_name }}</v-list-item-title>
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
                    icon
                    @click="openImagePopup(
                      `${SERVER_PATH}media/${patient.last_message.media_url}`
                    )"
                  >
                    <v-icon>mdi-image</v-icon>
                  </v-btn>
                </span>
                <span v-else>無訊息</span>
              </v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-action>
              <v-btn 
                fab 
                elevation="0"
                :color="patient.pin ? 'main-green' : ''"
                @click="togglePin(patient)"
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
            <span slot="no-more">No more data</span>
            <span slot="no-results">No results found</span>
          </infinite-loading>
        </v-list>
        <!-- 圖片彈出組件 -->
      <ImagePopup
       :key="`imgpop-${popImgKey}`" 
       :visible="imageDialog" 
       :image="imageSrc" 
       @close="closeImagePopup">
      </ImagePopup>
      </v-container>
  
      
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import ImagePopup from '../components/ImagePopup.vue';
  
  export default {
    components: {
      ImagePopup
    },
    data() {
      return {
        username: '使用者',
        thumb_avatar: '',
        searchQuery: '',
        imageDialog: false,
        imageSrc: '',
        popImgKey: 1,
        patients: [],
        patientCount: 0,
        currentPage: 1,
        pageSize: 2, // 每頁資料數量
        infiniteId: +new Date(), // 確保重置 infinite-loading
        pinnedPatients: [], // 存儲已經 pin 的病患 ID
      };
    },
    computed: {
      filteredPatients() {
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
      loadMorePatients($state) {
        console.log("Loading more patients...");
        axios.put('http://127.0.0.1:8000/api/chat/room', {
          user_id: this.storeUserId,
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
          $state.complete();
        });
      },
      togglePin(patient) {
        const newPinState = !patient.pin;
        patient.pin = newPinState;
        axios.put('http://127.0.0.1:8000/api/chat/update_pin', {
          user_id: this.storeUserId,
          pin: newPinState,
          room_path: patient.room_path
        })
        .then(() => {
          if (newPinState) {
            this.updateAlert({
              show: true,
              status: 'success',
              message: 'Item pinned!'
            });
          } else {
            this.updateAlert({
              show: true,
              status: 'success',
              message: 'Item unpinned!'
            });
          }
          this.reloadPatients();
        })
        .catch(error => {
          console.error("Error updating pin state:", error);
        });
      },
      reloadPatients() {
        this.currentPage = 1;
        this.patients = [];
        this.infiniteId += 1; // 重置 infinite-loading
        this.$nextTick(() => {
          setTimeout(() => {
            this.loadMorePatients({
              loaded: () => {},
              complete: () => {}
            });
          }, 300);
        });
      }
    },
    mounted() {
      // const userId = this.storeUserId;
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
  .chat-list-container {
    height: calc(100vh - 48px);
    overflow: auto;
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
  </style>