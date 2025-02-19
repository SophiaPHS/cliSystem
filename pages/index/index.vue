<template>
		<view class="container">
			<!-- 顶部logo -->
			<view class="top">
				<img src="../../static/images/indexTitle.png" alt="">
			</view>
			<!-- 中间门诊服务 -->
			<view class="title">
				<uni-icons custom-prefix="iconfont" type="icon-menzhenfuwukaobei" size="15"></uni-icons>
				<text>门诊服务</text> 
			</view>
			<view class="middle">
				<view class="left">
					<view class="order" @click="regist">
						<text class="second-title">预约挂号</text>
					</view>
				</view>
				<view class="right">
					<view class="online">
						<text class="second-title" @click="develop()">远程问诊</text>
					</view>
					<view class="dibu">
						<view class="drugbuy"  @click="prescribe()">
							<text class="col-title">复诊开药</text>
						</view>
						<view class="pay"><text class="col-title" @click=pay()>在线缴费</text></view>
					</view>
				</view>
				<view class="bottom-content" @click="elReport()">
					<text class="ele-report">电子报告</text>
				</view>
			</view>
			<!-- 底部便民服务 -->
			<view class="title">
				<uni-icons custom-prefix="iconfont" type="icon-bianminfuwu" size="15"></uni-icons>
				<text>便民服务</text>
			</view>
			<view class="bottom">
				<view class="com_css info"  @click="introduce()">
					<img src="../../static/iconfont_png/yiyuanjieshao.png" alt="">
					<text class="bottom_title">医院介绍</text>
				</view>
				<view class="com_css serve route" @click="guide()">
					<img src="../../static/iconfont_png/daohang.png" alt="">
					<text class="bottom_title">院内导航</text>
				</view>
				<view class="com_css docInfo" @click="doctor">
					<img src="../../static/iconfont_png/yisheng.png" alt="">
					<text class="bottom_title">科室医生</text>
				</view>
				<view class="com_css sknow" @click="develop()">
					<img src="../../static/iconfont_png/zhishikepu.png" alt="">
					<text class="bottom_title">知识科普</text>
				</view>
				<view class="com_css query" @click="search">
					<img src="../../static/iconfont_png/chaxun.png" alt="">
					<text class="bottom_title">药品/诊疗查询</text>
				</view>
			</view>
		</view>
</template>

<script>
	export default {
		onShow() {
			// 判断是否登录账号，如果没有跳转至登录页面
			if(this.$store.state.userInfo.stuId==undefined){
				uni.showLoading({
					title: '加载中',
				});
				setTimeout(function(){
					uni.redirectTo({
						url:'/pages/user/login'
					})
				}, 1000)
				
			}
		},
		methods:{
			/* 进入预约挂号页面 */
			regist(){
				uni.navigateTo({
					url: 'guahao/registration'
				})
			},
			/* 进入复诊开药界面 */
			prescribe(){
				uni.navigateTo({
					url: 'prescribe'
				})
			},
			/* 进入在线缴费页面 */
			pay(){
				uni.navigateTo({
					url: 'pay'
				})
			},
			/* 进入电子报告页面 */
			elReport(){
				uni.navigateTo({
					url: 'ereport'
				})
			},
			/* 进入医院介绍页面 */
			introduce(){
				uni.request({
					url:'http://127.0.0.1:5000/api/introduce',
					success: (data) =>{
						let obj = JSON.stringify(data.data)
						uni.navigateTo({
							url:'introduce?obj='+encodeURIComponent(obj)
						})
					}
				})
			},
			/* 进入院内导诊界面 */
			guide(){
				uni.navigateTo({
					url:'hosGuide'
				})
			},
			/* 进入药品/诊疗费用查询页面 */
			search(){
				uni.navigateTo({
					url: 'search'
				})
			},
			/* 进入医生界面 */
			doctor(){
				uni.navigateTo({
					url:'doctor/doctor'
				})
			},
			/* 开发中模块 */
			develop(){
				uni.showLoading({
					title: '开发中'
				});
				setTimeout(function () {
					uni.hideLoading();
				}, 1000);
			}
			
			
		}
	}
</script>

<style lang="scss">
	.container {
		display: flex;
		flex-direction: column;
		font-size: 14px;
		line-height: 24px;
	}
	/* 头部设置 */
	.top {
		height: 250rpx;
		background: url('http://yiyuan.nchu.edu.cn/Content/yiyuan/Base/img/body.jpg') 50% 50% no-repeat;
	}
	.top > img{
		width: 400rpx;
		height: 100rpx;
		padding-left: 30rpx;
		padding-top: 100rpx;
	}
	/* 每一个标题模块的设置 */
	.title{
		height: 20rpx;
		font-size: 16px;
		text-align: left;
		font-weight: bolder;
		margin: 20rpx 30rpx;
		color: #389BFF;
	}
	/* 门诊服务样式 */
	.middle {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: center;  /*水平*/
		align-items: center; /*垂直*/
		margin-top: 20rpx;
		margin-bottom: 0rpx;
	}
	.middle > .left {
		display: flex;
		flex-direction: column;
	}
	.middle > .left > .order{
		width: 220rpx;
		height: 440rpx;
		margin: 10rpx 10rpx 10rpx 0rpx;
		border-radius: 60rpx;
		background: url('@/static/images/yuyueguahao.jpg') no-repeat;
		background-size: cover;
	}

	.middle > .right {
		display: flex;
		flex-direction: column;
	}
	.middle > .right > .online {
		width: 455rpx;
		height: 200rpx;
		margin: 10rpx 0rpx 10rpx 10rpx;
		border-radius: 60rpx;
		background: url('@/static/images/wenzhen.jpg') no-repeat;
		background-size: cover;
	}
	.middle > .right > .dibu {
		display: flex;
		flex-direction: row;
	}
	.middle > .right > .dibu > .drugbuy {
		width: 220rpx;
		height: 220rpx;
		margin: 10rpx;
		border-radius: 60rpx;
		background: url('@/static/images/kaiyao.png') no-repeat;
		background-size: cover;
		background-color: rgba(64, 224, 157,0.5);
	}
	.middle > .right > .dibu > .pay {
		width: 220rpx;
		height: 220rpx;
		margin: 10rpx 0rpx 10rpx 10rpx;
		border-radius: 60rpx;
		background: url('@/static/images/jiaofei.png') no-repeat;
		background-size: cover;
	}
	.middle > .bottom-content {
		width: 100%;
		height: 200rpx;
		margin: 10rpx 30rpx;
		border-radius: 60rpx;
		background:url('@/static/images/dianzibaogao.jpg') 0 50% no-repeat;
		background-size: cover;
		.ele-report {
			display: inline-block;
			margin-left: 40rpx;
			margin-top: 30rpx;
			font-weight: bold;
			font-size: 14px;
			letter-spacing: 2px; /* 控制字符间距*/
			writing-mode: vertical-rl; /* 使文字排版为竖排 */
		}
	}
	/* 里面文字内容设计样式 */
	.second-title {
		display: block;
		font-size: 14px;
		margin-left: 35rpx;
		margin-top: 20rpx;
		font-weight: bold;
	}
	.col-title {
		display: inline-block;
		margin-left: 60rpx;
		margin-top: 20rpx;
		font-weight: bold;
		font-size: 14px;
		width:20rpx;
		writing-mode: vertical-rl;
	}
	/* 便民服务样式 */
	.bottom {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		margin: 30rpx;
		border-radius: 60rpx;
		background-color: white;
		align-items: center;    /**子view垂直居中*/
		justify-content: center;
	}
	.bottom > .com_css {
		display: flex;
		flex-direction: column;
		width: 200rpx;
		height: 200rpx;
		margin: 10rpx 10rpx;
		justify-content: center; /**内容居中*/
	}
	.bottom >.com_css > img {
		display: block;
		width: 100rpx;
		height: 100rpx;
		margin: 0 auto;
		margin-top: 10rpx;
	}
	.bottom > .com_css > .bottom_title{
		display: block;
		font-size: 12px;
		text-align: center;
	}
	
</style>
