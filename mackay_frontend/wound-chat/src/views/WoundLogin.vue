<template>
  <v-app>
    <v-container v-if='!preloading' class="fill-height">
      <v-row justify="center" align="center" class="main-container" style="max-width: 400px;">
        <!-- 左側圖片方框 -->
        <!-- <v-col cols="12" md="4" class="v-col colLeft">
          <v-card class="image-box">
            <v-img src="../assets/loginNurse.jpg" alt="Left Image"></v-img>
          </v-card>
        </v-col> -->
        <v-col 
          cols="12" 
          style="height: 180px; width: 100%;">
          <v-layout align-center class="justify-center">
            <v-img 
            max-width="100%"
            class="aling-center loginLogo" src="../assets/trm01.png"></v-img>
          </v-layout>
          
        </v-col>
        <!-- 右側登入方框 -->
        <v-col cols="12" md="12" class="v-col colRight">
          
          <v-card class="pa-5 text-center">
            <v-card-title class="headline font-weight-bold text-center custom-title">Online Platform System</v-card-title>
            <v-chip 
             closed 
             close-label
             color="v-dark"
             class="white--text mb-3"
             >Fast log in/Sign up</v-chip>
            <v-card-text>
              <!-- 快速登入/註冊 -->
              <template>
                <!-- <v-btn
                  color="v-dark"
                  class="mb-3 justify-space-between align-center fastLogin lineFast white--text"
                  block
                  style="height: 62px;"
                  outlined
                  elevation="0"
                  @click="loginToWoundChat('line123','line會員','line')">
                  <div style="display: flex; align-items: center;">
                    <i class="fab fa-line" style="margin-right: 10px;"></i>
                  </div>
                  <span style="flex: 1; text-align: center;">LINE 快速登入 / 註冊</span>
                </v-btn> -->
                <v-btn
                  color="v-dark"
                  class="mb-3 justify-space-between align-center fastLogin lineFast white--text"
                  block
                  outlined
                  elevation="0"
                  href="https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=2006462026&redirect_uri=http://127.0.0.1:8000/&scope=openid%20profile&nonce=helloWorld&state=mackay&prompt=consent&ui_locales=zh-TW">
                  <div style="display: flex; align-items: center;">
                    <i class="fab fa-line" style="margin-right: 10px;"></i>
                  </div>
                  <span style="flex: 1; text-align: center;">LINE Account</span>
                </v-btn>

                <!-- <v-btn 
                  color="v-dark"
                  class="mb-2 justify-space-between align-center fastLogin"
                  block
                  style="height: 62px;"
                  outlined
                  elevation="0"
                  @click="loginToWoundChat('google123','google會員','google')">
                  <div style="display: flex; align-items: center;"> -->
                    <!-- <v-icon left>mdi-google</v-icon> -->
                     <!-- <v-img left class="iconImg" src="../assets/google.png"></v-img>
                  </div>
                  <span style="flex: 1; text-align: center;">GOOGLE Account</span>
                </v-btn> -->
              </template>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- 這裡在設計一個v-else 轉圈圈動畫 -->
    <!-- <span v-else style="font-size: 50px;">轉圈圈</span> -->
    <ProgressLoader :key='activeKey' :showText="`LOADING...`" :active="preloading"></ProgressLoader>


    <v-footer
      color="point-1"
      fixed
    >
      <v-card-text class=" text-center">
        <div class="caption">© 2020, MacKay Memorial Hospital. All rights reserved. No part of this website may be reproduced without written permission.</div>
        <div class="caption">Copyright © 2020, Mackay Memorial Hospital, Taiwan Christian Church Presbyterian Mackay Medical Foundation. All rights reserved.</div>
      </v-card-text>
      <v-card-text class="black--text text-center py-0 mb-4">
        <a class="black--text px-2 caption bdR" href="">Homepage</a>
        <a class="black--text px-2 caption bdR" href="">Facebook</a>
        <a class="black--text px-2 caption" href="">LINE</a>
      </v-card-text>
    </v-footer>
  </v-app>
</template>

<script>
import axios from 'axios';
import ProgressLoader from '../common/progessLoading.vue';
export default {
  components: {
    ProgressLoader,
  },
  created() {
    console.log('LOGIN STATUS 2: ', this.userLogin);

    // LINE登入Callback頁面
    if (this.$route.query.code && this.$route.query.state) {
      const LoginProcess = new Promise((resolve) => {
        const done = this.userLoginProcess(this.$route.query.code, this.$route.query.state);
        if (done) {
          return resolve({
            status: 'ok',
            value: true,
          });
        }
      })

      LoginProcess.then((value) => {
        if (value.status === 'ok') {
          this.activeKey += 1 ;
          this.preloading = value.value;
          console.log('LOGIN STATUS END: ', this.userLogin);
        }
      });
    } else {
      this.preloading = false
    }

  },

  data() {
    return {
      preloading: true,
      activeKey: 0,
    };
  },

  methods: {
    loginToWoundChat(patient_id , patient_name, patient_auth) {
      axios.post('http://127.0.0.1:8000/api/member/fast_login', {
          patient_id: patient_id,
          patient_name: patient_name,  
          patient_auth: patient_auth
        })
        .then((response) => {
          // 跳轉到 /woundChat
          console.log('Login successfully:', response.data);
          this.$router.push({ name: 'chat-room' });
        })
        .catch((err) => {
          console.error('Error sending message:', err);
        });
      
    }
  },
};
</script>

<style scoped>
.theme--light.v-application{
  background-image: url(../assets/loginBG.png); 
  background-repeat: no-repeat; 
  background-size: cover;
  background-position: center;
}
.fill-height {
  min-height: 100vh;
  justify-content: center;
}
.main-container {
  transform: translate3d(0, -7vh, 0);
}
.image-box {
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  filter: brightness(0.7) blur(2px);
  background-size: contain;
}
.fa-line {
  color: #fff;
  font-size: 20px;
}
.v-application .lineFast {
  color: #fff;
  background-color: #06c755;
}
.custom-title {
  font-size: 1.3rem !important;
  padding: 8px 16px;
  justify-content: center;
}
.v-btn.fastLogin {
  font-size: 1rem;
  height: 62px;
}
.v-col{
  padding: unset;
}
.colRight .pa-5{
  border-radius: 15px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
}
.colRight .custom-title{
  letter-spacing: 3px !important;
}
.loginLogo{
  justify-content: center;
}

.iconImg{
  width: 20px;
}
.bdR{
  border-right: 1px solid #fff;
}
@media screen and (max-width: 767px){
  .colRight .pa-5{
    height: 40vh;
  }
  .image-box{
    height: 40vh;
  }
}
</style>
