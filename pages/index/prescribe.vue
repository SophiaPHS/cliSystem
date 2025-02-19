<template>
	<view>
		<!-- 挂号信息展示 -->
		<view class="duty_list" v-for="item in list" :key="item['duty_id']" v-show='isShow'>
			<view class="top_container">
				<img class="doc_photo" :src="baseUrl+item['doc_id']+'.png'">
				<view class="doc_info">
					<view class="info_top">
						<view class="doc_name">{{item['doc_name']}}</view>
						<view class="doc_post">{{item['doc_post']}}</view>
					</view>
					<view class="doc_skill">
						<text class="skill">{{item['doc_skill']}}</text>
					</view>
				</view>
			</view>
			<view class="divider"/>
			<view class="bottom">
				<view class="left">{{item['duty_time']}}&nbsp;&nbsp;{{item['duty_period']}}</view>
				<view class="middle">余号：{{item['reg_quantity']}}</view>
				<button class="right">￥{{item['duty_price']}}复诊</button>
			</view>
		</view>
		<view class="nothing" v-if="!isShow">
			<img src="@/static/iconfont_png/nothing.png" />
		</view>
	</view>
	
</template>

<script>
	export default{
		onLoad() {
			uni.request({
				url:'http://127.0.0.1:5000/api/doctor/getrecord',
				method:'post',
				data:{
					'user_id':this.$store.state.userInfo.stuId,
				},
				header:{
					'Content-Type':'application/json'
				},
				success: (data) => {
					let records = data.data.records
					if(data.data.records!='none'){
						for(let i=0;i<data.data.records.length;i++){
							uni.request({
								url:'http://127.0.0.1:5000/api/doctor/duty',
								method:'post',
								data:{
									'doc_id':data.data.records[i]['doc_id']
								},
								header:{
									'Content-Type':'application/json'
								},
								success: (data) => {
									let docDuty = data.data.dutys
									/* 获取当前时间 */
									let curDate = new Date()
									let curYear = curDate.getFullYear()
									let curMonth = curDate.getMonth()+1
									let curRi = curDate.getDate()
									let curTime = new Date(curYear+'-'+curMonth+'-'+curRi)
									for(let j=0;j<docDuty.length;j++){
										/* 获取医生值班时间 */
										let gmtDate = new Date(docDuty[j]['duty_time'])
										let gmtYear = gmtDate.getUTCFullYear()
										let gmtMonth = gmtDate.getUTCMonth()+1
										let gmtRi = gmtDate.getUTCDate()
										let gmtTime = new Date(gmtYear+'-'+gmtMonth+'-'+gmtRi)
										gmtRi.toString().padStart(2,'0')
										if(gmtTime>curTime){
											if(records[i]['doc_id']==docDuty[j]['doc_id']&&records[i]['duty_time']==docDuty[j]['duty_time']&&records[i]['duty_period']==docDuty[j]['duty_period']){
												continue
											}else{
												let duty = {
													duty_id:docDuty[j]['duty_id'],
													doc_id:docDuty[j]['doc_id'],
													doc_name:docDuty[j]['doc_name'],
													doc_post:docDuty[j]['doc_post'],
													doc_skill:docDuty[j]['doc_skill'],
													duty_period:docDuty[j]['duty_period'],
													duty_price:docDuty[j]['duty_price'],
													duty_time:gmtMonth+'.'+gmtRi,
													reg_quantity:docDuty[j]['reg_quantity']
												}
												this.list.push(duty)
											}
										}
									}
									if(this.list.length){
										this.isShow=true
									}else{
										this.isShow=false
									}
								}
							})
						}
					}else{
						this.isShow=false
					}
				}
			})
		},
		data(){
			return {
				list:[],
				isShow:false,
				baseUrl:'http://127.0.0.1:5000/api/doctors/photo/'
			}
		}
	}
</script>

<style lang="scss">
	/* 挂号列表样式 */
	.duty_list{
		display: flex;
		flex-direction: column;
		margin: 20rpx;
		border-radius: 5%;
		padding: 30rpx;
		background-color:white;
		.top_container{
			display: flex;
			flex-direction: row;
			margin: 0rpx;
			padding: 0rpx;
			.doc_photo{
				display: block;
				width: 120rpx;
				height: 150rpx;
				margin: 10rpx;
			}
		}
		.divider{
			background: #E0E3DA;
			height: 5rpx;
			margin: 20rpx 10rpx;
		}
		.bottom{
			display: flex;
			flex-direction: row;
			padding-left: 20rpx;
			margin-left: 120rpx;
			align-items: center;
			justify-content: center;
			.left{
				font-size: 12px;
				color:#389BFF
			}
			.middle{
				display: block;
				margin-left: 80rpx;
				font-size: 12px;
				color:#389BFF
			}
			.right{
				// width: 200rpx;
				height: 60rpx;
				padding-left: 10rpx;
				padding-right: 10rpx;
				margin-right: 0rpx;
				background-color: #389BFF;
				color: white;
				font-size: 12px;
				text-align: center;
				line-height: 23px;
			}
		}
	}
	.doc_info{
		display: flex;
		flex-direction: column;
		margin-left: 20rpx;
		.info_top{
			display: flex;
			flex-direction: row;
			align-items: center;
			.doc_post{
				margin-left: 20rpx;
				margin-top: 10rpx;
				font-size: 12px;
				color:gray;
			}
		}
		.doc_skill{
			margin-top: 20rpx;
			width: 450rpx;
			height: 80rpx;
			font-size: 12px;
			.skill{
				/*设置为弹性盒子*/
				display: -webkit-box;
				/* 表示几行后超出隐藏 */
				-webkit-line-clamp:2;
				/* 超出隐藏 */
				overflow:hidden;
				/*超出显示为省略号*/
				text-overflow:ellipsis;
				-webkit-box-orient:vertical;
			}
		}
	}
	/* 无挂号信息样式 */
	.nothing.image{
		display: block;
		margin: 0 auto;
		margin-top: 600rpx;
		height: 400rpx;
		width: 400rpx;
	}
</style>