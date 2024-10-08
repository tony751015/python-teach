<template>
  <v-row :class="[is_carer_user ? 'justify-start' : 'justify-end']" style="margin: 0;">
    <v-col cols="auto">
      <v-card 
        :class="[is_carer_user ? 'other-message': 'own-message']"
        flat>
        <v-card-text 
          v-if="content_type === 'text'"
          class="font-weight-bold">{{content}}</v-card-text>
        
        <v-card-text 
          v-else-if="content_type === 'image'">
          <img :src="content" @click="$emit('image-click', content)" />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
  
<script>
export default {
  name: 'ChatMessage',
  props: {
    is_carer_user: {
      type: Boolean,
      required: true
    },
    content_type: {
      type: String,
      required: true
    },
    user_name: {
      type: String,
      required: true
    },
    content: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.col-auto{
  max-width: 60%;
  padding: 0;
}
.v-card__text{
  padding: 10px 15px;
}
.own-message {
  background-color: #000 !important;
  color: #fff;
  border-radius: 16px 16px 0 16px;
  margin: 5px 0;
  margin-right: 5px;
}
.own-message .v-card__text{
  color: #FFF;
}

.other-message {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 16px 16px 16px 0;
  margin: 5px 0;
}

img {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  margin-top: 10px;
  cursor: pointer;
}
</style>
