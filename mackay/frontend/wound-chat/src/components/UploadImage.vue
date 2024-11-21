<template>
    <v-dialog v-model="uploadImage" max-width="500px" scrollable>
      <v-card>
        <v-card-title class="headline text-center">
          選擇 <span class="text-primary font-weight-bold">上傳</span> 的圖片
        </v-card-title>
  
        <v-card-text>
          <v-container
            class="uploader-area"
            :class="{ 'is-dragging': fileOnDrag }"
            @dragenter.prevent="handleDragEnter"
            @dragleave.prevent="handleDragLeave"
            @drop.prevent="handleDragDrop"
          >
            <v-file-input
              ref="fileInput"
              v-model="file"
              accept="image/jpeg, image/png"
              show-size
              hide-input
              @change="handleChange"
              prepend-icon="mdi-upload"
            >
              <template v-slot:placeholder>
                <!-- 預覽圖顯示區 -->
                <div v-if="filePreviewSrc" class="uploader-preview">
                  <v-img :src="filePreviewSrc" aspect-ratio="1" contain></v-img>
                </div>
                <!-- 防呆訊息顯示區 -->
                <div v-else class="uploader-interface">
                  <v-icon size="40" color="#dcdcdc">mdi-cloud-upload-outline</v-icon>
                  <p :class="{ 'error-message': showErrorMsg }">{{ fileTips }}</p>
                  <p class="text-caption text-grey--text">僅支援 JPG/PNG 格式，最大 8 MB</p>
                </div>
              </template>
            </v-file-input>
          </v-container>
        </v-card-text>
  
        <v-card-actions class="justify-end">
          <v-btn text color="grey" @click="handleClose">關閉</v-btn>
          <v-btn
            color="primary"
            :disabled="!canUpload"
            @click="startUpload"
          >
            <v-progress-circular
              v-if="showLoading"
              indeterminate
              color="white"
              size="20"
            ></v-progress-circular>
            <span v-else>傳送</span>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
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
      handleChange(file) {
        this.handleUploadFile(file);
      },
  
      handleUploadFile(file) {
        this.fileOnDrag = false;
        this.showErrorMsg = false;
  
        if (file.type === 'image/jpeg' || file.type === 'image/png') {
          const _URL = window.URL || window.webkitURL;
          const img = new Image();
          img.src = _URL.createObjectURL(file);
            console.log('img.src', img.src);
          img.onload = () => {
            if (file.size < 8000 * 1024) { // 檢查檔案大小
              this.fileTips = file.name;
              this.canUpload = true;
              this.filePreviewSrc = img.src; // 設置圖片預覽
              console.log('filePreviewSrc', this.filePreviewSrc); // 測試輸出
            } else {
              this.showErrorMsg = true;
              this.fileTips = '檔案過大，需小於8MB';
            }
          };
        } else {
          this.showErrorMsg = true;
          this.fileTips = '不正確的檔案類型';
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
      handleClose() {
        this.uploadImage = false;
      },
      startUpload() {
        // 開始上傳邏輯
      }
    }
  };
  </script>
  

<style scoped>
.uploader-area {
  position: relative;
  border: 2px dashed #dcdcdc;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: border-color 0.2s ease;
}
.uploader-area.is-dragging {
  border-color: #42a5f5;
}
.uploader-preview {
  position: relative;
  width: 100%;
  height: 150px;
}
.uploader-interface {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.error-message {
  color: #f44336;
}
</style>