<template>
	<view class="content">
		<Pay :items='items'/>
	</view>
	
</template>

<script>
	import Pay from '@/components/segMented.vue'
	export default{
		components:{Pay},
		data(){
			return {
				items:['未支付','已支付']
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