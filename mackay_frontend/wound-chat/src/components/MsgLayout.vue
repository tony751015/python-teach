<template>
  <v-bottom-sheet
    v-model="localVisible"
    inset
  >
    <v-sheet class="message-layout">
      <!-- 頂部工具欄 -->
      <v-toolbar dense color="main-green" dark>
        <v-btn icon dark @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>New Message</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>

      <!-- 訊息輸入區域 -->
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
        <div class="action-buttons-grid">
          <!-- 左側：附件按鈕 -->
          <div class="grid-item">
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
          </div>

          <!-- 右側：發送按鈕 -->
          <div class="grid-item text-right">
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
        </div>
      </v-card-text>
    </v-sheet>

    <!-- 圖片上傳組件 -->
    <UploadImage 
      :key="`imgupload-${uploadImgKey}`"
      :activeUpload="uploadImage"
      @close="closeUploadImage"
      @update:visible="updateVisible"
      @message-uploaded="handleMessageUploaded"
    ></UploadImage>
  </v-bottom-sheet>
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
      uploadImgKey: 1,
      localVisible: false
    };
  },

  watch: {
    visible(val) {
      this.localVisible = val;
      if (!val) {
        this.newMessage = '';
      }
    },
    localVisible(val) {
      this.$emit('update:visible', val);
    }
  },

  methods: {
    close() {
      this.localVisible = false;
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
  }
};
</script>

<style scoped>
.message-layout {
  padding-bottom: 16px;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
}

.message-input-area {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
}

.message-textarea {
  margin-bottom: 15px;
}

.action-buttons-grid {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 兩列等寬 */
  gap: 8px;
  padding: 0 8px;
  max-width: 600px;
  margin: 0 auto;
}

.grid-item {
  display: flex;
  align-items: center;
}

.grid-item:last-child {
  justify-content: flex-end;
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
</style>
