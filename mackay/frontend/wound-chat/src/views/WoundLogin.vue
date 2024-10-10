<template>
  <v-app>
    <v-container class="fill-height">
      <v-row justify="center" align="center" style="max-width: 400px; border-radius: 15px; overflow: hidden; box-shadow: 0px 5px 15px #e3e3e3;">
        <!-- 左側圖片方框 -->
        <!-- <v-col cols="12" md="4" class="v-col colLeft">
          <v-card class="image-box">
            <v-img src="../assets/loginNurse.jpg" alt="Left Image"></v-img>
          </v-card>
        </v-col> -->
        <v-col 
          cols="12" 
          style="height: 250px; width: 100%; background-size: cover; background-image: url(https://images.squarespace-cdn.com/content/v1/5ebaaed9bb839b7b67d29b74/1595423617407-II6O8RO8D10X3DPXO4RJ/PatientFlow%26OperationalVisibility.jpg);"></v-col>
        <!-- 右側登入方框 -->
        <v-col cols="12" md="12" class="v-col colRight">
          
          <v-card class="pa-5">
            <v-card-title class="headline text-center custom-title">會員登入</v-card-title>
            <v-divider></v-divider>
            
            <v-card-text>
              <!-- 快速登入/註冊 -->
              <template>
                <v-btn
                  color="v-dark"
                  class="mb-3 justify-space-between align-center fastLogin lineFast white--text"
                  block
                  x-large
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
                  x-large
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
  /* background-image: url(../assets/hospital_BG.jpg); */
  background-repeat: no-repeat; 
  background-size: cover;
}
.fill-height {
  min-height: 100vh;
}
.fill-height{
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
}
.v-btn.fastLogin {
  font-size: 1rem;
}
.v-col{
  padding: unset;
}
.colRight .pa-5{
  box-shadow: unset;
  background-color: #f5f5f5;
  border-radius: 0 4px 4px 0;
}
.colLeft .pa-5{
  border-radius: 4px 0 0 4px;
}
.iconImg{
  width: 20px;
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
