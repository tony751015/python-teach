<template>
  <v-app>
    <!-- Topbar 區域 -->
    <v-app-bar color="main-green" elevation="0" dense>
      <v-responsive class="d-sm-none">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
      </v-responsive>
      
        <!-- <v-img src="../assets/logo_dr.png" class="main-logo"></v-img> -->
        <img src="../assets/logo_dr.png" class="main-logo" alt="logo">
      <!-- <header class="chat-title text-h6 font-weight-black">星禾互聯</header> -->
      <v-btn
        v-if="userProfile.super_user"
        text
        class="ml-6"
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

    <!-- 主內容區塊 -->
    <v-container fluid class="fill-height">
      <v-row>
        <!-- 左側：聊天室區域 -->
        <v-col cols="8" class="chat-section">
          <v-toolbar flat dense class="w-100">
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
              prepend-icon="mdi-magnify"
              label="Search for a chat"
              dense
              outlined
              color="main-green"
              placeholder="Search for a chat"
              hide-details
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
          :albums="albums"
          :current-album.sync="currentAlbum"
          :selected-patient-id="currentAlbum"
          @update:current-album="updateCurrentAlbum"
        ></wound-photos>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import ChatWindows from '../components/ChatWindows.vue';
import WoundPhotos from '../components/WoundPhotos.vue';
import { mapMutations } from 'vuex';

export default {
  components: {
    ChatWindows,
    WoundPhotos
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
      ...mapMutations(['UPDATE_USER_ID'])
  },
  mounted() {
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
  width: 10px;
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
</style>
