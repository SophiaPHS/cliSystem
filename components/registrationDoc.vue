<!-- 挂号模块中对应科室医生列表组件 -->
<template>
	<view>
		<view class="doc-list">
			<uni-list v-for="item in doc" :key="item.doc_id" >
				<uni-list-item :title="item.doc_name" showArrow clickable @click="detail(item.doc_id)"/>
			</uni-list>
		</view>
	</view>
	
</template>

<script>
	export default{
		props:['doc'],
		/* 解决使用 /deep/ 或者 ::v-deep 修改第三方组件不生效时 */
		options: {
		    styleIsolation: 'shared'
	    },
		methods:{
			/* 向后台获取对应医生所有值班情况并跳转至挂号详情页面 */
			detail(id){
				uni.request({
					url:'http://127.0.0.1:5000/api/doctor/duty',
					method:'post',
					data:{
						doc_id:id
					},
					header:{
						'Content-Type':'application/json'
					},
					success: (data) => {
						let obj = JSON.stringify(data.data)

						uni.navigateTo({
							/* 此处url是相对路径 pages/user/about就跳转不了了 */
							url:'/pages/index/guahao/dutyDetail?obj='+encodeURIComponent(obj)
						})
					}
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	/* 强制修改第三方样式 */
	/deep/ .uni-list-item{
		background-color: #F8F8F8;
	}
	/deep/ .uni-list-item--hover{
		background-color: #c3c3c3;
	}
</style>