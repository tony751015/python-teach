<template>
    <v-row :class="{'justify-end': isOwnMessage, 'justify-start': !isOwnMessage}">
      <v-col cols="auto">
        <v-card :class="{'own-message': isOwnMessage, 'other-message': !isOwnMessage}" flat>
          <v-card-text v-html="message"></v-card-text>
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
    background-color: #000;
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
    background-color: #FFF;
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
  