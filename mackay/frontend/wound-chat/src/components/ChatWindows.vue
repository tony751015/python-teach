<template>
  <v-container class="chat-container">
    <v-dialog v-model="detectError" width="200">
      <v-alert dense type="error">發生錯誤</v-alert>
    </v-dialog>

    <div class="px-3">
      <div ref="chatWindow" class="chat-window">
        <div class="date-divider">2024-10-01</div>
        <infinite-loading direction="top" @infinite="infiniteHandler">
          <div slot="no-more">沒有更多留言了</div>
          <div slot="no-results">沒有更多留言了</div>
        </infinite-loading>
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
        hint="Shift + Enter 換行 Enter 發送訊息"
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
const GET_API_URL = 'http://127.0.0.1:8000/api/chat/list?';
export default {
  name: 'ChatWindows',
  components: {
    ChatMessage
  },
  data() {
    return {
      page: 1,
      newMessage: '',
      imagePopupVisible: false,
      selectedImage: '',
      messages: [],
      detectError: false,
      user_name: '',  // 儲存使用者名稱
    };
  },
  created() {
    this.fetchMessages();
  },
  mounted() {
    // 頁面初次加載時滾動到底部
    // this.$nextTick(() => {
    //   const chatWindow = this.$refs.chatWindow;
    //   if (chatWindow) {
    //     chatWindow.scrollTop = chatWindow.scrollHeight;
    //   }
    // });
  },
  watch: {
    // messages() {
    //   // 當 messages 更新時，滾動到底部
    //   this.$nextTick(() => {
    //     const chatWindow = this.$refs.chatWindow;
    //     if (chatWindow) {
    //       chatWindow.scrollTop = chatWindow.scrollHeight;
    //     }
    //   });
    // }
  },
  methods: {
    // 獲取訊息列表
    fetchMessages() {
      // axios.get('http://127.0.0.1:8000/api/chat/list?user_id=1&page=' + this.page + '&size=15')
      axios.get(GET_API_URL,{
        params: {
          user_id: '1',
          page: this.page,
          size: 15
        }
      })
        .then((res) => {
          if (!res.data.count) {
            this.detectError = true;
          } else {
            this.page += 1;
            this.messages = res.data.results.slice().reverse();
            this.user_name = res.data.results[0].user_name;
            localStorage.setItem('user_name', this.user_name);
             // 頁面初次加載時滾動到底部
            this.$nextTick(() => {
              const chatWindow = this.$refs.chatWindow;
              if (chatWindow) {
                chatWindow.scrollTop = chatWindow.scrollHeight;
              }
            });
          }
        })
        .catch((err) => {
          this.detectError = true;
          console.error(err);
        });
    },
    infiniteHandler($state) {
      axios.get(GET_API_URL, {
        params: {
          user_id: '1',
          page: this.page,
          size: 15
        },
      }).then(( res ) => {
        // console.log(JSON.stringify(res.data.results));
        // console.log(res.data.count);
        if (!res.data.results.length) {
          $state.complete();
        } else {
          this.page += 1;
          this.messages.unshift(...res.data.results.slice().reverse());
          $state.loaded();
        }
        // if (res.data.count) {
        //   this.page += 1;
        //   this.messages.unshift(res.data.results.slice().reverse());
        //   $state.loaded();
        // } else {
        //   $state.complete();
        // }
      });
    },
    // 發送訊息並用 axios 將資料 POST 到資料庫
    sendMessage() {
      if (this.newMessage.trim() !== '') {
        const user_name = localStorage.getItem('user_name') || '您';
        const messageData = {
          is_carer_user: false,
          user_name: user_name,
          content: this.newMessage,
          content_type: 'text'
        };

        // 發送到前端 UI
        this.messages.push(messageData);
        this.newMessage = '';
        // 發送滾動到底部
        this.$nextTick(() => {
            const chatWindow = this.$refs.chatWindow;
            if (chatWindow) {
              chatWindow.scrollTop = chatWindow.scrollHeight;
            }
          });

        // 發送 POST 請求到後端
        axios.post('http://127.0.0.1:8000/api/chat/control', {
          user_id: '1',
          is_carer_user: false,  // 自己發送的訊息
          content: messageData.content,
          content_type: 'text'
        })
        .then((response) => {
          console.log('Message sent successfully:', response.data);
        })
        .catch((err) => {
          console.error('Error sending message:', err);
        });
      }
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
};
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
  position: relative;
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