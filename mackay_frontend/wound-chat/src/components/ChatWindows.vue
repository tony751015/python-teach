<template>
  <v-container class="chat-container">
    <v-dialog v-model="detectError" width="200">
      <v-alert dense type="error"> Error </v-alert>
    </v-dialog>

    <div class="px-3">
      <ProgressLoader :key='activeKey' :showText="`LOADING...`" :active="activeProgress"></ProgressLoader>
      
      <div ref="chatWindow" class="chat-window">
        <infinite-loading direction="top" @infinite="infiniteHandler" :identifier='infiniteId'>
          <div slot="no-more">No more comments</div>
          <div slot="no-results">No more comments</div>
        </infinite-loading>

        <chat-message
          v-for="(msg, index) in messages"
          :key="index"
          :is_carer_user="msg.is_carer_user"
          :content_type="msg.content_type"
          :user_name="msg.user_name"
          :content="msg.content"
          :media_url="msg.media_url"
          :isFirstDate="msg.isFirstDate"
          @image-click="openImagePopup(`${SERVER_PATH}media/${msg.media_url}`)" 
          @image-click2="openImagePopup(msg.media_url)"
        ></chat-message>
        <!-- image-click2解決測試時路徑用 -->
      </div>
    </div>
    <div>
      <v-layout row class="send-message-layout">
        <v-text-field
          v-model="newMessage"
          placeholder="Type your message here"
          outlined
          hint="Shift + Enter for a new line, Enter to send: "
          persistent-hint
          @keyup.enter="sendMessage"
          class="message-input mb-13 mx-3"
        >
        </v-text-field>
        <button @click="sendMessage" elevation="0" color="white" class="send-btn px-1 mr-1" >
            <v-icon color="main-green">mdi-send</v-icon>
        </button>
        <v-btn @click="openUploadImage" elevation="0" color="primary" class="upload-btn main-green">
          <v-icon>mdi-paperclip</v-icon>
          Upload
        </v-btn>
      </v-layout>
      
    </div>

    <!-- 圖片彈窗 -->
    <!-- <v-dialog v-model="imagePopupVisible" max-width="none" persistent>
      <v-card class="image-popup">
        <v-btn icon @click="closeImagePopup" class="close-btn">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-img :src="selectedImage" class="popup-img"></v-img>
      </v-card>
    </v-dialog> -->
    <ImagePopup
      :key="`imgpop-${popImgKey}`"
      :image="selectedImage"
      :visible="imagePopupVisible"
      @close="closeImagePopup">
    </ImagePopup>

    <UploadImage 
      :key="`imgupload-${uploadImgKey}`"
      :activeUpload="uploadImage"
      @close="closeUploadImage"
      @update:visible="updateVisible"
      @message-uploaded="handleMessageUploaded">
    </UploadImage>

  </v-container>
</template>

<script>
import axios from 'axios';
import ChatMessage from './ChatMessage.vue';
import ProgressLoader from '../common/progessLoading.vue';
import ImagePopup from './ImagePopup.vue';
import UploadImage from './UploadImage.vue';
export default {
  name: 'ChatWindows',
  components: {
    ImagePopup,
    ChatMessage,
    ProgressLoader,
    UploadImage
  },
  data() {
    return {
      newMessage: '',
      selectedImage: '',
      messages: [],
      
      user_name: '',  // 儲存使用者名稱
      user_id: null,
      
      preloader: true,
      imagePopupVisible: false,
      activeProgress: false,
      detectError: false,
      uploadImage: false,
      
      page: 1,
      popImgKey: 1,
      uploadImgKey: 1,
      activeKey: 1,
      infiniteId: 1,
    };
  },
  created() {
    this.activeProgress = true;
    // setTimeout(() => {
    this.$route.params.id ? this.fetchMessages() : this.routerRedirectTo404();
    // }, 500);
    // if (this.$route.query.code && this.$route.query.state) {

    //   axios.post('http://127.0.0.1:8000/api/member/line_login', {
    //       code: this.$route.query.code,
    //       state: this.$route.query.state,  // 自己發送的訊息
    //     })
    //     .then((res) => {
    //       localStorage.setItem('mackay', JSON.stringify(res.data.jwt_token));
    //       console.log('LINE LOGIN Success:');
    //     })
    //     .catch((err) => {
    //       console.error('LINE LOGIN Failed:', err);
    //     });
    // }
  },
  // mounted() {
    // 頁面初次加載時滾動到底部
    // this.$nextTick(() => {
    //   const chatWindow = this.$refs.chatWindow;
    //   if (chatWindow) {
    //     chatWindow.scrollTop = chatWindow.scrollHeight;
    //   }
    // });
  // },
  // watch: {
    // messages() {
    //   // 當 messages 更新時，滾動到底部
    //   this.$nextTick(() => {
    //     const chatWindow = this.$refs.chatWindow;
    //     if (chatWindow) {
    //       chatWindow.scrollTop = chatWindow.scrollHeight;
    //     }
    //   });
    // }
  // },
  methods: {
    // 獲取訊息列表
    fetchMessages() {
      let userId
      let fetch_user_id
      const getJWTData = JSON.parse(localStorage.getItem('mackay'));
      if (this.userProfile.super_user){
         fetch_user_id = this.storeUserId
      }else {
         fetch_user_id = this.userProfile.id
      }
      if (fetch_user_id) {
        userId = fetch_user_id
      }else {
        userId = getJWTData.selectedId
      }
      console.log('fetchMessages', this.userProfile.id, this.storeUserId);
      // if (this.userProfile.id !== this.$route.params.id) {
      //   alert('Wrong User');
      //   this.routerRedirectTo404();
      //   return;
      // }
      const chatRoomId = this.$route.params.id.split('-')[0];
      
      if (!this.userProfile.super_user) {
            if (userId != chatRoomId) {
              // alert('Wrong User');
              this.routerRedirectTo404();
              return;
            
          }
        }else {
          const getJWTData = JSON.parse(localStorage.getItem('mackay'));
          const selectedIdForCheck = getJWTData.selectedId;
          if (selectedIdForCheck != chatRoomId) {
            // alert('Wrong User');
            this.$router.push('/chat')
            return;
          }
        }

      console.log('fetchMessages 1', userId)
      // axios.get('http://127.0.0.1:8000/api/chat/list?user_id=1&page=' + this.page + '&size=15')
      axios.get(`${this.SERVER_PATH}/api/chat/list?`,{
        params: {
          user_id: userId,
          page: this.page,
          size: 3
        }
      })
        .then((res) => {
          if (!res.data.count) {
            this.user_name = '';
          } else {
            this.user_name = res.data.results[0].user_name;
            // localStorage.setItem('user_name', this.user_name);
          }

          console.log(JSON.stringify(res.data));
          this.preloader = false;
          // console.log('fetchMessages 2', this.page);
          this.messages = res.data.results.slice().reverse();
          // this.user_name = res.data.results[0].user_name;
          // localStorage.setItem('user_name', this.user_name);
          this.page += 1;
          this.infiniteId += 1;

          if (!res.data.count) {
            this.user_name = '';
          } else {
            this.user_name = res.data.results[0].user_name;
            // localStorage.setItem('user_name', this.user_name);
          }

          // 頁面初次加載時滾動到底部
          setTimeout(() => {
            this.$nextTick(() => {
              this.activeProgress = false;
              this.activeKey += 1;
              const chatWindow = this.$refs.chatWindow;
              if (chatWindow) {
                chatWindow.scrollTop = chatWindow.scrollHeight;
              }
            });
          },1000)
          
        })
        .catch((err) => {
          this.detectError = true;
          // setTimeout(() => {
          //   this.$router.push({ name: 'chat-list' });
          // }, 500);
          console.error(err.response.status);
          if (err.response.status === 404) {
            this.routerRedirectTo404();
          } else if (err.response.status === 403) {
            this.routerRedirectTo404();
          }else{
            if (this.userProfile.super_user){
              this.$router.push({ name: 'chat-list' });
            }else {
              this.routerRedirectTo404();
            }
          }
          // if (err.response.status === 404) {
          //   xxx
          // } else if (err.response.status === 403) {
          //   xxx
          // }
        });
    },

    infiniteHandler($state) {
      let userId
      let fetch_user_id
      const getJWTData = JSON.parse(localStorage.getItem('mackay'));
      if (this.userProfile.super_user){
         fetch_user_id = this.storeUserId
      }else {
         fetch_user_id = this.userProfile.id
      }
      if (fetch_user_id) {
        userId = fetch_user_id
      }else {
        userId = getJWTData.selectedId
      }
      if (!this.preloader) {
        axios.get(`${this.SERVER_PATH}/api/chat/list?`, {
          params: {
            user_id: userId,
            page: this.page,
            size: 3
          },
        }).then(( res ) => {
          // console.log(JSON.stringify(res.data.results));
          // console.log(res.data.count);
          if (!res.data.results.length) {
            $state.complete();
          } else {
            console.log('infiniteHandler', this.page);
            this.messages.unshift(...res.data.results.slice().reverse());

            this.page += 1;
            $state.loaded();
          }
          // if (res.data.count) {
          //   this.page += 1;
          //   this.messages.unshift(res.data.results.slice());
          //   $state.loaded();
          // } else {
          //   $state.complete();
          // }
        });
      }
      
    },
    // 發送訊息並用 axios 將資料 POST 到資料庫
    sendMessage() {
      let userId
      let fetch_user_id
      const getJWTData = JSON.parse(localStorage.getItem('mackay'));
      if (this.userProfile.super_user){
         fetch_user_id = this.storeUserId
      }else {
         fetch_user_id = this.userProfile.id
      }
      if (fetch_user_id) {
        userId = fetch_user_id
      }else {
        userId = getJWTData.selectedId
      }
      if (this.newMessage.trim() !== '') {
        const user_name = this.userProfile.name || '您';
        const isCarerUser = this.userProfile.super_user === true;

        const messageData = {
          is_carer_user: isCarerUser,
          user_name: user_name,
          media_url: '',
          content: this.newMessage,
          content_type: 'text',
          isFirstDate: ''
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
        axios.post(`${this.SERVER_PATH}/api/chat/control`, {
          user_id: userId,
          is_carer_user: isCarerUser,  // 根據 super_user 設置
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
      this.popImgKey += 1
      console.log('openImagePopup', this.imagePopupVisible)
    },
    // 關閉圖片彈窗
    closeImagePopup(value) {
      this.imagePopupVisible = value;
      this.selectedImage = '';
      this.popImgKey += 1
    },
    updateVisible(val) {
      this.imagePopupVisible = val
    },
    openUploadImage() {
      this.uploadImage = true;
      this.uploadImgKey += 1
    },
    closeUploadImage() {
      this.uploadImage = false;
    },
    handleMessageUploaded(messageData) {
      console.log('Message uploaded:', messageData);
      // 在這裡更新 this.messages 陣列
      this.messages.push(messageData);
    },
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

.send-message-layout{
  padding-top: 2px;
  padding-right: 12px;
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
.layout {
  align-items: baseline;
}
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  color: white;
  z-index: 101;
}
.v-btn.send-btn:hover{
  background-color: #fff !important;
}
.v-dialog__content {
  z-index: 100;
}
.infinite-loading-container{
  font-size: 12px;
  color: #ccc;
  margin-top: 15px;
  margin-bottom: 15px;
}
.v-btn.upload-btn{
  height: 55px;
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