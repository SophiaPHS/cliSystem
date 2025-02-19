<!-- 消息页面顶部布局组件 -->
<template>
	<view class="header">
			<view class="title">
				{{title}}
			</view>
	</view>
</template>

<script>
	export default{
		props:['title'],
	}
</script>

<style lang="less">
	.header{
		position: relative;//注意，建议使用相对定位，因为固定定位会脱离文档流，然后你还要去设置marginTop值
		display: flex;
		align-items: center;
		height: 150rpx;  
		.title{
			text-align: left; 
			vertical-align: center;
			font-size: 40rpx;
			font-weight: bold;
			color: black;
			// margin: 0 auto; //使文字居中
			padding-top: 30px;
			padding-left: 10px;
		}  
	}
</style>