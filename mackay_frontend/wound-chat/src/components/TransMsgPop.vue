<template>
  <v-bottom-sheet v-model="localVisible" inset>
    <v-sheet class="trans-msg-pop">
      <!-- 頂部工具欄 -->
      <v-toolbar dense color="main-green" dark>
        <v-spacer></v-spacer>
        <v-toolbar-title class="text-center mx-auto">翻譯訊息</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon dark @click="close" class="ml-n6">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text class="trans-input-area">
        <div class="block-title">原文</div>
        <v-textarea
          v-model="originText"
          outlined
          color="main-green"
          auto-grow
          rows="2"
          row-height="30"
          
          placeholder="原文內容..."
          hide-details
          class="trans-textarea mb-2"
        ></v-textarea>
        <div class="action-buttons-grid mb-2">
          <div class="grid-item">
            <v-btn color="main-green" text class="action-btn" @click="onFixAndTranslate">{{ allowEdit ? '修正完成並翻譯' : '修正並翻譯' }}</v-btn>
          </div>
          <div class="grid-item text-right">
            <v-btn color="main-green" text class="action-btn" @click="onTranslate" :disabled="loadingTranslate">{{ loadingTranslate ? '翻譯中...' : '翻譯' }}</v-btn>
          </div>
        </div>
        <div class="block-title">翻譯</div>
        <v-textarea
          v-model="transText"
          outlined
          color="main-green"
          auto-grow
          rows="2"
          row-height="30"
          
          placeholder="翻譯內容..."
          hide-details
          class="trans-textarea mb-2"
        ></v-textarea>
        <div class="d-flex justify-end mt-2">
          <v-btn color="main-green" text class="action-btn" @click="onSubmit" :disabled="loadingSubmit">{{ loadingSubmit ? '送出中...' : '送出' }}</v-btn>
        </div>
      </v-card-text>
    </v-sheet>
  </v-bottom-sheet>
</template>

<script>
import axios from 'axios'
export default {
  name: 'TransMsgPop',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    // 初始原文/翻譯（可選）
    originTextInit: { type: String, default: '' },
    transTextInit: { type: String, default: '' }
  },
  data() {
    return {
      localVisible: false,
      originText: '',
      transText: '',
      allowEdit: false,
      loadingTranslate: false,
      loadingSubmit: false
    };
  },
  watch: {
    visible(val) {
      this.localVisible = val;
      if (val) {
        this.originText = this.originTextInit || this.originText;
        this.transText = this.transTextInit || '';
        this.allowEdit = false;
      }
    },
    localVisible(val) {
      this.$emit('update:visible', val);
    }
  },
  methods: {
    close() {
      this.localVisible = false;
    },
    normalizedUserLang() {
      const jwt = JSON.parse(localStorage.getItem('mackay') || '{}')
      const lang = jwt.user_lang || this.userProfile.user_lang || 'en'
      if (['zh', 'zh-tw', 'zh_TW', 'zh-Hant'].includes(lang)) return 'zh-tw'
      return lang
    },
    async doTranslate(text) {
      try {
        this.loadingTranslate = true
        this.transText = ''
        const res = await axios.post(`${this.SERVER_PATH}chatTranslate/api/translate/`, {
          text,
          source_lang: 'zh-tw',
          target_lang: this.normalizedUserLang()
        })
        if (res.data && res.data.success) {
          this.transText = res.data.translated_text || ''
        } else {
          this.transText = ''
        }
      } catch (e) {
        this.transText = ''
        console.error('translate failed', e)
      } finally {
        this.loadingTranslate = false
      }
    },
    onTranslate() {
      const text = (this.originText || '').trim()
      if (!text) return
      this.allowEdit = false
      this.doTranslate(text)
    },
    onFixAndTranslate() {
      const origin = (this.originText || '').trim()
      if (!origin) return
      // 先請求校對 API，將修正後文字覆蓋 originText，再進行翻譯
      this.loadingTranslate = true
      this.transText = ''
      axios.post(`${this.SERVER_PATH}chatTranslate/api/proofread/`, { text: origin })
        .then(res => {
          const corrected = (res.data && res.data.corrected_text) ? res.data.corrected_text : origin
          this.originText = corrected
          return this.doTranslate(corrected)
        })
        .catch(err => {
          console.error('proofread failed', err)
          // 校對失敗則用原文直接翻譯
          return this.doTranslate(origin)
        })
        .finally(() => {
          this.loadingTranslate = false
        })
    },
    async onSubmit() {
      const content = (this.originText || '').trim()
      const contentTrans = (this.transText || '').trim()
      if (!content) return
      try {
        this.loadingSubmit = true
        let fetch_chatRoom
        const getJWTData = JSON.parse(localStorage.getItem('mackay')) || {}
        if (this.userProfile && this.userProfile.super_user) {
          if (getJWTData.room_path) {
            fetch_chatRoom = getJWTData.room_path
          } else {
            fetch_chatRoom = this.storeChatRoom
          }
        } else {
          fetch_chatRoom = this.userProfile && this.userProfile.room_path
        }
        const isCarer = this.userProfile ? (this.userProfile.super_user === true) : true
        const res = await axios.post(`${this.SERVER_PATH}api/chat/control`, {
          user_id: this.userProfile && this.userProfile.id,
          chatRoom: fetch_chatRoom,
          is_carer_user: isCarer,
          content: content,
          content_trans: contentTrans,
          user_lang: this.normalizedUserLang(),
          content_type: 'text'
        })
        const messageData = {
          is_carer_user: isCarer,
          user_name: (this.userProfile && this.userProfile.name) || '您',
          media_url: '',
          content: content,
          content_trans: contentTrans,
          content_type: 'text',
          isFirstDate: ''
        }
        this.$emit('message-uploaded', messageData)
        this.$emit('submitted', { record_id: res.data && res.data.record_id, content, content_trans: contentTrans })
        // 清空輸入區
        this.originText = ''
        this.transText = ''
        this.close()
      } catch (e) {
        console.error('submit failed', e)
      } finally {
        this.loadingSubmit = false
      }
    }
  }
};
</script>

<style scoped>
.trans-msg-pop {
  padding-bottom: 16px;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
}
.trans-input-area {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
}
.trans-textarea {
  margin-bottom: 15px;
}
.block-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 4px;
}
.action-buttons-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
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
  line-height: 1.35;
  margin-top: 4px;
}
.action-btn.v-btn--disabled {
  opacity: 0.6;
}
</style>
