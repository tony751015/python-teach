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
      // console.log('exportUserProfile: ', st.user_profile);
      return st.user_profile;
    },
    exportUserId(st) {
      // console.log('exportUserId: ', st.user_profile.id);
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
      // if (st.user_profile) {
      //   st.user_profile.id = payload;
      // }
      st.user_profile.id = payload;
      // console.log('UPDATE_USER_ID: ', st.user_profile.id);
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
