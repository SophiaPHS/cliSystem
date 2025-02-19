<template>
	<view>
		<!-- 显示一周时间 -->
		<scroll-view scroll-x="true" scroll-view-content='true' show-scrollbar='false'>
			<view class="grid-wrapper">
				<uni-grid :column="7" :highlight="true"  @change="change()">
					<uni-grid-item 
						v-for="(item,index) in weekList"
						 :index="index"
						:key="index"
						:style="[getStyle(index)]">
						<view class="grid-item-box">
							<view class="grid-box">
								<text class="text" v-show='index==0'>今天</text>
								<text class="text" v-show='index!=0'>{{ item['weekDay']}}</text>
								<text class="text">{{ item['month'] }}.{{item['dayOfMonth']}}</text>
							</view>
						</view >
					</uni-grid-item>
				</uni-grid>
			</view>
		</scroll-view>
		<!-- 挂号信息展示 -->
		<view class="duty_list" v-for="item in dutyList" :key="item['duty_id']" v-show='isShow'>
			<view class="top_container">
				<img class="doc_photo" :src="baseUrl+item['doc_id']+'.png'">
				<view class="doc_info">
					<view class="info_top">
						<view class="doc_name">{{item['doc_name']}}</view>
						<view class="doc_post">{{item['doc_post']}}</view>
					</view>
					<view class="doc_skill">
						<text class="skill">{{item['doc_skill']}}</text>
						<view class="detail" @click="()=>docDetail(item['doc_id'])">[详情]</view>
					</view>
				</view>
			</view>
			<view class="divider"/>
			<view class="bottom">
				<view class="left">{{item['duty_time']}}&nbsp;&nbsp;{{item['duty_period']}}</view>
				<view class="middle">余号：{{item['reg_quantity']}}</view>
				<button class="right" v-if="isRegist(item['duty_id'])" @click="regist(item['duty_id'],item['reg_quantity'],item['duty_price'])">￥{{item['duty_price']}}挂号</button>
				<button class="right" v-if="!isRegist(item['duty_id'])" @click="quit(item['duty_id'],item['reg_quantity'])">取消挂号</button>
			</view>
		</view>
		<view class="nothing" v-if="!isShow">
			<img src="@/static/iconfont_png/nothing.png" />
		</view>
		<!-- 挂号窗口 -->
		<view>
			<uni-popup ref="regDialog" type="dialog">
				<uni-popup-dialog 
					cancelText="取消" 
					confirmText="确定" 
					title="提示" 
					:content="'当前余额为'+money+',是否挂号'" 
					@confirm="regConfirm()">
				</uni-popup-dialog>
			</uni-popup>
		</view>
		<!-- 取消挂号窗口 -->
		<view>
			<uni-popup ref="quitDialog" type="dialog">
				<uni-popup-dialog 
					cancelText="取消" 
					confirmText="确定" 
					title="提示" 
					content="是否取消挂号" 
					@confirm="quitConfirm()">
				</uni-popup-dialog>
			</uni-popup>
		</view>
	</view>
</template>

<script>
	export default{
		onLoad(options){
			// 接收上一个页面传递的数据并存放至当前data中
			let data = JSON.parse(decodeURIComponent(options.obj))
			this.docDuty=data.dutys
			// 获取当前年月日,并拼接成年-月-日
			let curDate = new Date()
			let curYear = curDate.getFullYear()
			let curMonth = curDate.getMonth()+1
			let curRi = curDate.getDate()
			let curTime = curYear+'-'+curMonth+'-'+curRi
			/* 判断医生值班情况是否有当日的，有的话就存入curDuty中 */
			for(let i=0;i<this.docDuty.length;i++){
				let gmtDate = new Date(this.docDuty[i]['duty_time'])
				let gmtYear = gmtDate.getUTCFullYear()
				let gmtMonth = gmtDate.getUTCMonth()+1
				let gmtRi = gmtDate.getUTCDate()
				let gmtTime = gmtYear+'-'+gmtMonth+'-'+gmtRi
				if(curTime==gmtTime){
					this.curDuty.push(this.docDuty[i])
				}
			}
			/* 如果初始页面有当日医生值班就展示值班信息 */
			if(this.curDuty.length!=0){
				this.isShow=true
			}
			/* 遍历一周的时间并存储至weekList中 */
			for(let i=0;i<7;i++){
				// 获取星期几
				let weekDay = curDate.getDay()
				let weekDayChina = '周'+['日','一','二','三','四','五','六'][weekDay]
				// 获取月份和日期
				let month = curDate.getMonth()+1
				let dayOfMonth = curDate.getDate().toString().padStart(2,'0')
				// 判断是否跨月
				if(dayOfMonth>new Date(curDate.getFullYear(),month,0).getDate()){
					dayOfMonth = 1
					month++
				}
				curDate.setDate(curDate.getDate()+1)
				let week = {
					'year':curYear,
					'month':month,
					'dayOfMonth':dayOfMonth,
					'weekDay':weekDayChina
				}
				this.weekList.push(week)
			}
			/* 页面加载时查询该用户是否挂号过，有的话把数据存入全局变量中 */
			/* uni.request({
				url:'http://127.0.0.1:5000/api/doctor/getrecord',
				method:'post',
				data:{
					'user_id':this.$store.state.userInfo.stuId,
				},
				header:{
					'Content-Type':'application/json'
				},
				success: (data) => {
					let regs = data.data.records
					if(data.data.records!='none'){
						for(let i=0;i<regs.length;i++){
							let regInfo={
								'regId':regs[i]['reg_id'],
								'isReg':true
							}
							this.$store.commit('ADD_REGINFO',regInfo)
						}
					}
				}
			}) */
		},
		data(){
			return {
				/* 存储医生图片根地址 */
				baseUrl:'http://127.0.0.1:5000/api/doctors/photo/',
				/* 选中某一时间索引 */
				selectedIndex:0,
				/* 存放上一页面传来的对应医生所有值班信息 */
				docDuty:[],
				// 存放当前时间的值班情况
				curDuty:[],
				// 存储一周内的日期和星期
				weekList:[],
				/* false展示无值班信息图片 */
				isShow:false,
				/* 监听是否可挂号，默认表示挂号前样式 */
				Regist:true,
				/* 给弹窗提供相应数据 */
				popupData:{}
			}
		},
		computed:{
			/* 从全局变量中获取就诊卡金额 */
			money(){
				return this.$store.state.cardInfo.money
			},
			/* 从全局变量中获取就诊卡id */
			cardId(){
				return this.$store.state.cardInfo.cardId
			},
			/* 从全局变量中获取当前用户所挂的号 */
			registed(){
				return this.$store.state.regInfo
			},
			/* 存放具体某天值班医生挂号情况列表 */
			dutyList(){
				if(this.curDuty.length==0){
					this.isShow=false
					return []
				}else{
					let list = []
					/* 根据是否今日值班进行相应逻辑处理 */
					for(let i=0;i<this.curDuty.length;i++){
						let curDate = new Date()
						let curTime = curDate.getFullYear()+'-'+(curDate.getMonth()+1)+'-'+curDate.getDate()
						let curHours = curDate.getHours()
						let gmtDate = new Date(this.curDuty[i]['duty_time'])
						let gmtMonth = gmtDate.getUTCMonth()+1
						let gmtRi = gmtDate.getUTCDate().toString().padStart(2,'0')
						let gmtTime = gmtDate.getUTCFullYear()+'-'+gmtMonth+'-'+gmtDate.getUTCDate()
						if(!(this.curDuty[i]['reg_quantity']==0&&this.Regist==false)){
							if(curTime==gmtTime){
								if(!(this.curDuty[i]['duty_period']=='上午'&&curHours>10)){
									if(!(this.curDuty[i]['duty_period']=='下午'&&curHours>16)){
										let duty = {
											duty_id:this.curDuty[i]['duty_id'],
											doc_id:this.curDuty[i]['doc_id'],
											doc_name:this.curDuty[i]['doc_name'],
											doc_post:this.curDuty[i]['doc_post'],
											doc_skill:this.curDuty[i]['doc_skill'],
											duty_period:this.curDuty[i]['duty_period'],
											duty_price:this.curDuty[i]['duty_price'],
											duty_time:gmtMonth+'.'+gmtRi,
											reg_quantity:this.curDuty[i]['reg_quantity']
										}
										list.push(duty)
									}
								}
							}else{
								let duty = {
									duty_id:this.curDuty[i]['duty_id'],
									doc_id:this.curDuty[i]['doc_id'],
									doc_name:this.curDuty[i]['doc_name'],
									doc_post:this.curDuty[i]['doc_post'],
									doc_skill:this.curDuty[i]['doc_skill'],
									duty_period:this.curDuty[i]['duty_period'],
									duty_price:this.curDuty[i]['duty_price'],
									duty_time:gmtMonth+'.'+gmtRi,
									reg_quantity:this.curDuty[i]['reg_quantity']
								}
								list.push(duty)
							}
							
						}
						
					}
					/* 依旧有无值班信息进行展示 */
					if(list.length!=0){
						this.isShow=true
						return list
					}else{
						this.isShow=false
						return []
					}
				}	
			}
		},
		methods:{
			/* 点击宫格事件 */
			change(e){
				const index = e.detail.index
				/* 不为今日挂号情况逻辑处理 */
				if(this.selectedIndex!=index){
					this.selectedIndex=index
					this.curDuty=[]
					let curTime = this.weekList[index]['year']+'-'+this.weekList[index]['month']+'-'+this.weekList[index]['dayOfMonth']
					for(let i=0;i<this.docDuty.length;i++){
						let gmtDate = new Date(this.docDuty[i]['duty_time'])
						let gmtYear = gmtDate.getUTCFullYear()
						let gmtMonth = gmtDate.getUTCMonth()+1
						let gmtRi = gmtDate.getUTCDate().toString().padStart(2,'0')
						let gmtTime = gmtYear+'-'+gmtMonth+'-'+gmtRi
						if(gmtTime===curTime){
							if(!(this.docDuty[i]['reg_quantity']==0&&this.Regist==false)){
								this.curDuty.push(this.docDuty[i])
							}
						}
					}
				}
			},
			// 选中时间的样式
			getStyle(index){
				if(this.selectedIndex===index){
					return {color:'#389BFF'}
				}
			},
			/* 查看医生详情 */
			docDetail(id){
				uni.request({
					url:'http://127.0.0.1:5000/api/doctors',
					method:'post',
					data:{
						'doc_id':id
					},
					header:{
						'Content-Type':'application/json'
					},
					success: (data) => {
						const datas = data.data.doctors
						let obj = JSON.stringify(datas[0])
						uni.navigateTo({
							url:'/pages/index/doctor/docDetail?obj='+encodeURIComponent(obj),
						})
					},
					error:(err)=>{
						console.log(err);
					}
				})
			},
			/* 挂号 or 取消挂号展示 true展示挂号 */
			isRegist(id){
				/* 初次判断全局变量中是否有挂号信息 */
				if(this.registed.length){
					for(let i=0;i<this.registed.length;i++){
						if(this.registed[i].isReg&&(id==this.registed[i].regId)){
							return false
						}
					}
				}
				/* 判断当前是否有挂号 */
				if(this.popupData.length){
					if(id==this.popupData.regid&&this.Regist==false){
						return false
					}
				}
				return true
			},
			/* 挂号操作 */
			regist(regid,count,regMoney){
				let isFull = this.money-regMoney
				if(isFull>=0){
					this.popupData={
						'regid':regid,
						'count':count,
						'Regist':true,
						'cardId':this.cardId,
						'cardMoney':this.money
					}
					this.$refs.regDialog.open()
				}else{
					uni.showToast({
						title:'余额不足',
						icon:'error'
					})
				}	
			},
			/* 挂号弹窗操作 */
			regConfirm(){
				this.Regist=false
				/* 修改就诊卡金额 */
				uni.request({
					url:'http://127.0.0.1:5000/api/doctor/regcount',
					method:'post',
					data:this.popupData,
					header:{
						'Content-Type':'application/json'
					},
					success: (data) => {
						// 更新store中就诊卡金额数据
						this.$store.commit('SET_CARDINFO',{...this.$store.state.cardInfo,money:data.data.cardMoney});
						if(this.docDuty.length){
							for(let i=0;i<this.docDuty.length;i++){
								if(this.popupData.regid==this.docDuty[i].duty_id){
									// 修改余号
									this.docDuty[i].reg_quantity-=1
									let record = {
										'reg_id':this.docDuty[i].duty_id,
										'user_id':this.$store.state.userInfo.stuId,
										'doc_id':this.docDuty[i].doc_id,
										'duty_time':this.docDuty[i].duty_time,
										'duty_period':this.docDuty[i].duty_period,
										'price':this.docDuty[i].duty_price,
										'isReg':true
									}
									/* 向后台发送对应挂号信息并添加至数据库中 */
									uni.request({
										url:'http://127.0.0.1:5000/api/doctor/regcord',
										method:'post',
										data:record,
										header:{
											'Content-Type':'application/json'
										}
									})
								}	
							}
						}
						/* 存放全局变量中的数据 */
						let regInfo={
							'regId':this.popupData.regid,
							'isReg':true
						}
						if(this.registed.length){
							/* 判断全局挂号信息中是否存在已挂号的情况如果有修改isReg，无继续添加*/
							for(let i=0;i<this.registed.length;i++){
								if(this.popupData.regid==this.registed[i].regId){
									if(this.registed[i].isReg==false){
										console.log(this.registed,regInfo);
										this.$store.commit('SET_REGINFO',regInfo)
										console.log('修改后：'+this.registed.length+this.registed);
										return 
									}else{
										return
									}	
								}
								if(i==this.registed.length-1){
									this.$store.commit('ADD_REGINFO',regInfo)
									return
								}
							}
						}else{
							/* 针对初始无全局挂号变量进行添加挂号操作 */
							this.$store.commit('ADD_REGINFO',regInfo)
						}
					}
				})
			},
			/* 取消挂号操作 */
			quit(id,count){
				this.popupData={
					'regid':id,
					'count':count,
					'Regist':false,
					'cardId':this.cardId,
					'cardMoney':this.money
				}
				this.$refs.quitDialog.open()
			},
			/* 取消挂号弹窗操作 */
			quitConfirm(){
				/* 在全局挂号变量中找到对应id处理isReg值，false表示取消挂号操作 */
				for(let i=0;i<this.registed.length;i++){
					console.log(i+"修改前："+this.registed[i].isReg);
					let regInfo={
						'regId':this.popupData.regid,
						'isReg':false,
					}
					this.$store.commit('SET_REGINFO',regInfo);
					console.log(i+"修改后："+this.registed[i].isReg);
					/* 存放全局变量中的数据 */
					
				}
				/* 修改就诊卡金额 */
				uni.request({
					url:'http://127.0.0.1:5000/api/doctor/regcount',
					method:'post',
					data:this.popupData,
					header:{
						'Content-Type':'application/json'
					},
					success: (data) => {
						this.Regist=true
						this.$store.commit('SET_CARDINFO',{...this.$store.state.cardInfo,money:data.data.cardMoney});
						if(this.docDuty.length){
							for(let i=0;i<this.docDuty.length;i++){
								if(this.popupData.regid==this.docDuty[i].duty_id){
									/* 修改余号 */
									this.docDuty[i].reg_quantity+=1
									let record = {
										'reg_id':this.docDuty[i].duty_id,
										'user_id':this.$store.state.userInfo.stuId,
										'doc_id':this.docDuty[i].doc_id,
										'duty_time':this.docDuty[i].duty_time,
										'duty_period':this.docDuty[i].duty_period,
										'price':this.docDuty[i].duty_price,
										'isReg':false
									}
									/* 向后台传入对应挂号信息进行删除操作 */
									uni.request({
										url:'http://127.0.0.1:5000/api/doctor/regcord',
										method:'post',
										data:record,
										header:{
											'Content-Type':'application/json'
										}
									})
								}
							}
						}
						
						
					}
				})
			},
		},
	}
</script>

<style lang="scss">
	/* 时间列表样式 */
	.grid-wrapper{
		width: 100vh;
		height: 150rpx;
		overflow-x: scroll;
		.grid-item-box {
			flex: 1;
			flex-direction: row;
			background-color: white;
		}
		.grid-box{
			display: flex;
			flex-direction:column;
			align-items: center;
			justify-content: center;
			margin: 0 auto;
			margin-top: 30rpx;
			.text{
				font-size: 14px;
				text-align: center;
			}
		}
	}
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
			.detail{
				margin: 0;
				padding: 0;
				color: #c26100;
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