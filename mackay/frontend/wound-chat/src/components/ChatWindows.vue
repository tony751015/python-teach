<template>
  <v-container class="chat-container">
    <v-dialog v-model="detectError" width="200">
      <v-alert dense type="error">發生錯誤</v-alert>
    </v-dialog>


    <div class="px-3">
      <div class="chat-window">
        <div class="date-divider">2024-10-01</div>
        <chat-message
          v-for="(msg, index) in messages"
          :key="index"
          :is_carer_user="msg.is_carer_user"
          :content_type="msg.content_type"
          :user_name="msg.user_name"
          :content="msg.content"
          @image-click="openImagePopup(msg.content)" 
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
import axios from 'axios';
import ChatMessage from './ChatMessage.vue';

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
      messages: [],
      detectError: false,
      user_name: '',  // 儲存使用者名稱
    }
  },
  created() {
    this.fetchMessages();
    // this.getuser_name();
  },
  methods: {
    // 獲取訊息列表
    fetchMessages() {
      console.log('Test fetchMessages')
      
      axios.get('http://127.0.0.1:8000/api/chat/list?user_id=1&page=1&size=10')
      .then((res) => {
        if (!res.data.count) {
          this.detectError = true;
          console.log('not found', this.detectError);
        } else {
          this.messages = res.data.results;
          this.user_name = res.data.results[0].user_name;
          localStorage.setItem('user_name', this.user_name);
        }
      })
      .catch((err) => {
        this.detectError = true;
        console.error(err);
      });
      // axios({
      //   method: 'get',
      //   baseURL: 'http://127.0.0.1:8000',
      //   url: '/api/chat/list',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   data:{
      //     "user_id": "1",
      //     "page": 1,
      //     "size": 10
      //   }
      // })
      // .then((result) => {
      //   this.messages = result.data;
      //   this.user_name = result.data.user_name;
      //   localStorage.setItem('user_name', this.user_name);
      // })
      // .catch((err) => {
      //   console.error(err);
      // });
    },
    // 獲取使用者名稱並存儲到 localStorage
    
    // 發送訊息並用 axios 將資料 POST 到資料庫
    // sendMessage() {
    //   if (this.newMessage.trim() !== '') {
    //     const user_name = localStorage.getItem('user_name') || '您';
    //     const messageData = {
    //       is_carer_user: false,
    //       user_name: user_name,
    //       content: this.newMessage,
    //       content_type: 'text'
    //     };
        
    //     // 發送到前端 UI
    //     this.messages.push(messageData);
    //     this.newMessage = '';

    //     // 發送 POST 請求到後端
    //     axios({
    //       method: 'post',
    //       baseURL: 'http://127.0.0.1:8000/',
    //       url: '/api/chat/list',
    //       headers: {
    //         'Content-Type': 'application/json',
    //       },
    //       data: {
    //         user_id: '1',
    //         is_carer_user: false,  // 自己發送的訊息
    //         content: messageData.content,
    //         content_type: 'text'
    //       }
    //     })
    //     .then((response) => {
    //       console.log('Message sent successfully:', response.data);
    //     })
    //     .catch((err) => {
    //       console.error('Error sending message:', err);
    //     });
    //   }
    // },
    sendMessage() {
      const messageData = {
        user_id: '1',
        content: this.newMessage,
        content_type: 'text',
        is_carer_user: false
      };

      axios.post('/api/chat_record_control/', messageData)
        .then(response => {
          console.log('Message sent', response.data);
        })
        .catch(error => {
          console.error('Error sending message', error.response);
        });
    },

    // 開啟圖片彈窗
    openImagePopup(imageUrl) {
      this.selectedImage = imageUrl;
      this.imagePopupVisible = true;
    },
    // 關閉圖片彈窗
    closeImagePopup() {
      this.imagePopupVisible = false;
      this.selectedImage = '';
    }
  }
}
</script>

<style scoped>
.chat-container {
  height: calc(100vh - 64px);
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
  border-top: 1px solid #eee;
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
  z-index: 1001;
}

.v-dialog__content {
  z-index: 1000;
}
</style>
