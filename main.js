
// #ifdef VUE2
import Vue from 'vue'
import App from './App'
import store from './store'
// import axios from 'axios'
// #ifdef MP-WEIXIN
// 引入适配器
import UniHttpAdapter from 'uni-request-adapter'
// #endif
Vue.config.productionTip = false
Vue.prototype.$store = store
// 为axios设置适配器，实现跨域请求
// #ifdef MP-WEIXIN
// 如果不加MP-WEIXIN，运行到chrome无法向后台发送post请求
Vue.prototype.$http.defaults.adapter = UniHttpAdapter
// #endif


// 设置vue调试工具
// Vue.config.devtools = true
// 使用axios
// Vue.prototype.$axios = axios

App.mpType = 'app'

const app = new Vue({
	store,
    ...App
})
app.$mount()
// #endif

// #ifdef VUE3
import { createSSRApp } from 'vue'
import App from './App.vue'
export function createApp() {
  const app = createSSRApp(App)
  return {
    app
  }
}
// #endif