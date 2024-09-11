<template>
  <v-container class="chat-container">
    <div class="px-3">
      <div class="chat-window">
        <div class="date-divider">2024-10-01</div>
        <chat-message
          v-for="(msg, index) in messages"
          :key="index"
          :isOwnMessage="msg.isOwnMessage"
          :name="msg.name"
          :message="msg.message"
          @image-click="openImagePopup(msg.message)" 
        ></chat-message>
      </div>
    </div>
    <div>
      <v-text-field
        v-model="newMessage"
        placeholder="請輸入留言"
        outlined
        hint="This field uses counter prop"
        persistent-hint
        append-icon="mdi-emoticon-outline"
        @keyup.enter="sendMessage"
        class="message-input mb-13 mx-4"
      ></v-text-field>
    </div>

    <!-- 圖片彈窗 -->
    <v-dialog v-model="imagePopupVisible" max-width="none" persistent>
      <v-card class="image-popup">
        <v-btn icon @click="closeImagePopup" class="close-btn">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-img :src="selectedImage" class="popup-img"></v-img>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import ChatMessage from './ChatMessage.vue'

export default {
  name: 'ChatWindows',
  components: {
    ChatMessage
  },
  data() {
    return {
      newMessage: '',
      imagePopupVisible: false,
      selectedImage: '',
      messages: [
        { isOwnMessage: false, name: '照護專員', message: '您好，您的傷口照護已告一段落 我們會幫您做結案的動作 若日後您有任何傷口的問題都歡迎您來可以訪問' },
        { isOwnMessage: true, name: '您', message: '我有些問題' },
        { isOwnMessage: true, name: '您', message: '客氣了，如果能有助益' },
        { isOwnMessage: true, name: '您', message: '<img src="https://via.placeholder.com/150" alt="image"><br>最近的傷口照' },
        { isOwnMessage: false, name: '照護專員', message: '照片看起來復原得不錯 但是還是要記得再幫我上傳傷口照片 提醒您臉部傷口可以使用除疤產品喔' }
      ]
    }
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== '') {
        this.messages.push({
          isOwnMessage: true,
          name: '您',
          message: this.newMessage
        });
        this.newMessage = '';
      }
    },
    openImagePopup(imageHtml) {
      const imgTag = imageHtml.match(/<img src="([^"]+)"/);
      if (imgTag) {
        this.selectedImage = imgTag[1];
        this.imagePopupVisible = true;
      }
    },
    closeImagePopup() {
      this.imagePopupVisible = false;
      this.selectedImage = '';
    }
  }
}
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 64px); /* Adjust based on your app bar height */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0;
}

.chat-window {
  flex: 1;
  background-color: #fff;
  padding: 0;
  height: calc(100vh - 205px);
  overflow-y: auto;
}

.date-divider {
  text-align: center;
  margin: 20px 0;
  color: #aaa;
}

.message-input {
  /* margin-top: 10px; */
  border-top: 1px solid #eee;
}

/* 彈窗樣式 */
.image-popup {
  background-color: rgba(0, 0, 0, 0.8); /* 半透明黑色背景 */
  width: calc(9/12 * 100vw); /* 占滿左側聊天室區域 */
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
  z-index: 1001; /* 確保關閉按鈕位於最上層 */
}

.v-dialog__content {
  z-index: 1000; /* 確保彈窗位於聊天室上方 */
}
</style>
