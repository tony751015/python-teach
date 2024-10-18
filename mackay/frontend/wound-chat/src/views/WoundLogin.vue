<template>
  <v-app>
    <v-container class="fill-height">
      <v-row justify="center" align="center" style="max-width: 400px;">
        <!-- 左側圖片方框 -->
        <!-- <v-col cols="12" md="4" class="v-col colLeft">
          <v-card class="image-box">
            <v-img src="../assets/loginNurse.jpg" alt="Left Image"></v-img>
          </v-card>
        </v-col> -->
        <v-col 
          cols="12" 
          style="height: 150px; width: 100%;">
          <v-layout align-center class="justify-center">
            <v-img 
            max-width="70%"
            class="aling-center loginLogo" src="../assets/trm01.png"></v-img>
          </v-layout>
          
        </v-col>
        <!-- 右側登入方框 -->
        <v-col cols="12" md="12" class="v-col colRight">
          
          <v-card class="pa-5 text-center">
            <v-card-title class="headline font-weight-bold text-center custom-title">傷造口遠距照護諮詢平台</v-card-title>
            <v-chip 
             closed 
             close-label
             color="v-dark"
             class="white--text mb-3"
             >會員快速登入</v-chip>
            <v-card-text>
              <!-- 快速登入/註冊 -->
              <template>
                <v-btn
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
                </v-btn>

                <v-btn 
                  color="v-dark"
                  class="mb-2 justify-space-between align-center fastLogin"
                  block
                  style="height: 62px;"
                  outlined
                  elevation="0"
                  @click="loginToWoundChat('google123','google會員','google')">
                  <div style="display: flex; align-items: center;">
                    <!-- <v-icon left>mdi-google</v-icon> -->
                     <v-img left class="iconImg" src="../assets/google.png"></v-img>
                  </div>
                  <span style="flex: 1; text-align: center;">Google 快速登入 / 註冊</span>
                </v-btn>
              </template>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-footer
      color="v-dark"
      fixed
    >
      <v-card-text class="white--text text-center">
        <div class="caption">© 2020, MacKay Memorial Hospital     本網站內容為馬偕紀念醫院所有，未經許可請勿轉載。</div>
        <div class="caption">台灣基督長老教會馬偕醫療財團法人馬偕紀念醫院 著作權所有，並保留一切權利。</div>
      </v-card-text>
      <v-card-text class="white--text text-center py-0 mb-4">
        <a class="white--text px-2 caption bdR" href="">馬偕醫院首頁</a>
        <a class="white--text px-2 caption bdR" href="">FB粉專</a>
        <a class="white--text px-2 caption" href="">LINE官方帳號</a>
      </v-card-text>
    </v-footer>
  </v-app>
</template>

<script>
import axios from 'axios';
export default {
  methods: {
    loginToWoundChat(patient_id , patient_name, patient_auth) {
      axios.post('http://127.0.0.1:8000/api/member/fast_login', {
          patient_id: patient_id,
          patient_name: patient_name,  
          patient_auth: patient_auth
        })
        .then((response) => {
          console.log('Login successfully:', response.data);
          // 跳轉到 /woundChat
          this.$router.push('/woundChat');
        })
        .catch((err) => {
          console.error('Error sending message:', err);
        });
      
    }
  }
};
</script>

<style scoped>
.theme--light.v-application{
  background-image: url(../assets/loginBG.png); 
  background-repeat: no-repeat; 
  background-size: cover;
}
.fill-height {
  min-height: 100vh;
  justify-content: center;
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
