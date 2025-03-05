<template>
  <v-dialog
    :value="visible"
    @input="$emit('update:visible', $event)"
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
  >
    <v-card class="message-layout">
      <!-- 頂部工具欄 -->
      <v-toolbar dark color="main-green">
        <v-btn icon dark @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>New Message</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>

      <!-- 訊息輸入區域容器 -->
      <div class="input-container">
        <v-card-text class="message-input-area">
          <v-textarea
            v-model="newMessage"
            outlined
            auto-grow
            rows="4"
            row-height="30"
            placeholder="Type your message here"
            hide-details
            class="message-textarea"
          ></v-textarea>

          <!-- 按鈕區域 -->
          <div class="action-buttons">
            <!-- 附件按鈕 -->
            <v-btn
              color="main-green"
              text
              class="action-btn"
              @click="openUploadImage"
            >
              <div class="d-flex flex-column align-center">
                <v-icon class="mb-1">mdi-paperclip</v-icon>
                <span class="caption">Upload</span>
              </div>
            </v-btn>

            <!-- 發送按鈕 -->
            <v-btn
              color="main-green"
              text
              class="action-btn"
              @click="sendMessage"
              :disabled="!newMessage.trim()"
            >
              <div class="d-flex flex-column align-center">
                <v-icon class="mb-1">mdi-send</v-icon>
                <span class="caption">Send</span>
              </div>
            </v-btn>
          </div>
        </v-card-text>
      </div>
    </v-card>

    <!-- 圖片上傳組件 -->
    <UploadImage 
      :key="`imgupload-${uploadImgKey}`"
      :activeUpload="uploadImage"
      @close="closeUploadImage"
      @update:visible="updateVisible"
      @message-uploaded="handleMessageUploaded"
    ></UploadImage>
  </v-dialog>
</template>

<script>
import UploadImage from './UploadImage.vue';

export default {
  name: 'MsgLayout',
  
  components: {
    UploadImage
  },

  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      newMessage: '',
      uploadImage: false,
      uploadImgKey: 1
    };
  },

  methods: {
    close() {
      this.$emit('update:visible', false);
      this.newMessage = '';
    },

    sendMessage() {
      if (this.newMessage.trim()) {
        this.$emit('send-message', this.newMessage);
        this.newMessage = '';
        this.close();
      }
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

    handleMessageUploaded(messageData) {
      this.$emit('message-uploaded', messageData);
      this.close();
    }
  },

  watch: {
    visible(val) {
      if (!val) {
        this.newMessage = '';
      }
    }
  }
};
</script>

<style scoped>
.message-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.input-container {
  flex: 1;
  display: flex;
  align-items: center;
  padding-bottom: 76px; /* 為底部功能按鈕區留出空間 */
}

.message-input-area {
  width: 100%;
  max-width: 600px; /* 限制最大寬度 */
  margin: 0 auto;
  padding: 16px;
}

.message-textarea {
  margin-bottom: 15px;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 8px;
}

.action-btn {
  min-width: 64px;
  height: auto;
  padding: 8px 0;
}

.action-btn .v-icon {
  font-size: 24px;
}

.action-btn .caption {
  font-size: 12px;
  line-height: 1;
  margin-top: 4px;
}

.action-btn.v-btn--disabled {
  opacity: 0.6;
}

/* 對話框底部過渡動畫 */
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
  transition: transform .3s ease-in-out;
}

.dialog-bottom-transition-enter,
.dialog-bottom-transition-leave-to {
  transform: translateY(100%);
}
</style>
