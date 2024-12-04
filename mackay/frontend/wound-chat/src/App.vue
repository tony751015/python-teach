<template>
  <v-app>
    <v-alert class="login-alert"
      v-if='alert.show'
      dense
      transition="scale-transition"
      :value="alert_timeout"
      :type="alert.status"> {{ alert.status === 'success' ? '登入成功!' : '自動登出' }}
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
// import { mapMutations, mapGetters } from 'vuex';
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
  //   console.log('this.$route.name', this.$route.name);
  //   if (this.$route.name.match(/chat-/g) && !this.$route.query.code && !this.$route.query.state) {
  //     this.detectAutoLoginProcess();
  //   }
  // },

  mounted() {
    console.log('this.$route', this.$route);
    console.log('this.$route.name', this.$route.name);
    if (this.$route.name.match(/chat-/g) && !this.$route.query.code && !this.$route.query.state) {
      this.detectAutoLoginProcess();
    }
  },

  methods: {
    detectAutoLoginProcess() {
      const getJWT = localStorage.getItem('mackay');

      if (getJWT) {
        // alert('JWT存在');
        console.log('JWT content: ', getJWT)
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
          this.updateUserLogin(true);
          this.updateAlert({
            show: true,
            status: 'success',
          });
        }
      } else {
        // alert('JWT不存在');
        this.updateUserProfile({});
        this.updateUserLogin(false);
        this.updateAlert({
          show: true,
          status: 'error',
        });

        // this.$router.push({
        //   name: 'woundLogin'
        // })
      }
      // setTimeout(() => {
      //   this.alert_timeout = false;
      //   console.log('alert_timeout', this.alert_timeout);
      // },3000);
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
    
  },
  watch: {
    'alert.show'(newVal) {
      if (newVal) {
        this.alert_timeout = true;
        setTimeout(() => {
          this.alert_timeout = false;
        }, 3000);
      }
    },
  },
  
  // computed: {
  //   ...mapGetters({
  //     getUserProfile: 'exportUserProfile',
  //   }),
  // },
};
</script>

<style>
.row {
  margin: 0 !important;
}
.login-alert{
  position: fixed;
  top: 50px;  
  z-index: 10000;
  left: 0;
  right: 0;
  width: 200px;
  margin: auto;
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
</style>
