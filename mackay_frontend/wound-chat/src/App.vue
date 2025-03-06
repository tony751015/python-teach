<template>
  <v-app>
    <v-alert class="login-alert text-center"
      v-if='alert.show'
      dense
      transition="scale-transition"
      :value="alert_timeout"
      :type="alert.status"> {{ alert.message }}
    </v-alert>
      
    
    <!-- <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar> -->

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>


<script>
import { mapMutations, mapGetters } from 'vuex';
import * as jwt_decode from 'jwt-decode';

export default {
  name: 'App',

  data: () => ({
    alertShow: false,
    alertStatus: '',
    alert_timeout: true,
    timer: '',
  }),

  // created() {
  //   // console.log('this.$route.name', this.$route.name);
  //   // if (this.$route.name.match(/chat-/g) && !this.$route.query.code && !this.$route.query.state) {
  //   //   this.detectAutoLoginProcess();
  //   // }
  // },

  mounted() {
    console.log('this.$route', this.$route);
    console.log('this.$route.name', this.$route.name);

    window.addEventListener('resize', this.clientWidthResize);
    // window.addEventListener('scroll', this.handleGoTopBtnShow);
    this.$nextTick(() => {
      this.clientWidthResize();
    });
    // if (this.$route.query.code && this.$route.query.state&& this.$route.name === 'woundLogin') {
      // console.log('AAAAAAAAAA1: ', this.$route.name);
    // const url = new URL("http://127.0.0.1:3000/");
    // const loginPage = url.href;
    // console.log('loginPage', loginPage);
    // console.log('URL', location.href.code);
    // if (loginPage === location.href && location.href.code && location.href.state) {
    //   // this.detectAutoLoginProcess();
    //   alert('reline callback')
      
    //   const LoginProcess = new Promise((resolve) => {
    //     const done = this.userLoginProcess(this.$route.query.code, this.$route.query.state);
    //     if (done) {
    //       return resolve({
    //         status: 'ok',
    //         value: true,
    //       });
    //     }
    //   })

    //   LoginProcess.then((value) => {
    //     if (value.status === 'ok') {
    //       alert('test ok')
    //       // this.activeKey += 1 ;
    //       // this.preloading = value.value;
    //       console.log('LOGIN STATUS END: ', this.userLogin);
    //     }
    //   });
    //   return;
    // } 
    this.checkURL(location.href);
    // this.initializeApp().then(() => {
    //     this.autoRelogin();
    // });
  },
  
  methods: {
    ...mapMutations({
      updateRwdType: 'SET_RWD_TYPE',
    }),

    checkURL(url) {
      try {
        const urlObj = new URL(url);

        console.log('URL:', url);
        console.log('Origin:', urlObj.origin);
        console.log('Pathname:', urlObj.pathname);
        console.log('path:', this.PATH_CHECK);

        // 檢查 domain 和 pathname，確保沒有任何路徑、字元或 query parameters
        if (urlObj.origin != this.PATH_CHECK || urlObj.pathname != '/') {
          console.log('網址不符合條件');
          this.autoRelogin();
          return '網址不符合條件';
        }
        return '網址符合條件';

      } catch (error) {
        console.log('網址格式錯誤:', error);
        return '網址格式錯誤';
      }
    },

    detectAutoLoginProcess() {
      const getJWT = localStorage.getItem('mackay');
      const getJWTData = JSON.parse(localStorage.getItem('mackay'));

      console.log('getJWTData_id', getJWTData.user_id);
      if (getJWT) {
        // alert('JWT存在');
        // console.log('JWT content: ', getJWT)
        const decoded = jwt_decode(getJWT);
        const { exp } = decoded;
        // const iat = Number(decoded.iat);
        const dateNow = Date.now() / 1000;
        console.log('JWT content: ', decoded)
     
        if (exp - dateNow > 0) {
          const USER_PROFILE = {
            name: decoded.name,
            line_id: decoded.sub,
            thumb: decoded.picture,
          }

          this.updateUserProfile(USER_PROFILE);
          this.updateUserId(getJWTData.user_id);
          this.updateUserLogin(true);
          this.updateAlert({
            show: true,
            status: 'success',
            message: 'Login ok!'
          });
        }
        this.$router.push('/chat/'+getJWTData.user_id);
      } else {
        // alert('JWT不存在');
        this.updateUserProfile({});
        this.updateUserLogin(false);
        this.updateAlert({
          show: true,
          status: 'error',
          message: 'Please log in again!'
        });

        this.$router.push('/');
      }
      // setTimeout(() => {
      //   this.alert_timeout = false;
      //   console.log('alert_timeout', this.alert_timeout);
      // },3000);
    },

    clientWidthResize() {
      this.clientWidth = document.documentElement.clientWidth;
      this.clientHeight = document.documentElement.clientHeight;
      // INIT Rwd Type
      if (this.clientWidth >= 1280) {
        this.updateRwdType('desktop');
        // this.changeHamburgerFocus(false);
      } else if (this.clientWidth < 1280 && this.clientWidth > 1080) {
        this.updateRwdType('tablet');
        // this.changeHamburgerFocus(false);
      } else if (this.clientWidth <= 1080 && this.clientWidth > 730) {
        this.updateRwdType('tablet-m');
      } else {
        this.updateRwdType('mobile');
      }

      console.log('CHECK RWDTYPE', this.getRwdType);
    },
    
    // detectAutoLoginProccess() {
    //   const getJWT = localStorage.getItem('mackay');

    //   if (getJWT) {
    //     // const JWT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FjY2Vzcy5saW5lLm1lIiwic3ViIjoiVTk4Y2Q2NTIxMjk3YzVhNzE0MzcyYWFiZWZhZWY1YmM5IiwiYXVkIjoiMjAwNjQ2MjAyNiIsImV4cCI6MTcyOTgyNzIwMywiaWF0IjoxNzI5ODIzNjAzLCJub25jZSI6ImhlbGxvV29ybGQiLCJhbXIiOlsibGluZXNzbyJdLCJuYW1lIjoi5ZGo5a2Q5aCvIFZpY3RvciIsInBpY3R1cmUiOiJodHRwczovL3Byb2ZpbGUubGluZS1zY2RuLm5ldC8waEJBclpMOTBlSFc1UEl3anZEcVZpT1hObUV3TTREUnNtTnhKYURqb2dGbHhnUmxrX2Uwd0ZDMjUwRkFsa1FROXJJUmRXQ1RseEZBNHcifQ.fDIzyGerYXRTI_B17ZbNI1m29GZFKehM0V6IAKztWPM';
  
    //     // const accessToken = JSON.parse(JWT);
    //     const decoded = jwt_decode(getJWT);
    //     const { exp } = decoded;
    //     const iat = Number(decoded.iat);
    //     const dateNow = Date.now() / 1000;

    //     console.log('JWT content: ', decoded)
  
    //     if (exp - dateNow > 0) {
    //       console.log('JWT令牌在免驗證時間內，不做任何事 | Exp:', (exp), 'Iat:', (iat), 'Count', (iat - exp), );

    //       const USER_PROFILE = {
    //         name: decoded.name,
    //         line_id: decoded.sub,
    //         thumb: decoded.picture,
    //       }
    //       this.updateUserProfile(USER_PROFILE);

    //     } else {
    //       console.log('JWT令牌過期了，強制登出 | Exp:', (exp), 'Iat:', (iat), 'Count', (iat - exp));
    //       // localStorage.removeItem('mackay');
    //     }
    //   }
    // }
    
    // async initializeApp() {
    //     // 假設有一些異步操作需要完成
    //     const mackayData = await this.loadLocalStorageData();
    //     console.log('LocalStorage 已加載:', mackayData);
    // },

    // loadLocalStorageData() {
    //     return new Promise((resolve) => {
    //         const data = localStorage.getItem('mackay');
    //         resolve(data);
    //     });
    // }
  },
  watch: {
    'alert.show'(newVal) {
      if (newVal) {
        this.alert_timeout = true;
        setTimeout(() => {
          this.alert_timeout = false;
          this.updateAlert({
            show: false,
            status: '',
            message: ''
          });
        }, 3000);
      }
    },
  },
  
  computed: {
    ...mapGetters({
      getRwdType: 'exportRwdType',
    }),
  },
};
</script>

<style lang="scss">
$topbarHeight: '38px';

.row {
  margin: 0 !important;
}

.v-dialog {
  /* v-dialog樣式寫在這裡。 */
}
.v-app-bar .dropdown-btn{
  padding: 0 10px;
}
.login-alert{
  position: fixed;
  top: 50px;  
  z-index: 10000;
  left: 0;
  right: 0;
  width: 300px;
  margin: auto;
}
.login-alert .v-alert__content{
  margin-left: -40px;
}
.font-super-small {
  font-size: 10px !important;
}

.font-small {
  font-size: 12px !important;
}

.font-normal {
  font-size: 14px !important;
}

.font-large {
  font-size: 16px !important;
}

.font-super-large {
  font-size: 18px !important;
}
// 桌機版
// @media (min-width: 1280px) and (max-width: 9999px) {}

// 平板版
// @media (min-width: 731px) and (max-width: 1279px) {}

// 手機板
@media (max-width: 730px) {
  .v-app-bar {
    height: #{$topbarHeight} !important;
    .v-slide-group, .v-toolbar__content, .v-toolbar__extension {
      height: #{$topbarHeight} !important;
    }
    .main-logo {
      width: 100px;
      height: 21px !important;
      padding: 0 !important;
    }
  }
}
</style>
