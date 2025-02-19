<template>
	<view>
		<uni-list>
			<uni-list-item 
				v-if="isShow"
				v-for="record in records"
				:key="record['reg_id']"
				:title="'坐诊医生：'+record['doc_name']" 
				:note="'挂号时间：'+record['duty_time']+' '+record['duty_period']" />
		</uni-list>
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
					'user_id':this.$store.state.userInfo.stuId
				},
				header:{
					'Content-Type':'application/json'
				},
				success:(data)=> {
					let regRecord = data.data.records
					if(regRecord!='none'){
						this.isShow=true
						for(let i=0;i<regRecord.length;i++){
							/* 获取医生值班时间 */
							let gmtDate = new Date(regRecord[i]['duty_time'])
							let gmtYear = gmtDate.getUTCFullYear()
							let gmtMonth = gmtDate.getUTCMonth()+1
							let gmtRi = gmtDate.getUTCDate().toString().padStart(2,'0')
							let gmtTime =gmtYear+'-'+gmtMonth+'-'+gmtRi
							let record = {
								reg_id:regRecord[i]['reg_id'],
								doc_name:regRecord[i]['doc_name'],
								duty_time:gmtTime,
								duty_period:regRecord[i]['duty_period']
							}
							this.records.push(record)
						}
					}else{
						this.isShow=false
					}
				}
			})
		},
		data(){
			return {
				isShow:false,
				records:[]
			}
		}
	}
</script>

<style>
</style>