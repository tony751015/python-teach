<template>
  <v-app>
    <!-- Topbar 區域 -->
    <v-app-bar color="main-green" elevation="0" dense>
      <!-- <v-responsive class="d-sm-none">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
      </v-responsive> -->
      
        <!-- <v-img src="../assets/logo_dr.png" class="main-logo"></v-img> -->
        <img src="../assets/logo_dr.png" class="main-logo" alt="logo">
      <!-- <header class="chat-title text-h6 font-weight-black">星禾互聯</header> -->
      <v-btn
        v-if="userProfile.super_user"
        text
        class="ml-6 white--text d-md-block  d-none"
        @click="goChatList()"
      >
        My Patients
      </v-btn>
      <v-spacer>
        <template>
          <v-tabs align-with-title background-color="transparent">
            
            <!-- <v-tab v-for="items, index in topBarNavList" class="white--text font-weight-bold" active-class="white v-dark2--text font-weight-bold" :key="index">
              {{ items }}
            </v-tab> -->
            <!-- <v-tab class="white--text font-weight-bold" active-class="white v-dark2--text font-weight-bold">One</v-tab>
            <v-tab class="white--text font-weight-bold" active-class="white v-dark2--text font-weight-bold">Two</v-tab>
            <v-tab class="white--text font-weight-bold" active-class="white v-dark2--text font-weight-bold">Three</v-tab> -->

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
            @click="handleDropdownClick"
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

    <!-- 主內容區塊 -->
    <v-container fluid class="fill-height">
      <v-row>
        <!-- 左側：聊天室區域 -->
        <v-col :cols="12" :md="8" class="chat-section">
          <v-toolbar flat dense class="w-100 searchChatToolBar">
            <!-- <div class="d-flex align-center">
              <v-avatar size="30">
                <v-img src="https://cdn.vuetifyjs.com/images/john.jpg"></v-img>
              </v-avatar>
              <v-toolbar-title class="pl-2 text-subtitle-1 font-weight-medium">照護專員</v-toolbar-title>
            </div> -->

            <!-- <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer> -->

            <v-text-field
              v-model="searchChat"
              prepend-inner-icon="mdi-magnify"
              label="Search for a chat"
              dense
              outlined
              color="main-green"
              placeholder="Search for a chat"
              hide-details
              class="searchChatBar"
              @keyup.enter="performSearch"
              @input="onInput"
            ></v-text-field>
            
            <!-- 搜尋結果列表 -->
            <v-list v-if="searchResults.length > 0 || noResults" class="search-results-list">
              <template v-if="searchResults.length > 0">
                <v-list-item
                  v-for="(result, index) in searchResults"
                  :key="index"
                  @click="scrollToMessage(result.index)"
                >
                  <v-list-item-content>
                    <v-list-item-title>{{ result.content }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </template>

              <!-- 沒有搜尋結果時顯示 -->
              <template v-else>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>No records found</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </template>
            </v-list>
          </v-toolbar>
          <chat-windows class="chatWindows" ref="chatWindows"></chat-windows>

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
          :selected-patient-id="currentAlbum"
          :selectedChatroom="selectedChatroom"
          @update:current-album="updateCurrentAlbum"
        ></wound-photos>
      </v-row>

      <!-- 修改手機版功能按鈕區 -->
      <div 
        class="mobile-actions d-md-none"
        :class="{'mobile-actions--hidden': isMessageLayoutOpen}"
      >
        <div class="mobile-actions-container">
          
          <!-- 照片區域切換按鈕 -->
          <v-btn
            text
            class="mobile-action-btn"
            :class="{'active': isPhotoSectionOpen}"
            @click="togglePhotoSection"
          >
            <div class="d-flex flex-column align-center">
              <v-icon class="action-icon">{{ isPhotoSectionOpen ? 'mdi-arrow-left' : 'mdi-image' }}</v-icon>
              <span class="action-text">{{ isPhotoSectionOpen ? 'Back' : 'Photos' }}</span>
            </div>
          </v-btn>

          <!-- 新增的上傳圖片按鈕 -->
          <v-btn
            text
            class="mobile-action-btn"
            @click="openUploadImage"
          >
            <div class="d-flex flex-column align-center">
              <v-icon class="action-icon">mdi-paperclip</v-icon>
              <span class="action-text">Upload</span>
            </div>
          </v-btn>

          <!-- 訊息輸入按鈕 -->
          <v-btn
            text
            class="mobile-action-btn"
            @click="openMessageLayout"
          >
            <div class="d-flex flex-column align-center">
              <v-icon class="action-icon">mdi-message-text</v-icon>
              <span class="action-text">Message</span>
            </div>
          </v-btn>

          <!-- My Patients 按鈕 -->
          <v-btn
            v-if="userProfile.super_user"
            text
            class="mobile-action-btn"
            @click="goChatList"
          >
            <div class="d-flex flex-column align-center">
              <v-icon class="action-icon">mdi-account-multiple</v-icon>
              <span class="action-text">Patients</span>
            </div>
          </v-btn>
        </div>
      </div>
    </v-container>

    <!-- 添加 MsgLayout 組件 -->
    <msg-layout
      :visible.sync="isMessageLayoutOpen"
      @send-message="handleSendMessage"
      @message-uploaded="handleMessageUploaded"
    ></msg-layout>

    <!-- 添加 UploadImage 組件 -->
    <UploadImage 
      :key="`imgupload-${uploadImgKey}`"
      :activeUpload="uploadImage"
      @close="closeUploadImage"
      @update:visible="updateVisible"
      @message-uploaded="handleMessageUploaded"
    ></UploadImage>
  </v-app>
</template>

<script>
import ChatWindows from '../components/ChatWindows.vue';
import WoundPhotos from '../components/WoundPhotos.vue';
import MsgLayout from '../components/MsgLayout.vue';
import UploadImage from '../components/UploadImage.vue';
import { mapMutations } from 'vuex';

export default {
  components: {
    ChatWindows,
    WoundPhotos,
    MsgLayout,
    UploadImage
  },
  data() {
    return {
      username: '使用者',
      thumb_avatar: '',
      searchChat: '', // 搜尋框中的文字
      searchResults: [], // 儲存搜尋結果
      noResults: false, // 用於顯示沒有搜尋結果的訊息
      topBarNavList: ['One', 'Two', 'Three'],
      chatRecord: [],
      albums: [],
      currentAlbum: 0,
      selectedChatroom: '',
      isPhotoSectionOpen: false,
      isMessageLayoutOpen: false,
      uploadImage: false, // 新增的狀態
      uploadImgKey: 1, // 新增的狀態
    };
  },
  computed: {
    currentPhotos() {
      return this.albums[this.currentAlbum]?.photos || [];
    },
  },
  methods: {
    updateCurrentAlbum(newAlbumIndex) {
      this.currentAlbum = newAlbumIndex;
    },
   
    // 當輸入改變時，更新搜尋結果
    onInput() {
      this.performSearch();
    },
    // 執行搜尋
    performSearch() {
      const searchText = this.searchChat.trim().toLowerCase();
      if (searchText) {
        const results = this.$refs.chatWindows.messages
          .map((msg, index) => ({ content: msg.content, index }))
          .filter((msg) => msg.content.toLowerCase().includes(searchText));

        if (results.length > 0) {
          this.searchResults = results;
          this.noResults = false;
        } else {
          this.searchResults = [];
          this.noResults = true; // 當沒有搜尋結果時，設置為 true
        }
      } else {
        this.searchResults = [];
        this.noResults = false; // 清除搜尋結果時，隱藏提示
      }
    },

    // 滾動到指定訊息
    scrollToMessage(index) {
      const chatWindow = this.$refs.chatWindows.$refs.chatWindow; // 獲取 .chat-window 容器
      const chatMessageElements = chatWindow.children; // 獲取所有訊息元素

      if (chatMessageElements[index]) {
        // 計算目標訊息相對於 chatWindow 的 offsetTop
        const targetMessageTop = chatMessageElements[index].offsetTop;

        // 使用 scrollTop 進行平滑滾動
        chatWindow.scrollTo({
          top: targetMessageTop,
          behavior: 'smooth'
        });
      }

      this.searchResults = []; // 清空搜尋結果
    },
    goChatList() {
        this.UPDATE_USER_ID(this.userProfile.id);

        // 取得 localStorage 中的 mackay
        const mackayData = JSON.parse(localStorage.getItem('mackay') || '{}');
        
        // 更新 user_id
        mackayData.user_id = this.userProfile.id;
        
        // 將更新後的物件存回 localStorage
        localStorage.setItem('mackay', JSON.stringify(mackayData));

        this.$router.push({ path: `/chat/` });
      },
      togglePhotoSection() {
        this.isPhotoSectionOpen = !this.isPhotoSectionOpen;
      },
      openMessageLayout() {
        if (this.isPhotoSectionOpen) {
          this.isPhotoSectionOpen = false;
        }
        this.isMessageLayoutOpen = true;
      },
      openUploadImage() {
        this.uploadImage = true;
        this.uploadImgKey += 1;
      },
      closeUploadImage() {
        this.uploadImage = false;
      },
      updateVisible(val) {
        this.uploadImage = val;
      },
      handleSendMessage(message) {
        this.$refs.chatWindows.newMessage = message;
        this.$refs.chatWindows.sendMessage();
      },
      handleMessageUploaded(messageData) {
        this.$refs.chatWindows.handleMessageUploaded(messageData);
      },
      handleDropdownClick() {
        if (this.isPhotoSectionOpen) {
          this.isPhotoSectionOpen = false;
        }
      },
      ...mapMutations(['UPDATE_USER_ID'])
  },
  mounted() {
    if (this.userProfile.name) {
      this.username = this.userProfile.name;
    }
    if (this.userProfile.thumb) {
      this.thumb_avatar = this.userProfile.thumb;
    }
  },
};
</script>

<style scoped lang="scss">
$topbarHeight: '38px';

.v-app-bar .dropdown-btn {
  padding: 0 10px;
}
.v-menu__content{
  z-index: 109 !important;
}
.v-toolbar__content {
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.main-logo{
  height: 100%;
  padding: 10px 0px;
}
.fill-height {
  height: calc(100vh - 48px);
  padding: unset;
}
.container.fill-height > .row{
  height: 100%;
}

.chat-section {
  border-right: 1px solid #ccc;
  height: 100%;
  overflow: hidden;
  position: relative;
  z-index: 100;
}
.chat-section header {
  z-index: 104;
}


.product-section {
  padding: 0;
  height: 100%;
}

.chat-title {
  padding-left: 10px;
  color: black;
}

.dropdown-btn {
  display: flex;
  align-items: center;
}
.search-results-list {
  max-height: 200px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #e0e0e0;
  position: absolute;
  top: 47px;;
  z-index: 1003;
  width: 97%;
  border-radius: 4px;
  box-shadow: 0 0 0 5px #555;
}
.logoutBtn{
  cursor: pointer;
  text-align: center;
}


/* width */
::-webkit-scrollbar {
  width: 5px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1; 
}
 
/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}


.photo-section {
  transition: transform 0.3s ease;
  flex: 0 0 33.33333%;
  max-width: 33.33333%;
}

.photo-section--mobile {
  position: fixed;
  top: #{$topbarHeight};
  right: 0;
  bottom: 0;
  z-index: 200;
  background: white;
  transform: translateX(100%);
  height: calc(100vh - #{$topbarHeight});
  width: 100%;
  flex: 0 0 100%;
  max-width: 100%;
}

.photo-section--open {
  transform: translateX(0);
}

@media (max-width: 730px) {
  .fill-height {
    height: calc(100vh - #{$topbarHeight});
    padding: unset;
  }
  .chat-section {
    flex: 0 0 100%;
    max-width: 100%;
    padding-bottom: 60px; /* 為底部按鈕區留出空間 */
  }
  
  .photo-section {
    flex: 0 0 100%;
    max-width: 100%;
  }
  
  .photo-section--mobile {
    height: calc(100vh - 105px); /* #{$topbarHeight} (topbar) + 60px (bottom actions) */
  }

  // .v-app-bar {
  //   height: #{$topbarHeight} !important;
  //   .v-toolbar__content, .v-toolbar__extension {
  //     height: #{$topbarHeight} !important;
  //   }
  //   .main-logo {
  //     width: 100px;
  //     height: 21px;
  //     padding: 0 !important;
  //   }
  // }
}

/* 確保 row 有正確的 flex 佈局 */
.container.fill-height > .row {
  height: 100%;
  display: flex;
  flex-wrap: wrap;
}
.searchChatToolBar:deep  .v-toolbar__content{
  padding: 4px 8px !important;
}
.mobile-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  z-index: 1000;
  transition: transform 0.3s ease; /* 添加過渡效果 */
}

.mobile-actions--hidden {
  transform: translateY(100%); /* 向下移動隱藏 */
}

.mobile-actions-container {
  display: flex;
  justify-content: space-around;
  padding: 12px 0 19px;
  max-width: 600px;
  margin: 0 auto;
  position: relative;
}

.mobile-action-btn {
  flex: 1;
  height: auto;
  min-width: auto;
  padding: 8px 0;
  border-radius: 0;
}

.action-icon {
  font-size: 20px;
  margin-bottom: 4px;
  color: #757575; /* 未選中的顏色 */
  transition: color 0.3s ease;
}

.action-text {
  font-size: 10px;
  line-height: 1;
  color: #757575; /* 未選中的顏色 */
  transition: color 0.3s ease;
}

/* 選中和懸停狀態使用 #2d9ca0 顏色 */
.mobile-action-btn.active .action-icon,
.mobile-action-btn.active .action-text,
.mobile-action-btn:hover .action-icon,
.mobile-action-btn:hover .action-text {
  color: #2d9ca0 !important;
}

/* 為底部導航添加微妙的陰影 */
.mobile-actions {
  box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.05);
}

/* 確保 MsgLayout 的 z-index 高於其他元素 */
.v-dialog {
  z-index: 1100 !important;
}

.user-name {
  color: rgba(0, 0, 0, 0.87);
  font-size: 14px;
  padding: 8px 16px;
}
</style>
