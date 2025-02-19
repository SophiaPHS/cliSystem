<!-- 用于医生模块布局组件 -->
<template>
	<view>
		<!-- 科室医生界面展示 -->
		<view class="list" v-if="!isTrue" scroll-y="true">
			<view
				class="doc-list" 
				v-for="(item) in docs" 
				:key="item['doc_id']" 
				@click="details(item)">
				<image class="doc_image" :src="baseUrl+item['doc_id']+'.png'" ></image>
				<view class="content">
					<view class="content_top">
						<view class="doc_name">{{item['doc_name']}}</view>
						<view class="doc_post">{{item['doc_post']}}</view>
					</view>
					<view class="content_bottom">
						<text class="note">{{item['doc_skill']}}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 医生详情界面展示 -->
		<view class="doc-list" v-if="isTrue">
			<image class="doc_image" :src="baseUrl+detail['doc_id']+'.png'" ></image>
			<view class="content">
				<view class="content_top">
					<view class="doc_name">{{detail['doc_name']}}</view>
					<view class="doc_post">{{detail['doc_post']}}</view>
					<view class="depart">{{detail['depart']}}</view>
				</view>
				<view class="content_bottom">
					<text class="note" type="primary" @click="toggle('center')">{{detail['doc_skill']}}</text>
				</view>
			</view>
		</view>
		<!-- 具体擅长治疗弹窗 -->
		<uni-popup ref="popup">
			<view class="popup-content">
				<text class="skill">擅长治疗</text>
				<text class="text">{{detail['doc_skill']}}</text>
			</view>
		</uni-popup>
	</view>
</template>

<script>
	export default{
		props:['docs','detail','isTrue'],
		data(){
			return {
				baseUrl:'http://127.0.0.1:5000/api/doctors/photo/'
			}
		},
		methods:{
			details(item){
				let obj = JSON.stringify(item)
				uni.navigateTo({
					url:'docDetail?obj='+encodeURIComponent(obj),
				})
			},
			/* 擅长治疗弹窗打开 */
			toggle(type) {
				this.$refs['popup'].open(type)
			},
			
		}
	}
</script>

<style lang="scss" scoped>
	/* 列表整体样式 */
	.list{
		overflow: auto;
		margin-top: 300rpx;
		height: 900rpx;
	}
	.doc-list{
		display: flex;
		flex-direction: row;
		margin-top: 20rpx;
		border-bottom: 1px solid #d3d8d3;
		height: 200rpx;
		background-color: white;
		/* 左侧照片 */
		.doc_image{
			display: block;
			width: 120rpx;
			height: 150rpx;
			margin: 30rpx;
		}
		/* 中间顶部内容 */
		.content{
			display: flex;
			flex-direction: column;
			width: 800rpx;
			height: 200rpx;
			margin-top: 20rpx;
		}
	}
	/* 中间顶部具体样式 */
	.content_top{
		display: flex;
		flex-direction: row;
		margin-top: 20rpx;
		width: 500rpx;
		height: 60rpx;
		padding: 0px;
		.doc_name{
			display: flex;
			flex-direction: row;
			align-items: center;
			text-align : left;
			padding: 0px;
			width: 100rpx;
			height: 40rpx;
			font-size: 14px;
			font-weight: bold;
		}
		.doc_post{
			display: flex;
			flex-direction: row;
			justify-content: center;
			align-items: center;
			font-size: 10px;
			color: #c26100;
			width: 130rpx;
			height:40rpx;
			margin-left: 20rpx;
			border: 1px solid #c26100;
		}
		.depart{
			display: flex;
			justify-content:center;
			align-items: right;
			font-size: 14px;
			margin-left: 150rpx;
			padding:0px;
			color: #d3d8d3;
		}
	}
	/* 中间底部内容 */
	.content_bottom{
		display: flex;
		flex-direction: column;
		margin-top: 10rpx;
		margin-bottom: 10rpx;
		width: 500rpx;
		height: 80rpx;
		font-size: 10px;
		.note{
			/*设置为弹性盒子*/
			display: -webkit-box;
			line-height: 160%;
			/* 表示几行后超出隐藏 */
			-webkit-line-clamp:2;
			/* 超出隐藏 */
			overflow:hidden;
			/*超出显示为省略号*/
			text-overflow:ellipsis;
			-webkit-box-orient:vertical;
		}
	}
	/* 提示层样式 */
	.popup-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		margin: 40rpx;
		padding: 15px;
		border-radius: 5%;
		background-color: #fff;
		.title{
			display: block;
			font-size: 14px;
			color:black;
			font-weight: bold;
			margin-top:30rpx;
			margin-bottom: 20rpx;
		}
		.text{
			display: inline-block;
			margin:20rpx 10rpx;
			font-size: 12px;
			text-align: left;
			text-indent:2em;
			color:black;
			
		}
	}
</style>