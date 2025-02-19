<template>
	<view>
		<view class="index">
			<IndexHeader title="消息列表"></IndexHeader>
		</view>
		<img class="nomsg" src="@/static/iconfont_png/nomessage.png"/>
		<!-- <view  class="list" wx:for="i in msg" wx:key="i">
			<view class="list-item">
				<image src="@/static/uni.png" mode="" class="img"></image>
				<view class="info">
					<view class="info-top">
						<text class="info-title">预约通知</text>
						<text class="msg-time">时间</text>
					</view>
					<text class="msg">通知内容had使访客完不成崩溃了下差不多脆薯饼拆弹专家第三方包创造性地凤凰山卡拉dfhskjafdsakcxlk党副书记管道符VN发的爽肤水</text>
				</view>
			</view>
		</view> -->
	</view>
</template>

<script>
	import IndexHeader from '../../components/msgHeader.vue'
	export default {
		components:{IndexHeader},
		// data(){
		// 	return {
		// 		msg:['1','2','3','4','5','6','7','8']
		// 	}
		// }
	}
</script>

<style>
	.nomsg{
		display: block;
		margin-top: 100rpx;
	}
	.list > .list-item {
		display: flex;
		flex-direction: row;
		background-color: white;
		border-radius: 30rpx;
		margin: 20rpx 0rpx;
	}
	.list > .list-item > .img {
		width: 90rpx;
		height: 80rpx;
		margin: 30rpx ;
		
	}
	.list > .list-item > .info {
		display: flex;
		flex-direction: column;
	}
	.list > .list-item > .info > .info-top {
		display: flex;
		flex-direction: row;
		margin: 5rpx;
	}
	.list > .list-item > .info > .info-top > .info-title {
		display: block;
		margin-right: 300rpx;
		width: 200rpx;
		font-size: 14px;
		font-weight: bold;
	}
	.list > .list-item > .info > .info-top > .msg-time {
		display: block;
		margin-top: 10rpx;
		font-size: 12px;
		line-height: 10px;
	}
	.list > .list-item > .info > .msg {
		/*设置为弹性盒子*/
		display: -webkit-box;
		/* 表示几行后超出隐藏 */
		-webkit-line-clamp:2;
		/* 超出隐藏 */
		overflow:hidden;
		/*超出显示为省略号*/
		text-overflow:ellipsis;
		-webkit-box-orient:vertical;
		height: 80rpx;
		width: 600rpx;
		font-size: 12px;
		margin: 10rpx;
	}
</style>