<template>
	<view class="process">
		<text class="title">就诊流程图</text>
		<img class="imgUrl" :src="imgUrl" alt="就诊流程">
		
	</view>
</template>

<script>
	export default{
		data(){
			return{
				imgUrl:'https://yiyuan.nchu.edu.cn/Upload/yiyuan/ContentManage/Node/image/e9222b9b7e5a4cc39fda808ae3a4f1e4.jpg'
			}
		}
	}
</script>

<style lang="scss">
	.process{
		display: flex;
		flex-direction: column;
		margin: 20rpx;
		.title{
			display: block;
			margin: 0 auto;
			margin-bottom: 20rpx;
			font-size: 14px;
			font-weight: bold;
		}
	}
</style>