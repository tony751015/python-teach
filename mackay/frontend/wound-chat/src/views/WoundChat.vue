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
      <v-title class="chat-title">星禾互聯</v-title>
      <v-spacer>
        <template>
          <v-tabs align-with-title background-color="transparent">
            <v-tab>One</v-tab>
            <v-tab>Two</v-tab>
            <v-tab>Three</v-tab>
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
        <v-col cols="9" class="chat-section">
          <v-toolbar flat dense>
            <v-avatar size="30">
              <v-img src="https://cdn.vuetifyjs.com/images/john.jpg"></v-img>
            </v-avatar>
            <v-toolbar-title>照護專員</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="searchChat"
              append-icon="mdi-magnify"
              label="搜尋對話"
              solo
              dense
              hide-details
            ></v-text-field>
          </v-toolbar>
          <chat-windows class="chatWindows"></chat-windows>
        </v-col>

        <!-- 右側：商品區域 -->
        <v-col cols="3" class="product-section">
          <v-toolbar flat dense>
            <v-toolbar-title>商品列表</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="searchProduct"
              append-icon="mdi-magnify"
              label="搜尋商品"
              solo
              dense
              hide-details
              clearable
            ></v-text-field>
          </v-toolbar>
          <v-list>
            <v-list-item v-for="(product, index) in products" :key="index">
              <v-list-item-avatar>
                <v-img :src="product.image"></v-img>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>{{ product.name }}</v-list-item-title>
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
      searchChat: '',
      searchProduct: '',
      products: [
        { name: '商品名', description: '介紹內容123321', image: 'https://cdn.vuetifyjs.com/images/cards/house.jpg' },
        { name: '商品名', description: '介紹內容123321', image: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg' },
        { name: '商品名', description: '介紹內容123321', image: 'https://cdn.vuetifyjs.com/images/cards/fashion.jpg' }
      ]
    };
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

.chat-section {
  border-right: 1px solid #ccc;
  height: 100%;
  overflow: hidden;
}


.product-section {
  padding-left: 20px;
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
</style>
