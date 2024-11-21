<template>
    <v-dialog v-model="uploadImage" max-width="500px" scrollable>
      <v-card>
        <v-card-title class="headline text-center">
          請上傳傷口照片
        </v-card-title>
  
        <v-card-text>
            <v-container
                class="uploader-area"
                :class="{ 'is-dragging': fileOnDrag }"
                @dragenter.prevent="handleDragEnter"
                @dragleave.prevent="handleDragLeave"
                @drop.prevent="handleDragDrop"
                @click="triggerFileInput" 
                >
                <!-- @click="triggerFileInput" 點擊作用區 -->
                <!-- 隱藏的 input -->
                <input
                    ref="fileInput"
                    type="file"
                    accept="image/jpeg, image/png"
                    style="display: none;"
                    @change="handleInputChange"
                />

                <!-- 預覽圖顯示區 -->
                <div v-if="filePreviewSrc" class="uploader-preview">
                    <v-img :src="filePreviewSrc" contain></v-img>
                </div>

                <!-- 防呆訊息顯示區 -->
                <div v-else class="uploader-interface">
                    <v-icon size="40" color="#dcdcdc">mdi-cloud-upload-outline</v-icon>
                    <p :class="{ 'error-message': showErrorMsg }">{{ fileTips }}</p>
                    <p class="text-caption text-grey--text">僅支援 JPG/PNG 格式，最大 8 MB</p>
                </div>
            </v-container>
        </v-card-text>
  
        <v-card-actions class="justify-end">
          <v-btn text color="grey" @click="handleClose">關閉</v-btn>
          <v-btn color="primary" :disabled="!canUpload" @click="startUpload">
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
        triggerFileInput() {
            // 點擊觸發隱藏的文件選擇器
            this.$refs.fileInput.click();
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
                } else {
                this.showErrorMsg = true;
                this.fileTips = "檔案過大，需小於8MB";
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
        startUpload() {
            // 開始上傳邏輯
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
    transition: border-color 0.2s ease;
    min-height: 200px; /* 增加區域高度 */
  }
  
  .uploader-area.is-dragging {
    border-color: #42a5f5;
  }
  
  .uploader-preview {
    display: flex;
    justify-content: center;
    margin-top: 16px;
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
  