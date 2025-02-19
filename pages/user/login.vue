<template>
	<view class="container">
		<text class="tip">{{tips}}</text>
		<!-- 登录表单 -->
		<view class="login-box">
			<uni-forms ref="valiForm" :modelValue="loginForm">
				<uni-forms-item name="userId">
					<uni-easyinput v-model="loginForm.userId" placeholder="请输入学号/工号" />
				</uni-forms-item>
				<uni-forms-item name="userPwd">
					<uni-easyinput  type="password" v-model="loginForm.userPwd" placeholder="请输入密码" />
				</uni-forms-item>
			</uni-forms>
			<button type="primary" size="mini" @click="submit('valiForm')">登录</button>
			<!-- 忘记密码 -->
			<view class="forget">忘记密码?</view>
		</view>
	</view>
</template>

<script>
import loginVue from './login.vue';
	export default {
		data(){
			return {
				// 顶部小贴士
				tips:'请输入您的学号/工号及密码进行绑定。若输入无误但未绑定成功，请与校医院分诊人员联系，或在校医院公众号留言，附一卡通等身份证明，管理员会尽快予以核实。',
				// 登录输入的表单
				loginForm:{
					userId:"",
					userPwd:""
				},
			}
		},
		methods:{
			/* 点击登录后向后台发送get请求进行账号校验，成功后将用户信息，就诊卡信息存入vuex中 */
			submit(ref){
				if((this.loginForm.userId=='') || (this.loginForm.userPwd=='')){
					uni.showToast({
						title: '信息不能为空',
						icon:'error'
					});
				}else{
					uni.request({
						url:'http://127.0.0.1:5000/api/students',
						header:{
							token:this.loginForm.userId
						},
						success: (res) => {
							if(res.data=='nothing'){
								uni.showToast({
									title: '用户不存在',
									icon:'error'
								});
							}else{
								let alluser = res.data
								let userInfo = alluser.students.students
								let cardInfo = alluser.card
								if(this.loginForm.userPwd==userInfo[0].pwd){
									this.$store.commit('SET_USERINFO',userInfo[0])
									this.$store.commit('SET_CARDINFO',cardInfo)
									uni.request({
										url:'http://127.0.0.1:5000/api/doctor/getrecord',
										method:'post',
										data:{
											'user_id':this.$store.state.userInfo.stuId,
										},
										header:{
											'Content-Type':'application/json'
										},
										success: (data) => {
											let regs = data.data.records
											if(data.data.records!='none'){
												for(let i=0;i<regs.length;i++){
													let regInfo={
														'regId':regs[i]['reg_id'],
														'isReg':true
													}
													this.$store.commit('ADD_REGINFO',regInfo)
												}
											}
										}
									}) 
									uni.switchTab({
										url:'/pages/index/index'
									})
								}else{
									uni.showToast({
										title: '密码错误',
										icon:'error'
									});
								}
							}
						}
					})
					
				}			
			}
		}
	}
</script>

<style lang="scss">
	.container {
		width: 100vw;
		height: 100vh;
		background: url('http://yiyuan.nchu.edu.cn/Content/yiyuan/Base/img/body.jpg') no-repeat;
		background-size: cover;
		.tip {
			display: block;
			padding:100rpx 20rpx;
			font-size: 12px;
			text-indent:2em;
			line-height: 18px;
		}
	}
	/* 登录的表单 */
	.container > .login-box {
		position: relative;
		top: 50rpx;
		margin: 0 40rpx;
		
		/* 登录按钮 */
		button{
			display: block;
			width: 400rpx;
			margin: 0 auto;
		}
		/* 忘记密码 */
		.forget{
			font-size: 12px;
			text-align: center;
			line-height: 100rpx;
			&:hover {
				color: #55aa00;
				text-decoration:underline; 
			}
		}
	}
</style>