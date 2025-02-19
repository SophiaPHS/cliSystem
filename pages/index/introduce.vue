<template>
	<view class="container">
		<view class="box">
			<view class="title">{{intro['title1']}}</view>
			<view class="content" v-for="(item,index) in intro['content1']" :key='index'>{{item}}</view>
		</view>
		<view class="box">
			<view class="title">{{intro['title2']}}</view>
			<view class="content" v-for="(item,index) in intro['content2']" :key='index'>{{item}}</view>
		</view>
		<view class="box">
			<view class="title">{{intro['title3']}}</view>
			<view class="content" v-for="(item,index) in intro['content3']" :key='index'>{{item}}</view>
		</view>
	</view>
</template>

<script>
	export default{
		onLoad(options){
			let data = JSON.parse(decodeURIComponent(options.obj))
			this.intro=data
			console.log(this.intro);
		},
		data(){
			return{
				intro:{}
			}
		}
	}
</script>

<style lang="scss">
	.container {
		background: url('http://yiyuan.nchu.edu.cn/Content/yiyuan/Base/img/body.jpg') no-repeat;
		background-size: cover;
	}
	.box{
		margin: 20rpx;
		display: flex;
		flex-direction: column;
		.title{
			display: flex;
			margin: 0 auto;
			margin-top: 10rpx;
			margin-bottom: 20rpx;
			font-size: 16px;
			font-weight: bold;
		}
		.content{
			font-size: 12px;
			text-indent: 2em;
		}
	}
	
</style>