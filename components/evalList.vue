<!-- 医生详情中评价列表组件 -->
<template>
	<view>
		<view class="list" v-for="item in evals" :key="item['eval_id']" v-if="evals!==''">
			<view class="user_info">
				<view class="nick_name">{{item['user_nick']}}</view>
				<view class="eval_time">{{item['eval_time']}}</view>
			</view>
			<view class="eval_con" >{{item['eval_con']}}</view>
		</view>
		<view class="nothing" v-if="evals==''">
			<img src="@/static/iconfont_png/nothing.png"/>
		</view>
	</view>
	
</template>

<script>
	export default{
		props:['evals'],
	}
</script>

<style lang="scss">
	.list{
		display: flex;
		flex-direction: column;
		margin: 0px;
		padding: 0px;
		background-color: white;
		border-bottom: 0.5px solid #d3d8d3;
		.user_info{
			display: flex;
			flex-direction: row;
			justify-content: space-between;
			align-items: center;
			margin:10rpx 30rpx;
			.nick_name{
				font-size: 12px;
			}
			.eval_time{
				font-size: 10px;
				color:gray;
			}
		}
		.eval_con{
			margin: 10rpx 30rpx;
			text-align: left;
			font-size: 12px;
		}
	}
	.nothing{
		margin: 0 auto;
		height: 400rpx;
		width: 400rpx;
		margin-right: 400rpx;
	}
</style>