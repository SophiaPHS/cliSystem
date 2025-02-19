<template>
	<view>
		<!-- 顶部搜索框 -->
		<view class="search">
			<uni-search-bar placeholder="搜索医生/科室" bgColor="#EEEEEE" @confirm="search" @focus="focus" @cancel="cancel"/>
		</view>
		<!-- 科室导航栏 -->
		<view class="list" v-show="isShow">
			<view class="region">
				<text class="region-title">科室</text>
			</view>
			<view class="whole-list">
				<uni-list class="department-list" >
					<uni-list-item 
						v-for="(item,index) in keshi" 
						:key='index'
						:title="item.title"
						:style="[getStyle(index)]"
						clickable
						@click="showdoc(item.title,index)"
					/>
				</uni-list>
				<!-- 对应科室的医生列表 -->
				<view class="content-list">
					<DepartDoc :doc='docs'/>
				</view>
			</view>
		</view>
			
		<!-- 点击搜索框时展示的内容 -->
		<view class="search-con" v-show="!isShow">
			
		</view>
	</view>
</template>

<script>
	import DepartDoc from 'components/registrationDoc.vue'
	export default {
		components:{DepartDoc},
		data(){
			return {
				/* 判断是科室展示还是搜索界面展示 */
				isShow:true,
				keshi:[
					{title:'内科'},
					{title:'外科'},
					{title:'妇科'},
					{title:'全科'},
					{title:'口腔科'},
					{title:'影像科'},
					{title:'中医科'}
				],
				/* 对科室绑定索引号点击后样式发生变化 */
				selectedIndex:-1,
				/* 用于存放对应科室医生列表信息 */
				docs:[]
			}
		},
		methods:{	
			/* 查询时提交发放事件 */
			search(res){
				console.log(res);
			},
			/* 搜索内容时隐藏科室 */
			focus(){
				this.isShow=false
			},
			/* 搜索内容时显示科室 */
			cancel(){
				this.isShow=true
			},
			/* 点击科室事件 */
			showdoc(keshi,index){
				this.selectedIndex=index
				/* 清空原先存储的医生信息 */
				if(this.docs){
					this.docs=[]
				}
				/* 向后台接口发送请求获取对应科室医生信息 */
				uni.request({
					url:'http://127.0.0.1:5000/api/doctors',
					method:'post',
					data:{
						depart:keshi
					},
					header:{
						'Content-Type':'application/json'
					},
					success: (data) => {
						const datas = data.data.doctors
						for(let i=0;i<datas.length;i++){
							this.docs.push(datas[i])
						}
					}
				})
			},
			/* 点击科室对应科室的样式设计 */
			getStyle(index){
				if(this.selectedIndex===index){
					return {fontWeight:'bold',borderLeft:'5px #389BFF solid'}
				}else{
					return {fontWeight:"normal"}
				}
			}
		},
	}
</script>
	
<style lang="scss" scoped>
	.region{
		width: 100%;
		margin-top: 30rpx;
		border-bottom: 1px solid gray;
		.region-title{
			display: block;
			width: 150rpx;
			line-height: 30px;
			margin-left: 30rpx;
			text-align: center;
			justify-content: center;
			vertical-align: center;
			font-size: 16px;
		}
	}
	.whole-list{
		width: 100%;
		display: flex;
		flex-direction: row;
		.department-list{
			margin-left: 30rpx;
			width: 400rpx;
			font-size: 16px;
			text-align: center;	
		}
		.content-list{
			width: 100%;
			margin-left: 40rpx;
			font-size: 14px;
		}
	}


</style>