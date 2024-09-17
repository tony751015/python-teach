<template>
  <v-row :class="[isOwnMessage ? 'justify-end': 'justify-start']" style="margin: 0;">
    <v-col cols="auto">
      <v-card 
        :class="[isOwnMessage ? 'own-message': 'other-message']"
        flat>
        <v-card-text 
          v-if="content_type === 'text'"
          class="font-weight-bold">{{message}}</v-card-text>
        
        <v-card-text 
          v-else-if="content_type === 'image'"
        >
          <img :src="message">
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
  
<script>
export default {
  name: 'ChatMessage',
  props: {
    isOwnMessage: {
      type: Boolean,
      required: true
    },
    content_type: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    message: {
      type: String,
      required: true
    }
  }
}
// console.log(this.content_type)
</script>

<style scoped>
.col-auto{
  max-width: 60%;
  padding: 0;
}
.v-card__text{
  padding: 10px 15px;
}
/* .row-reverse{
  flex-direction: row-reverse;
} */
.own-message {
  background-color: #000 !important;
  color: #fff;
  border-radius: 16px 16px 0 16px;
  /* padding: 3px 8px; */
  margin: 5px 0;
  /* max-width: 60%; */
}
.own-message .v-card__text{
  color: #FFF;
}

.other-message {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 16px 16px 16px 0;
  /* padding: 3px 8px; */
  margin: 5px 0;
  /* max-width: 60%; */
}

img {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  margin-top: 10px;
}
</style>
  