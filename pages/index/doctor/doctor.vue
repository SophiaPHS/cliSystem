<template>
    <view>
		<!-- 搜索栏 -->
		<view class="search">
			<uni-search-bar placeholder="请输入科室或医生名称" bgColor="#EEEEEE" @confirm="search"/>
		</view>
		<!-- 导航栏 -->
		<scroll-view scroll-x="true" scroll-view-content='true'>
			<view class="grid-wrapper">
				<uni-grid :column="7" :highlight="true"  @change="change()">
					<uni-grid-item 
						v-for="(item, index) in departList" 
						:index="index" 
						:key="index"
						:style="[getStyle(index)]">
						<view class="grid-item-box">
							<text class="text">{{ item.text }}</text>
						</view >
					</uni-grid-item>
				</uni-grid>
			</view>
		</scroll-view>
		<!-- 医生列表 -->
		<DocInfo :docs='docs'/>
    </view>
</template>

<script>
	import DocInfo from 'components/docInfo.vue'
	export default {
		components:{DocInfo},
		data() {
			return {
				/* 宫格导航数据 */
				departList:[
					{text:'内科'},
					{text:'外科'},
					{text:'妇科'},
					{text:'全科'},
					{text:'口腔科'},
					{text:'影像科'},
					{text:'中医科'}
				],
				/* 选中索引 */
				selectedIndex:-1,
				/* 用于存放接口传来的数据 */
				docs:[],
			}
		},
		methods:{
			// 点击科室
			change(e){
				const index = e.detail.index
				this.selectedIndex=index
				/* 清空原先存储的医生信息 */
				if(this.docs){
					this.docs=[]
				}
				/* 根据科室向后台获取对应医生信息 */
				uni.request({
					url:'http://127.0.0.1:5000/api/doctors',
					method:'post',
					data:{
						depart:this.departList[e.detail.index].text
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
			// 选中科室的样式
			getStyle(index){
				if(this.selectedIndex===index){
					return {backgroundColor:'#c26100',color:'#fff'}
				}else{
					return {backgroundColor:'#F8F8F8',color:'#000'}
				}
			}
		}
	}
</script>

<style lang="scss">
	/* 搜索框 */
	.search{
		position: fixed;
		margin-top: 10rpx;
		padding: 0rpx;
		width: 100%;
	}
	/* 中间导航栏样式 */
	.grid-wrapper{
		position: fixed;
		margin-top: 150rpx;
		width: 900rpx;
		height: 150rpx;
		overflow-x: scroll;
		.grid-item-box {
			flex: 1;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			padding: 15px 0;
			.text{
				display: block;
				font-size: 15px;
				text-align: center;
			}
		}
	}
</style>