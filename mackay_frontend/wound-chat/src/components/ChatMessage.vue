<template lang="pug">
  div
    .date-divider.text-center.grey--text.font-small {{ isFirstDate }}
    v-row(:class="alignmentClass" style="margin: 0;")
      v-col(cols="auto" v-if="content_type === 'text'")
        v-card.mr-4(:class="[messageClass, 'mr-4']" flat)
          v-card-text.font-large.font-weight-bold(class="font-weight-bold" v-html="contentRegexMatchURL")

      v-col.img_col(cols="5" :key="media_url" class="img_col" v-else-if="content_type === 'image'")
        v-card.mr-4(color="point-1" :class="[messageClass, 'mr-4']" flat)
          img(:src="`${IMG_PATH}media/${media_url}`" @click="$emit('image-click', `${IMG_PATH}media/${media_url}`)")

      v-col(cols="5" :key="media_url" class="img_col" v-else-if="content_type === 'image2'")
        v-card.mr-4(color="point-1" :class="[messageClass, 'mr-4']" flat)
          img(:src="media_url" @click="$emit('image-click2', media_url)")

  //- <div>
  //-   <div class="date-divider text-center grey--text">{{ isFirstDate }}</div>
  //-   <v-row :class="alignmentClass" style="margin: 0;">
  //-     <v-col cols="auto" v-if="content_type === 'text'">
  //-       <v-card 
  //-         :class="[messageClass, 'mr-4']"
  //-         flat>
  //-         <v-card-text
  //-           class="font-weight-bold" v-html="contentRegexMatchURL"></v-card-text>
  //-       </v-card>
        
  //-     </v-col>
  //-     <v-col cols="5" :key="media_url" class="img_col"  v-else-if="content_type === 'image'">
  //-       <v-card 
  //-         color="point-1"
  //-         :class="[messageClass, 'mr-4']"
  //-         flat>
  //-           <img :src="`${IMG_PATH}media/${media_url}`" @click="$emit('image-click', `${IMG_PATH}media/${media_url}`)" />
  //-       </v-card>
  //-     </v-col>
  //-     <v-col cols="5" :key="media_url" class="img_col"  v-else-if="content_type === 'image2'">
  //-       <v-card 
  //-         color="point-1"
  //-         :class="[messageClass, 'mr-4']"
  //-         flat>
  //-           <img :src="media_url" @click="$emit('image-click2', media_url)" />
  //-       </v-card>
  //-     </v-col>
  //-   </v-row>  
  //- </div>
  
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
    },
    media_url: {
      type: String,
      required: true
    },
    isFirstDate: {
      type: String,
      required: true
    }
  },

  computed: {
    contentRegexMatchURL: function() {
      let newContent = this.content;
      // eslint-disable-next-line
      /* eslint-disable-next-line */
      const urlRegex = /https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)/g;
      const matchURL = newContent.match(urlRegex);
      if (matchURL) {
        newContent = newContent.replace(urlRegex, `<a style="margin: 0 5px;" href="${matchURL[0]}" target="_blank">${matchURL[0]}</a>`);
      }
      return newContent;
    },
    alignmentClass() {
      // alert(this.is_carer_user);
      const isSuperUser = this.$root.userProfile?.super_user;
      if (isSuperUser) {
        return this.is_carer_user ? 'justify-end' : 'justify-start';
        // return this.is_carer_user ? 'justify-start' : 'justify-end';
      } else {
        return this.is_carer_user ? 'justify-start' : 'justify-end';
        // return this.is_carer_user ? 'justify-end' : 'justify-start';
      }
    },
    messageClass() {
      const isSuperUser = this.$root.userProfile?.super_user;
      if (isSuperUser) {
        return this.is_carer_user ? 'own-message' : 'other-message';
        // return this.is_carer_user ? 'other-message' : 'own-message';
      } else {
        return this.is_carer_user ? 'other-message' : 'own-message';
        // return this.is_carer_user ? 'own-message' : 'other-message';
      }
    }
  },

  watch: {

  },

}
</script>

<style scoped lang='scss'>
.col-auto{
  max-width: 75%;
  padding: 0;
}
.justify-start{
  .img_col{
    display: flex;
    justify-content: flex-start;
    padding-left: 0px;
  }
}
.justify-end{
  .img_col{
    display: flex;
    justify-content: flex-end;
    padding-right: 0px;
  }
}

.img_col .v-card{
  line-height: 0 !important;
}
.img_col img{
  max-height: 450px;
}
.v-card__text {
  padding: 10px 15px;
  overflow-wrap: break-word;
  word-wrap:break-word;
  word-break:break-all;
  line-height: 1.5;
}

.own-message {
  background-color: #000 !important;
  color: #fff;
  border-radius: 16px 16px 0 16px;
  margin: 5px 0;
  /* margin-right: 15px; */
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

.date-divider {
  color: #aaa;
}
img {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  // margin-top: 10px;
  cursor: pointer;
}
</style>
