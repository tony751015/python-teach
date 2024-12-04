import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user_profile: {},
    user_login: false,
    alert: {
      show: false,
      status: '',
    }
  },
  getters: {
    exportUserProfile(st) {
      return st.user_profile;
    },
    exportUserId(st) {
      return st.user_profile.id;
    },
    exportUserLogin(st) {
      return st.user_login;
    },
    exportAlert(st) {
      return st.alert;
    },
  },
  mutations: {
    UPDATE_USER_PROFILE(st, payload) {
      st.user_profile = payload;
    },
    UPDATE_USER_ID(st, payload) {
      st.user_profile.id = payload;
    },
    UPDATE_USER_LOGIN(st, payload) {
      st.user_login = payload;
    },
    UPDATE_ALERT(st, payload) {
      st.alert = payload;
    },
  },
  actions: {
  },
  modules: {
  }
})
