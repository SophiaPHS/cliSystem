<template>
	<view>
		<!-- 医生信息 -->
		<view class="info">
			<DocInfo :detail='detail' :isTrue='true'/>
		</view>
		<!-- 是否开启用户评价 -->
		<view class="eval_change">
			<view class="eval">用户评价</view>
			<switch color='#389BFF' style="margin-right: 40rpx;" @change="switchChange" />
		</view>
		<!-- 评价列表 -->
		<scroll-view class="eval_list" v-if="isOpen" scroll-y="true">
			<EvalList :evals='evalList'/>
		</scroll-view>
		
		
		<!-- 输入评价 -->
		<view class="input_eval" v-if="isOpen">
			<input class="eval_content" v-model="inputData" placeholder="请输入评价内容"/>
			<img :src='submitIcon' class="eval_submit" @click="onSubmit"></img>
		</view>
	</view>
	
</template>

<script>
	import DocInfo from 'components/docInfo.vue'
	import EvalList from 'components/evalList.vue'
	export default{
		components:{DocInfo,EvalList},
		onLoad(options){
			// 接收上一个页面传递的数据
			let data = JSON.parse(decodeURIComponent(options.obj))
			// 使用setData方法将数据存入detail数组中
			this.detail=data
		},
		data(){
			return {
				/* 用于存放提交图标 */
				submitIcon:'/static/iconfont_png/tijiao.png',
				/* 用于存放单击上一页面某一医生列表对应的数据 */
				detail:[],
				/* 用于存放用户输入评价的内容 */
				inputData:'',
				/* 用于存放用户评价是否打开,初始值为false */
				isOpen:false,
				/* 用于存放评价列表 */
				evalList:[],
				/* 存放添加评价时的对象*/
				evalTodo:{}
			}
		},
		computed:{
			nickName(){
				return this.$store.state.userInfo.nickName
			},
			stuId(){
				return this.$store.state.userInfo.stuId
			},
			
		},
		methods:{
			/* 是否显示用户评价界面并展示评价内容 */
			switchChange(e){
				/* 根据switch的detail值控制列表是否展示，如果为true向后台请求数据 */
				this.isOpen = e.detail.value
				if(this.isOpen==true){
					uni.request({
						url:'http://127.0.0.1:5000/api/evaluation/select',
						method:'post',
						data:{
							doc_id:this.detail['doc_id']
						},
						header:{
							'Content-Type':'application/json'
						},
						success: (data) => {
							const datas = data.data.evaluations
							if(!this.evalList.length){
								for(let i=0;i<datas.length;i++){
									this.evalList.push(datas[i])
								}
							}else{
								let temList = JSON.stringify(this.evalList)
								let temdata = JSON.stringify(datas)
								// 防止数据重复
								if(!temList.includes(temdata)){
									this.evalList=[]
									for(let i=0;i<datas.length;i++){
										this.evalList.push(datas[i])
									}
								}
							}
						}
					})
				}
				
			},
			/* 添加评价事件 */
			onSubmit(){
				if(this.inputData===''){
					uni.showToast({
						title:'输入值不能为空',
						icon:'error'
					})
				}else{
					let date = new Date() // 获取当前时间
					let year = date.getFullYear()
					let month = (date.getMonth()+1)
					month = month.toString().padStart(2,'0') // 将月份转为为两位数并填充0，日同理
					let day = date.getDate()
					day = day.toString().padStart(2,'0')
					/* 向后台发送添加评价请求 */
					uni.request({
						url:'http://127.0.0.1:5000/api/evaluation/add',
						method:'post',
						data:{
							doc_id:this.detail['doc_id'],
							stu_id:this.stuId,
							eval_con:this.inputData,
							eval_time:year+'-'+month+'-'+day
						},
						header:{
							'Content-Type':'application/json'
						},
						success:(res)=>{
							/* 添加评价成功后清空输入框内容同时把评价加入列表中 */
							this.evalTodo={
								doc_id:this.detail['doc_id'],
								user_nick:this.nickName,
								eval_time:year+'.'+month+'.'+day,
								eval_con:this.inputData
							}
							this.evalList.push(this.evalTodo)
							this.evalList.sort((a,b)=>new Date(b.eval_time)-new Date(a.eval_time))
							this.inputData = '' // 清空评价输入框内容
						}
					})
				}
			}
		}
	}
</script>

<style lang="scss">
	/* 医生信息样式 */
	.info{
		width: 100vh;
		height: 220rpx;
	}
	/* 评价切换样式 */
	.eval_change{
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		height: 100rpx;
		background-color: white;
		border-top:0.5rpx solid #d3d8d3;
		border-bottom:0.5rpx solid #d3d8d3;
		.eval{
			margin-left: 40rpx;
		}
	}
	/* 评价列表 */
	.eval_list{
		width: 100%;
		height: 715rpx;
	}
	/* 底部评价 */
	.input_eval{
		position: fixed;
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: center;
        bottom: 0;
		left: 0;
		width: 80%;
		height: auto;
		margin:0 20rpx 1rpx 50rpx;
		padding: 30rpx 20rpx;
		border-radius: 20%;
		background-color: #fff;
		box-shadow: 0px -2px 5px #ccc;
		.eval_submit{
			display: block;
			width: 70rpx;
			height: 70rpx;
		}
	}
</style>