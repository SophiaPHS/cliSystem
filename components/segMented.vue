<!-- 电子报告/在线缴费布局 -->
<template>
	<view>
		<view class="uni-padding-wrap uni-common-mt">
			<uni-segmented-control :current="current" :values="items" :style-type="styleType"
				:active-color="activeColor" @clickItem="onClickItem" />
		</view>
		<view class="list">
			<view class="content">
				<view v-if="current === 0"><img src="@/static/iconfont_png/fileNone.png"/></view>
				<view v-if="current === 1"><img src="@/static/iconfont_png/fileNone.png"/></view>
			</view>
		</view>
		
	</view>
</template>

<script>
	export default{
		props:['items'],
		data(){
			return{
				current: 0,
				activeColor: '#389BFF',
				styleType: 'button'
			}
		},
		methods:{
			onClickItem(e) {
				if (this.current !== e.currentIndex) {
					this.current = e.currentIndex
				}
			}
		}
	}
</script>

<style>
	.list{
		margin-left: 5%;
		margin-top: 20%;
	}
</style>