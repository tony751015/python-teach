const { defineConfig } = require('@vue/cli-service')

console.log('Check-ENV: ', process.env);

module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],

  devServer: {
    open: true,
    host: process.env.VUE_APP_IP4,
    // host: '0.0.0.0',
    port: 3000,

    // https: {
    //   key: fs.readFileSync('./cert/localhost+2-key.pem'),
    //   cert: fs.readFileSync('./cert/localhost+2.pem'),
    // },
    // headers: {
    //   'Access-Control-Allow-Origin': '*',
    //   'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
    //   'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
    // }
  },
})

// module.exports = {
//   lintOnSave: false,
//   filenameHashing: false,
//   // publicPath: process.env.NODE_ENV === 'production' ? '/static/cms/' : '/',
//   publicPath: process.env.NODE_ENV === 'production' ? `${process.env.VUE_APP_GOOGLE_STORAGE_BUCKET}static/cms/` : '/',
//   pwa: {
//     disableWebAppManifestInjection: true,
//   },
//   css: {
//     sourceMap: true,
//     // requireModuleExtension: true,
//     // loaderOptions: {
//       // css: {
//       //   modules: {
//       //     localIdentName: process.env.NODE_ENV === 'production' ? '[hash:base64:5]' : '[local]',
//       //   },
//       // },
//       // sass: {
//       //   prependData: () => `$BaseUrl: '${process.env.NODE_ENV === 'production' ? '/static/' : '/'}';`,
//       // },
//     // },
//   },
//   devServer: {
//     open: true,
//     host: '127.0.0.1',
//     // host: '0.0.0.0',
//     port: 8080,

//     // https: {
//     //   key: fs.readFileSync('./cert/localhost+2-key.pem'),
//     //   cert: fs.readFileSync('./cert/localhost+2.pem'),
//     // },
//     // headers: {
//     //   'Access-Control-Allow-Origin': '*',
//     //   'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
//     //   'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
//     // }
//   },
//   // transpileDependencies: [
//   //   'vuetify'
//   // ]
// }
