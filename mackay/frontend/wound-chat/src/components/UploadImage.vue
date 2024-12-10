<template>
    <v-dialog v-model="uploadImage" max-width="500px" scrollable>
      <v-card>
        <v-card-title class="font-large font-weight-bold text-center">
          請上傳傷口照片
          <span class="font-weight-regular font-small grey--text">僅支援JPG、PNG圖片格式(檔案限8MB內)</span>
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
                    <p :class="{ 'error-message': showErrorMsg }">{{ fileTips }}</p>
                    <p class="text-caption text-grey--text">僅支援 JPG/PNG 格式，最大 8 MB</p>
                  </div>
                </div>
            </v-container>
        </v-card-text>
  
        <v-card-actions class="justify-end">
          <v-btn text color="v-dark" @click="handleClose">取消</v-btn>
          <v-btn color="primary" text :disabled="!canUpload" @click="startUpload">
            <v-progress-circular
              v-if="showLoading"
              indeterminate
              color="white"
              size="20"
            ></v-progress-circular>
            <span v-else>確認上傳</span>
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
        fileTips: "拖曳或點擊上傳圖片", // 提示訊息
        showErrorMsg: false, // 是否顯示錯誤訊息
        canUpload: false, // 是否允許上傳
        showLoading: false, // 傳送按鈕的載入狀態
        
      };
    },
    methods: {
        startUpload() {
          // 發送 POST 圖片訊息
          let userId
          const getJWTData = JSON.parse(localStorage.getItem('mackay'));
          if (this.storeUserId) {
            userId = this.storeUserId
          }else {
            userId = getJWTData.user_id
          }
          const formData = new FormData();
          // const userId = getUserIdCheck
          const ts = new Date().getTime();
          console.log('this.file', this.file)

          formData.append('user_id', userId);
          formData.append('is_carer_user', '1'); // 0
          formData.append('photo_upload', this.file, `${userId}_${ts}.${this.file.type.split('/')[1]}`);

          axios.post('http://127.0.0.1:8000/api/chat/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
            .then((response) => {
              console.log('Message sent successfully:', response.data);
              this.uploadImage = false;
              const user_name = this.userProfile.name || '您';
              // console.log('user_name', user_name); 
              const messageData = {
                is_carer_user: false,
                user_name: user_name,
                media_url: this.filePreviewSrc,
                content_type: 'image2',
                content: '',
                isFirstDate: '',
              };
              this.$emit('message-uploaded', messageData);
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
                  this.fileTips = "檔案過大，需小於8MB";
                  this.file = null;
                }
              };
            } else {
              this.showErrorMsg = true;
              this.fileTips = "不正確的檔案類型";
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
  