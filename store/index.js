// 页面路径：store/index.js 
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
// 引入http适配器
// import UniHttpAdapter from 'uni-request-adapter'

Vue.use(Vuex);//vue的插件机制
// 在vue原型上注册$http，这样可以全局使用
Vue.prototype.$http = axios


//Vuex.Store 构造器选项
const store = new Vuex.Store({
	// 用于存储数据——全局变量
	state:{//存放状态、
		userInfo:{},
		cardInfo:{},
		regInfo:[]
	},
	// 全局计算属性——用于将state中的数据进行加工
	getters:{
		
	},
	// 用于操作数据(state)——修改数据的方法
	mutations:{
		/* 用户信息存入、修改操作 */
		SET_USERINFO(state,payload){
			state.userInfo = payload
		},
		/* 就诊卡金额修改 */
		SET_CARDINFO(state,payload){
			state.cardInfo = payload
		},
		/* 添加挂号信息 */
		ADD_REGINFO(state,newObj){
			state.regInfo.push(newObj)
		},
		/* 修改挂号信息 */
		SET_REGINFO(state,payload){
			const item = state.regInfo.find(item => item.regId===payload.regId)
			item.isReg = payload.isReg
		},
		/* 删除挂号信息 */
		DEL_REGINFO(state){
			state.regInfo = []
		}
	},
	// 用于响应组件中的动作
	actions:{
		/* 向服务器发送更新的用户信息 */
		updateUser({commit},newUser){
			// 像服务器发送请求，更新用户信息
			return new Promise((resolve,reject)=>{
				axios({
					method:'post',
					url:'http://127.0.0.1:5000/api/students',
					data:newUser,
					headers:{
						'Content-Type':'application/json',
					},
				}).then(res=>{
					console.log('成功修改个人信息');
					
				}).catch(error=>{
					reject('修改个人信息失败')
				})
			})
		},
	}
})
export default store
