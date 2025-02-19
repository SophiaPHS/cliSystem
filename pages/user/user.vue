<template>
	<view class="container">
		<view class="navbar">
			<IndexHeader title="昌航校医院"></IndexHeader>
		</view>
		<!-- 头部个人用户信息 -->
		<view class="my-info">
			<view class="icon">
				<image :src="avatarUrl" @click="previewImage(avatarUrl)"></image>
			</view>
			<view class="person-info">
				<text class="name">{{userInfo.nickName}}</text>
				<text class="account">账号: {{userInfo.stuId}}</text>
			</view>
			<view class="right-arrow" @click="changeInfo">
				<uni-icons type="forward" size="30" color="white"></uni-icons>
			</view>
		</view>
		<!-- 就诊卡信息 -->
		<view class="card" @click="toggle('center')">
			<uni-icons custom-prefix="iconfont" type="icon-juminjiankangqia-" size="40"></uni-icons>
			<text class="card-info">就诊卡</text>
		</view>
		<!-- 就诊信息弹窗 -->
		<uni-popup ref="popup">
			<view class="popup-content">
				<view class="box">
					<text class="box-title">就诊卡id：</text>
					<text class="box-con">{{cardId}}</text>
				</view>
				<view class="box">
					<text class="box-title">就诊卡金额：</text>
					<text class="box-con">{{cardMoney}}元</text>
				</view>
				<button class="topup" @click="tip">充值</button>
			</view>
		</uni-popup>
		<!-- 就诊记录 -->
		<text class="title">就诊记录</text>
		<view class="record">
			<view class="com_css order" @click="records()">
				<img src="@/static/iconfont_png/guahaojilu.png" alt="">
				<text class="info-title">挂号记录</text>
			</view>
			<view class="com_css buy">
				<img src="@/static/iconfont_png/jiaofei.png" alt="">
				<text>缴费记录</text>
			</view>
			<view class="com_css medical-record">
				<img src="@/static/iconfont_png/baogao.png" alt="">
				<text class="info-title">我的报告</text>
			</view>
		</view>
		<!-- 更多服务 -->
		<text class="title">更多服务</text>
		<view class="more-serve">
			<uni-list>
				<uni-list-item 
					link="navigateTo"
					to="feedback"
					title="用户反馈"
				/>
				<uni-list-item 
					link="navigateTo"
					to="about"
					title="关于我们" 
				/>
				<uni-list-item 
					title="退出登录"  
					clickable
					showArrow 
					@click="quit"
				/>
			</uni-list>
		</view>
	</view>
</template>

<script>
	import IndexHeader from '../../components/userHeader.vue'
	export default {
		components:{IndexHeader},
		onShow(){
			/* 绑定头像更新事件 */
			uni.$on('upAvatar',(data)=>{
				this.avatarUrl = data
			})
		},
		onUnload() {
			uni.$off('upAvatar');//解除头像更新监听
		},
		data(){
			return {
				cardId:this.$store.state.cardInfo.cardId,
				// cardMoney:this.$store.state.cardInfo.money,
				headImg:require('static/images/touxiang.png'),
				avatarUrl:'http://127.0.0.1:5000/api/students/avatar/'+this.$store.state.userInfo.stuId+'.png'
			}
		},
		computed:{
			/* 获取store数据 */
			userInfo(){
				return this.$store.state.userInfo
			},
			cardMoney(){
				return this.$store.state.cardInfo.money
			}
		},
		methods:{
			/* 预览用户头像 */
			previewImage(imageUrl){
				uni.previewImage({
					urls:[imageUrl],  // 需要预览的图片地址列表
					current:imageUrl, // 当前显示的图片的链接
					indicator:'none', // 不显示顶部位置信息
				})
			},
			/* 跳转个人信息详情页面 */
			changeInfo(){
				uni.navigateTo({
					url: 'myInfo'
				})
			},
			/* 就诊卡信息弹窗打开 */
			toggle(type) {
				this.$refs['popup'].open('success')
			},
			/* 退出登录 */
			quit(){
				/* 清空所有全局变量并跳转至登录界面 */
				this.$store.commit('SET_USERINFO','')
				this.$store.commit('SET_CARDINFO','')
				this.$store.commit('DEL_REGINFO')
				uni.redirectTo({
					url:'/pages/user/login'
				})
			},
			/* 充值按钮点击 */
			tip(){
				uni.showToast({
					title:'未开通微商',
					icon:'error'
				})
			},
			/* 挂号记录详情 */
			records(){
				uni.navigateTo({
					url:'regRecord'
				})
			}
		},
	}
</script>

<style lang="scss">
	.container{
		font-size: 12px;
		line-height: 24px;
	}
	.title{
		display: block;
		font-size: 12px;
		font-weight: bold;
		margin: 20rpx;
	}
	.my-info {
		width: 100%;
		display: flex;
		flex-direction: row;
		background:-webkit-linear-gradient(left,white,lightblue,rgb(60, 157, 255));
	}
	.my-info > .icon {
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
		background: #d3d8d3;
		margin: 20rpx 30rpx;
	}
	.my-info > .icon > image {
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
	}
	.my-info > .person-info {
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
	.my-info > .person-info > .name {
		font-size: 16px;
		font-weight: bold;
		margin-bottom: 5rpx;
	}
	.my-info > .person-info > .account {
		font-size: 12px;
		margin-top: 5rpx;
		margin-left: 10rpx;
	}
	.my-info > .right-arrow {
		display: flex;
		margin-left: auto;
		margin-right: 20px;
		align-items: center;
	} 
	.card{
		display: flex;
		flex-direction: row;
		width: 100%;
		height: 100rpx;
		background-color: white;
		align-items: center; /*垂直居中 */
		justify-content: center;
	}
	.card > .card-info {
		display: block;
		margin-left: 5rpx;
	}
	.record{
		display: flex;
		flex-direction: row;
		width: 100%;
		background-color: white;
		justify-content: center; /**内容居中*/
		align-items: center; /* 垂直居中*/
	}
	.record > .com_css {
		display: flex;
		flex-direction: column;
		width: 200rpx;
		height: 200rpx;
		margin: 10rpx 10rpx;
		justify-content: center; /**内容居中*/
		align-items: center; /* 垂直居中 */
	}
	.record > .com_css > img {
		display: block;
		width: 80rpx;
		height: 80rpx;
		margin: 0 auto;
		margin-top: 10rpx;
	}
	.more-serve {
		background-color: white;
	}
	/* 弹窗层样式 */
	.popup-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		margin: 40rpx;
		padding: 15px;
		border-radius: 5%;
		background-color: #fff;
		.box{
			width: 400rpx;
			height: 50rpx;
			margin-bottom: 5rpx;
			text-align: left;
			.box-title{
				font-size: 14px;
				font-weight: bold;
			}
			.id-con{
				font-size: 12px;
			}
		}
		.topup{
			margin-top: 10rpx;
			margin-bottom: 10rpx;
			padding: 0;
			width: 120rpx;
			height: 100rpx;
			font-size: 14px;
		}
	}
</style>