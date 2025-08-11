const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    hot: true,
    liveReload: true,
    watchFiles: {
      paths: ['src/**/*', 'public/**/*'],
      options: {
        usePolling: true,
        interval: 1000,
      },
    },
  },
  configureWebpack: {
    watchOptions: {
      poll: 1000,
      aggregateTimeout: 300,
      ignored: /node_modules/,
    }
  }
})