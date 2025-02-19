<template>
	<view>
		<!-- 顶部导航 -->
		<view class="topBar">
			<view :class="[{'drugSearch':true},{'isHover':isHover}]" @click="showDrugSearch">药品查询</view>
			<view :class="[{'diagSearch':true},{'isHover':!isHover}]" @click="showDiagSearch">诊疗费用查询</view>
		</view>
		<!-- 搜索框 -->
		<view class="search" v-if="showDrug">
			<uni-search-bar placeholder="请输入药品名称" bgColor="#EEEEEE" @confirm="search"/>
		</view>
		<view class="search" v-if="!showDrug">
			<uni-search-bar placeholder="请输入诊疗名称" bgColor="#EEEEEE" @confirm="search"/>
		</view>
		<text class="results">搜索结果</text>
		<!-- 药品搜索结果 -->
		<view class="list" scroll-y="true" v-if="showDrug">
			<uni-list class="drug-list" v-for="(i,index) in druglist" :key="index">
				<view class="drug-item">
					<view class="name">
						<text class="title">药品名称</text>
						<text class="content">{{i['name']}}</text>
					</view>
					<view class="name">
						<text class="title">药品规格</text>
						<text class="content">{{i['specification']}}</text>
					</view>
					<view class="name">
						<text class="title">剂型</text>
						<text class="content">{{i['form']}}</text>
					</view>
					<view class="name">
						<text class="title">生产企业</text>
						<text class="content">{{i['enterprise']}}</text>
					</view>
					<view class="name">
						<text class="title">价格(元)</text>
						<text class="content">{{i['price']}}</text>
					</view>
				</view>
			</uni-list>
		</view>
		<!-- 诊疗费用搜索结果 -->
		<view class="list" scroll-y="true" v-if="!showDrug">
			<uni-list class="diag-list">
				<uni-list-item v-for="(i,index) in (diaglist)" :key="index" :title="i['dia_name']" :note="'价格(元)：'+i['price']"/>
			</uni-list>
		</view>
	</view>
</template>

<script>
	export default {
		data(){
			return {
				/* 搜索框值，true为药品 */
				showDrug:true,
				/* 导航选中样式，初始为药品查询 */
				isHover:true,
				/* 存放药品信息 */
				druglist:[],
				/* 存放诊疗费用信息 */
				diaglist:[]
			}
		},
		methods:{
			showDrugSearch(){
				// 导航样式和搜索框渲染
				this.isHover=true
				this.showDrug=true
				// 清空诊疗查询结果
				this.diaglist=''
			},
			showDiagSearch(){
				// 导航样式和搜索框渲染
				this.isHover=false
				this.showDrug=false
				// 清空药品查询结果
				this.druglist=''
			},
			// 搜索栏查询事件，根据this.showDrug判断是药品还是诊疗从发发送不同的请求
			search(res) {
				if(this.showDrug){
					console.log(res.value);
					if(res.value==''){
						uni.showToast({
							title:'值不能为空',
							icon:'error'
						})
					}else{
						// 向药品信息接口发送post请求，传的值为搜索框中value
						uni.request({
							url:'http://127.0.0.1:5000/api/drugs',
							method:'post',
							data:res,
							header:{
								'Content-Type':'application/json'
							},
							success: (data) => {
								// 将数据存入data中的药品信息列表，若无信息则showToast
								if((data.data.drugs.length)!=0){
									this.druglist=data.data.drugs
								}else{
									this.druglist=''
									uni.showToast({
										title: '暂无相关信息',
										icon: 'error'
									})
								}
							}
						})
					}
				}else{
					if(res.value==''){
						uni.showToast({
							title:'值不能为空',
							icon:'error'
						})
					}else{
						// 向诊疗费用接口发送post请求，传的值为搜索框中value
						uni.request({
							url:'http://127.0.0.1:5000/api/diagnosisFee',
							method:'post',
							data:res,
							header:{
								'Content-Type':'application/json'
							},
							success: (data) => {
								// 将数据存入data中的诊疗列表，若无信息则showToast
								if((data.data.dia_fee.length)!=0){
									this.diaglist=data.data.dia_fee
								}else{
									this.diaglist=''
									uni.showToast({
										title: '暂无相关信息',
										icon: 'error'
									})
								}
							}
						})
					}
				}
			},	
		}
	}
</script>

<style lang="scss">
	/* 顶部导航栏 */
	.topBar {
		position: fixed;
		display: flex;
		flex-direction: row;
		top: 0%;
		width: 100%;
		height: 80rpx;
		margin-bottom: 20rpx;
		background-color: white;
		align-items: center;
		justify-content: space-between; /* 两端对齐*/
		font-size: 14px;
		.drugSearch{
			margin-left: 100rpx;
			margin-right: 40rpx;
		}
		.diagSearch{
			margin-left: 40rpx;
			margin-right: 100rpx;
		}
	}
	.isHover{
		color: red;
		border-bottom: solid 1px red;
		font-weight: bold;
	}
	/* 搜索框 */
	.search {
		position: fixed;
		margin-top: 80rpx;
		top: 0%;
		width: 100%;
	}
	/* 搜索结果 */
	.results{
		position: fixed;
		margin-top: 220rpx;
		top: 0%;
		width: 100%;
		display: block;
		font-size: 14px;
		padding-left: 10rpx;
		border-left: 5px solid red;
		margin-left: 10rpx;
		margin-bottom: 30rpx;
	}
	.list{
		width: 100%;
		margin-top: 270rpx;
		overflow: auto;
		height: 900rpx;
	}
	/* 搜索药品结果 */
	.drug-list{
		display: flex;
		flex-direction: column;
		margin: 20rpx;	
	}
	.drug-item{
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		margin: 20rpx;
		font-size:14px;
		.name{
			display: flex;
			flex-direction: row;
			justify-content: center;
			margin-left: 10rpx;
			margin-top: 20rpx;
			margin-bottom: 20rpx;
			.title{
				display: block;
				width: 200rpx;
				color:gray;	
			}
			.content{
				display: block;
				margin:0 auto
			}
		}
	}
</style>