<template>
  <v-app>
    <!-- Topbar 區域 -->
    <v-app-bar color="green lighten-1" elevation="1" dense>
      <v-responsive class="d-sm-none">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
      </v-responsive>
      <v-avatar left size="40">
        <v-img src="https://cdn.vuetifyjs.com/images/john.jpg"></v-img>
      </v-avatar>
      <header class="chat-title text-h6 font-weight-black">星禾互聯</header>
      <v-spacer>
        <template>
          <v-tabs align-with-title background-color="transparent">
            
            <v-tab v-for="items, index in topBarNavList" class="white--text font-weight-bold" active-class="white v-dark2--text font-weight-bold" :key="index">
              {{ items }}
            </v-tab>
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
              <v-img src="https://cdn.vuetifyjs.com/images/john.jpg"></v-img>
            </v-avatar>
            <span class="ml-2">Helena</span>
            <v-icon right>mdi-chevron-down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>Logout</v-list-item-title>
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
            <div class="d-flex align-center">
              <v-avatar size="30">
                <v-img src="https://cdn.vuetifyjs.com/images/john.jpg"></v-img>
              </v-avatar>
              <v-toolbar-title class="pl-2 text-subtitle-1 font-weight-medium">照護專員</v-toolbar-title>
            </div>

            <!-- <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer> -->

            <v-text-field
              v-model="searchChat"
              append-icon="mdi-magnify"
              label="搜尋對話"
              dense
              outlined
              placeholder="搜尋對話"
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
                    <v-list-item-title>沒有搜尋結果</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </template>
            </v-list>
          </v-toolbar>
          <chat-windows class="chatWindows" ref="chatWindows"></chat-windows>
        </v-col>

        <!-- 右側：商品區域 -->
        <v-col cols="4" class="product-section pt-3">
          <v-toolbar flat dense>
            <!-- <v-toolbar-title>商品列表</v-toolbar-title> -->
            <v-text-field
              v-model="searchProduct"
              append-icon="mdi-magnify"
              label="搜尋商品"
              dense
              hide-details
              outlined
              clearable
            ></v-text-field>
          </v-toolbar>
          <v-list>
            <v-list-item v-for="(product, index) in products" :key="index" class="pt-1">
              <v-list-item-avatar>
                <v-img :src="product.image"></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="font-weight-bold secondary--text">{{ product.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ product.description }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import ChatWindows from '../components/ChatWindows.vue';

export default {
  components: {
    ChatWindows
  },
  data() {
    return {
      searchChat: '', // 搜尋框中的文字
      searchResults: [], // 儲存搜尋結果
      noResults: false, // 用於顯示沒有搜尋結果的訊息
      searchProduct: '',
      topBarNavList: ['One', 'Two', 'Three'],
      chatRecord: [],
      products: [
        { name: '商品名', description: '介紹內容123321', image: 'https://cdn.vuetifyjs.com/images/cards/house.jpg' },
        { name: '商品名', description: '介紹內容123321', image: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg' },
        { name: '商品名', description: '介紹內容123321', image: 'https://cdn.vuetifyjs.com/images/cards/fashion.jpg' }
      ]
    };
  },
  methods: {
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
  top: 44px;;
  z-index: 1003;
  width: 100%;
}
</style>
