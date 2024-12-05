import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';
import InfiniteLoading from 'vue-infinite-loading';
import axios from 'axios'

Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.component('infinite-loading', InfiniteLoading);

import { mapGetters, mapMutations } from 'vuex';
import * as jwt_decode from 'jwt-decode';

const VUEX_FEATURE = {
  data: () => ({
    SERVER_PATH: process.env.VUE_APP_SERVER_PATH,
    VUE_PATH: process.env.VUE_APP_PATH,
  }),

  methods: {
    ...mapMutations({
      updateUserProfile: 'UPDATE_USER_PROFILE',
      updateUserLogin: 'UPDATE_USER_LOGIN',
      updateUserId: 'UPDATE_USER_ID',
      updateAlert: 'UPDATE_ALERT',
    }),
    autoRelogin() {
      const getJwt = localStorage.getItem('mackay');
      const getJwtJson = JSON.parse(getJwt)
      console.log('Check JWT', getJwtJson)

      if (getJwt) {
        const decoded = jwt_decode(getJwtJson.jwt);

        const USER_PROFILE = {
          name: decoded.name,
          line_id: decoded.sub,
          thumb: decoded.picture,
          id: getJwtJson.user_id
        }

        console.log('autoRelogin', USER_PROFILE);

        this.updateUserProfile(USER_PROFILE);
        this.updateUserId(USER_PROFILE.id);
        this.updateUserLogin(true);
        this.updateAlert({
          show: true,
          status: 'success',
        });
      } else {
        this.updateUserProfile(null);
        this.updateUserId(null);
        this.updateUserLogin(false);
        this.updateAlert({
          show: true,
          status: 'error',
        });

        this.$router.push('/');
      }
    },

    routerRedirectTo404() {
      this.$router.push({name: 'error404'});
    },

    // showAlertBlock(status) {
    //   this.alertShow = true;
    //   this.alertStatus = status;
      
    //   console.log('RUN ALERT: ', status, this.alertShow, this.alertStatus);
    //   // setTimeout(() => {
    //   //   this.alertShow = false;
    //   // }, 5000);
    // },

    userLoginProcess(code, state) {
      axios.post('http://127.0.0.1:8000/api/member/line_login', {code, state,})
        .then((res) => {
          const getJWT = res.data.jwt_token;
          
          if (getJWT) {
            // alert('JWT存在');
            console.log('JWT content: ', getJWT)
            const localStorageSaveObj = {
              jwt: getJWT,
              user_id: res.data.user_id,
            };
            
            localStorage.setItem('mackay', JSON.stringify(localStorageSaveObj));

            const decoded = jwt_decode(getJWT);

            const USER_PROFILE = {
              name: decoded.name,
              line_id: decoded.sub,
              thumb: decoded.picture,
              id: res.data.user_id
            }

            this.updateUserProfile(USER_PROFILE);
            this.updateUserId(USER_PROFILE.id);
            this.updateUserLogin(true);
            this.updateAlert({
              show: true,
              status: 'success',
            });

            console.log('LOGIN STATUS: ', this.userLogin);
            console.log('USER_PROFILE: ', USER_PROFILE);
            // localStorage.setItem('userId', USER_PROFILE.id);  
            localStorage.setItem('userName', USER_PROFILE.name);
            localStorage.setItem('userThumb', USER_PROFILE.thumb);
            // this.showAlertBlock('success');
          }

          // this.$router.push({name: 'chat-list'});

          this.$router.push('/chat/'+res.data.user_id);
        })
        .catch((err) => {
          console.error('LINE LOGIN Failed:', err);
          this.updateUserProfile({});
          this.updateUserId('');
          this.updateUserLogin(false);
          this.updateAlert({
            show: true,
            status: 'error',
          });
          localStorage.removeItem('mackay');
        });

      return true;
    },
    logout() {
      localStorage.removeItem('mackay');
      localStorage.removeItem('userName');
      localStorage.removeItem('userThumb');
      this.updateAlert({
        show: true,
        status: 'error',
      });
      setTimeout(() => {
        this.$router.push('/');
      }, 1000);
    }
  },

  computed: {
    ...mapGetters({
      userProfile: 'exportUserProfile',
      userLogin: 'exportUserLogin',
      storeUserId: 'exportUserId',
      alert: 'exportAlert',
    }),
  },
}

Vue.mixin(VUEX_FEATURE);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
