<template>
  <v-dialog v-model="dialog" persistent max-width="400px">
    <v-card>
      <v-card-title class="headline">Please select your language.</v-card-title>
      <v-card-text>
        <v-select
          v-model="selectedLang"
          :items="langOptions"
          label="please select language"
          outlined
        ></v-select>
        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          @click="confirmLang"
          :loading="loading"
          :disabled="loading"
        >
          submit
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios';
export default {
  name: 'LangSelect',
  props: {
    value: {
      type: Boolean,
      default: false
    },
    langOptions: {
      type: Array,
      default: () => [
        { text: 'English', value: 'en' },
        { text: 'Spanish', value: 'es' },
        { text: 'French', value: 'fr' },
        { text: 'German', value: 'de' },
        { text: 'Italian', value: 'it' },
        { text: 'Portuguese', value: 'pt' }
      ]
    }
  },
  data() {
    return {
      dialog: this.value,
      selectedLang: '',
      loading: false,
      errorMsg: ''
    };
  },
  watch: {
    value(val) {
      this.dialog = val;
    },
    dialog(val) {
      this.$emit('input', val);
    }
  },
  methods: {
    async confirmLang() {
      if (!this.selectedLang) {
        this.errorMsg = 'please select language';
        return;
      }
      // 二次確認
      const langText = this.langOptions.find(opt => opt.value === this.selectedLang)?.text || this.selectedLang;
      if (!window.confirm(`Are you sure you want to select "${langText}" as your language?`)) {
        return;
      }
      this.errorMsg = '';
      this.loading = true;
      try {
        await axios.put(`${this.SERVER_PATH}api/user/update_lang`, {
          user_id: this.userProfile.id,
          user_lang: this.selectedLang
        });
        this.$emit('lang-selected', this.selectedLang);
        this.dialog = false;
      } catch (err) {
        this.errorMsg = 'Language setting failed. Please try again.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.error-msg {
  color: red;
  font-size: 14px;
  margin-top: 8px;
}
</style>
