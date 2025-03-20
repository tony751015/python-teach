<template>
    <v-dialog v-model="uploadImage" max-width="500px" scrollable>
      <v-card>
        <v-card-title class="font-large font-weight-bold text-center">
          Upload a photo of the wound
          <span class="font-weight-regular font-small grey--text ml-1">JPG and PNG image files only(Max: 8MB)</span>
        </v-card-title>
        
        <v-card-text>
            <v-container
                class="uploader-area"
                :class="{ 'is-dragging': fileOnDrag }"
                >
                <!-- @click="triggerFileInput" -->
                <!-- @click="triggerFileInput" 點擊作用區 -->
                <!-- 隱藏的 input -->
                
                <!-- 預覽圖顯示區 -->
                <div v-show="filePreviewSrc" class="uploader-preview">
                  <v-btn class="uploader-remove-btn" @click='handleResetInput'>
                    <v-icon color="primary">mdi-trash-can-outline</v-icon>
                  </v-btn>
                  <v-img :src="filePreviewSrc" contain></v-img>
                </div>

                <div v-show="!filePreviewSrc">
                  <input
                    ref="fileInput"
                    type="file"
                    accept="image/jpeg, image/png"
                    class="uploader-input"
                    @dragenter='handleDragEnter'
                    @dragleave='handleDragEnter'
                    @dragdrop='handleDragDrop'
                    @change='handleInputChange'/>
                 
                  <!-- 防呆訊息顯示區 -->
                  <div class="uploader-interface">
                    <v-icon size="40" color="#dcdcdc">mdi-cloud-upload-outline</v-icon>
                    <p :class="{ 'error-message': showErrorMsg }">{{ displayFileTips }}</p>
                    <!-- <p class="text-caption text-grey--text">Only accept JPG and PNG image files，Max: 8MB</p> -->
                  </div>
                </div>
            </v-container>
        </v-card-text>
  
        <v-card-actions class="justify-end">
          <v-btn text color="v-dark" @click="handleClose">Cancel</v-btn>
          <v-btn color="primary" text :disabled="!canUpload" @click="startUpload">
            <v-progress-circular
              v-if="showLoading"
              indeterminate
              color="white"
              size="20"
            ></v-progress-circular>
            <span v-else>Submit upload</span>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  import axios from "axios";

  export default {
    props: {
      activeUpload: Boolean
    },
    data() {
      return {
        uploadImage: this.activeUpload,
        file: null, // 上傳檔案物件
        filePreviewSrc: "", // 圖片預覽 URL
        fileOnDrag: false, // 是否處於拖曳狀態
        fileTips: "Drag and drop or click to upload images", // 初始提示訊息
        showErrorMsg: false, // 是否顯示錯誤訊息
        canUpload: false, // 是否允許上傳
        showLoading: false, // 傳送按鈕的載入狀態
        
      };
    },
    computed: {
      displayFileTips() {
        // 使用 $vuetify.breakpoint.smAndDown 來檢查是否為手機版
        return this.$vuetify.breakpoint.smAndDown ? "Click to upload images" : this.fileTips;
      }
    },
    methods: {
        startUpload() {
          const userId = this.userProfile.id;
          let chatRoom;
          const getJWTData = JSON.parse(localStorage.getItem('mackay'));
          if (this.userProfile.super_user) {
            if (getJWTData.room_path) {
              chatRoom = getJWTData.room_path;
            }else {
              chatRoom = this.storeChatRoom;
            }
            
          } else {
            chatRoom = this.userProfile.room_path;
          }
          const isCarerUser = this.userProfile.super_user === true ? '1' : '0';
          // const chatRoom = this.userProfile.chatRoom;
          const formData = new FormData();
          const ts = new Date().getTime();
          console.log('this.file', this.file);

          formData.append('user_id', userId);
          formData.append('chatRoom', chatRoom); // 根據 super_user 設置
          formData.append('is_carer_user', isCarerUser); // 根據 super_user 設置
          formData.append('photo_upload', this.file, `${userId}_${ts}.${this.file.type.split('/')[1]}`);
          axios.post(`${this.SERVER_PATH}api/chat/upload`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then((response) => {
            // alert('Message sent successfully');
            console.log('Message sent successfully:', response.data);
            this.uploadImage = false;
            const user_name = this.userProfile.name || '您';
            const messageData = {
              is_carer_user: isCarerUser === '1',
              user_name: user_name,
              media_url: this.filePreviewSrc,
              content_type: 'image2',
              content: '',
              isFirstDate: '',
            };
            this.$emit('message-uploaded', messageData);
            this.$root.$emit('upload-success');
            // 發送滾動到底部
            this.$nextTick(() => {
              const chatWindow = this.$parent.$refs.chatWindow;
              if (chatWindow) {
                chatWindow.scrollTop = chatWindow.scrollHeight;
              }
            });
          })
          .catch((err) => {
            console.error('Error sending message:', err);
          });
        },

        triggerFileInput() {
            // 點擊觸發隱藏的文件選擇器
            this.$refs.fileInput.click();
        },
        handleResetInput() {
          console.log('handleResetInput', this.$refs.fileInput)
          this.canUpload = false;
          this.$refs.fileInput.value = '';
          this.filePreviewSrc = '';
          this.fileTips = this.$options.data().fileTips;
        },
        handleInputChange(event) {
            const file = event.target.files[0];
            if (file) {
              this.handleUploadFile(file);
            }
        },
        handleUploadFile(file) {
            this.fileOnDrag = false;
            this.showErrorMsg = false;

            if (file.type === "image/jpeg" || file.type === "image/png") {
              const _URL = window.URL || window.webkitURL;
              const img = new Image();
              img.src = _URL.createObjectURL(file);

              img.onload = () => {
                if (file.size < 8000 * 1024) {
                  this.fileTips = file.name;
                  this.canUpload = true;
                  this.filePreviewSrc = img.src; // 設置圖片預覽
                  this.file = file; // 設置上傳檔案物件
                } else {
                  this.showErrorMsg = true;
                  this.fileTips = "File size must be under 8MB";
                  this.file = null;
                }
              };
            } else {
              this.showErrorMsg = true;
              this.fileTips = "File format is not supported";
            }
        },
        handleDragEnter(event) {
            event.preventDefault();
            this.fileOnDrag = true;
        },
        handleDragLeave() {
            this.fileOnDrag = false;
        },
        handleDragDrop(event) {
            event.preventDefault();
            this.fileOnDrag = false;
            const files = event.dataTransfer.files;
            if (files && files.length > 0) {
            const file = files[0];
            this.handleUploadFile(file);
            }
        },
        handleChange(file) {
            this.handleUploadFile(file);
        },

        handleClose() {
            this.uploadImage = false;
        },
    },
  };
  </script>
  

  <style scoped>
  .uploader-area {
    position: relative;
    border: 2px dashed #dcdcdc;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: border-color 0.2s ease;
    min-height: 200px; /* 增加區域高度 */
  }
/* 
  .headline {
    font-size: 13px;
  } */

  .uploader-input {
    position: absolute;
    top: 0;
    text-indent: -9999px;
    width: 100%;
    height: 100%;
    left: 0;
  }
  
  .uploader-area.is-dragging {
    border-color: #42a5f5;
  }
  
  .uploader-preview {
    display: flex;
    justify-content: center;
    width: 100%;
  }

  .v-btn.uploader-remove-btn {
    position: absolute;
    z-index: 30;
    bottom: 10px;
    right: 10px;
    width: 40px;
    height: 40px;
    min-width: unset;
    border-radius: 50%;
    background-color: #fff;
  }

  .image-preview {
    width: 400px; /* 固定寬度為 400px */
    height: calc(400px * 0.75); /* 高度為寬度的 75% (4:3 比例) */
    object-fit: contain; /* 確保圖片完整呈現 */
    border-radius: 8px; /* 圓角效果（視需要調整） */
    border: 1px solid #dcdcdc; /* 添加邊框讓預覽更清晰 */
  }
    
  .uploader-interface {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  .uploader-interface p {
    margin: 4px 0;
  }
  
  .error-message {
    color: #f44336;
  }
  </style>
  