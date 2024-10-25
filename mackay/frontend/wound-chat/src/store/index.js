import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user_profile: {}
  },
  getters: {
    exportUserProfile(st) {
      return st.user_profile;
    },
  },
  mutations: {
    UPDATE_USER_PROFILE(st, payload) {
      st.user_profile = payload;
    },
  },
  actions: {
  },
  modules: {
  }
})
