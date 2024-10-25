import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';
import InfiniteLoading from 'vue-infinite-loading';
Vue.component('infinite-loading', InfiniteLoading);
import axios from 'axios'
Vue.prototype.$http = axios
Vue.config.productionTip = false

import { mapGetters, mapMutations } from 'vuex';

Vue.mixin({
  methods: {
    ...mapMutations({
      updateUserProfile: 'UPDATE_USER_PROFILE',
    }),
  },

  computed: {
    ...mapGetters({
      exportUserProfile: 'exportUserProfile',
    }),
  },
})

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
