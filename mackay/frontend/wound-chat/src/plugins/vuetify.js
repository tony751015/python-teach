import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

import zhHant from 'vuetify/lib/locale/zh-Hant';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    // options: { customProperties: true },
    themes: {
      light: {
        primary: '#66bb6a',
        secondary: '#424242',
        accent: '#8c9eff',
        error: '#d8374d',
        success: '#4CAF50',
        warning: '#da8200',

        'main-green': '#2D9CA0',
        'v-light': '#eee',
        'v-dark': '#242526',
        'v-dark2': '#161616',
        'color-1': '#d6545c',
        'color-2': '#f98068',
        'color-3': '#f0c158',
        'color-4': '#98cb69',
        'color-5': '#00b69e',
        'pain-1': '#00b69e',
        'pain-2': '#98cb69',
        'pain-3': '#f0c158',
        'pain-4': '#f98068',
        'pain-5': '#d6545c',

        'point-0': '#49954c',
        'point-1': '#fff',
        'point-2': '#f0c158',
        'point-3': '#d6545c',

        'level-4': '#f0c158',
        'level-5': '#d6545c',

        'level-reverse-2': '#f0c158',
        'level-reverse-1': '#d6545c',

        'record-basic': '#5580a0',
        'record-se': '#616eb7',
        'record-se1': '#616eb7',
        'record-se2': '#616eb7',
        'record-event': '#915c4c',
        'record-trail': '#49954c',
        'record-profile': '#ef6357',

        'real-reply': '#ffdd73',
      }
    },
  },
  lang: {
    locales: { zhHant },
    current: 'zhHant',
  },
});
