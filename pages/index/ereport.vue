<template>
	<view class="content">
		<EReport :items='items'/>
	</view>
	
</template>

<script>
	import EReport from '@/components/segMented.vue'
	export default{
		components:{EReport},
		data(){
			return {
				items:['检验报告','检查报告']
			}
		}
	}
</script>

<style>
	.content{
		width: 100%;
		height: 100%;
	}
</style>