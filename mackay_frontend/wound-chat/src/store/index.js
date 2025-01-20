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
    },
    user_Id: null
  },
  getters: {
    exportUserProfile(st) {
      // console.log('exportUserProfile: ', st.user_profile);
      return st.user_profile;
    },
    exportUserId(st) {
      // console.log('exportUserId: ', st.user_profile.id);
      return st.user_Id;
    },
    exportChatRoom(st) { 
      return st.chat_room;
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
      st.user_Id = payload;
      // console.log('UPDATE_USER_ID: ', st.user_profile.id);
    },
    UPDATE_CHAT_ROOM(st, payload) {
      st.chat_room = payload;
    },
    UPDATE_USER_LOGIN(st, payload) {
      st.user_login = payload;
    },
    UPDATE_ALERT(st, payload) {
      st.alert = payload;
    },
    SET_USER_ID(state, userId) {
      state.user_Id = userId;
    }
  },
  actions: {
    updateUserId({ commit }, userId) {
      commit('SET_USER_ID', userId);
    }
  },
  modules: {
  }
})
