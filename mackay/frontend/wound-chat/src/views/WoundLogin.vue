<template>
  <v-app>
    <v-container class="fill-height">
      <v-row justify="center" align="center">
        <!-- 左側圖片方框 -->
        <v-col cols="12" md="4" class="v-col colLeft">
          <v-card class="image-box">
            <v-img src="../assets/loginNurse.jpg" alt="Left Image"></v-img>
          </v-card>
        </v-col>
        
        <!-- 右側登入方框 -->
        <v-col cols="12" md="4" class="v-col colRight">
          <v-card class="pa-5">
            <v-card-title class="headline text-center custom-title">會員登入</v-card-title>
            <v-divider></v-divider>
            
            <v-card-text>
              <!-- 快速登入/註冊 -->
              <template>
                <v-btn class="mb-4 justify-space-between align-center fastLogin lineFast" block @click="redirectToWoundChat('line')">
                  <div style="display: flex; align-items: center;">
                    <i class="fab fa-line" style="margin-right: 10px;"></i>
                  </div>
                  <span style="flex: 1; text-align: center;">LINE 快速登入 / 註冊</span>
                </v-btn>

                <v-btn color="white" class="mb-4 justify-space-between align-center fastLogin" block @click="redirectToWoundChat('google')">
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
export default {
  methods: {
    redirectToWoundChat() {
      // 跳轉到 /woundChat
      this.$router.push('/woundChat');
    }
  }
};
</script>

<style scoped>
.theme--light.v-application{
  background-image: url(../assets/hospital_BG.jpg);
  background-repeat: no-repeat; 
  background-size: cover;
}
.fill-height {
  min-height: 100vh;
}
.fill-height .row{
  /* box-shadow: 0 0 1px #ccc; */
  height: 70vh;
}
.image-box {
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh;
  overflow: hidden;
  filter: brightness(0.7) blur(2px);
  background-size: contain;
}
.fa-line {
  color: #fff;
  font-size: 20px;
}
.v-application .lineFast {
  margin-bottom: 25px !important;
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
  height: 70vh;
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
