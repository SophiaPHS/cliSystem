<template>
	<view class="content">
		<uni-list>
			<uni-list-item showArrow style="line-height:80rpx;" title="头像" @click="upfile"  clickable>
				<template v-slot:footer>
					<image 
						class="slot-image image-size" 
						:src="avatarUrl"  
						mode="aspectFit" 
						avatarCircle='true'>
					</image>
				</template>
			</uni-list-item>
			<uni-list-item showArrow title="昵称" :rightText="userInfo.nickName"  @click="inputDialogToggle(userInfo.nickName)" clickable/>
			<uni-list-item title="账号" :rightText="userInfo.stuId"/>
			<uni-list-item showArrow title="密码" :rightText="pwdHide" @click="inputDialogToggle(userInfo.pwd)" clickable/>
		</uni-list>
		<!-- 弹出层修改昵称和密码 -->
		<view>
			<uni-popup ref="inputDialog" type="dialog">
				<uni-popup-dialog ref="inputClose"  mode="input" :title="currentTitle" :value="currentValue"
					 :placeholder="tip" @confirm="dialogInputConfirm"></uni-popup-dialog>
			</uni-popup>
		</view>
	</view>
</template>

<script>
	export default {
		data(){
			return {
				/* 用于标识修改弹窗内容 */
				flag:0,
				// 获取对应用户头像的接口地址
				avatarUrl:'http://127.0.0.1:5000/api/students/avatar/'+this.$store.state.userInfo.stuId+'.png'
			}
		},
		computed:{
			/* 获取store数据 */
			userInfo(){
				return this.$store.state.userInfo
			},
			/* 设置敏感信息-密码隐藏 */
			pwdHide(){
				return '····'
			},
			/* 设置弹框标题 */
			currentTitle(){
				return this.flag===0 ? '修改昵称' : '修改密码';
			},
			/* 设置弹框初始内容 */
			currentValue(){
				return this.flag===0 ? this.userInfo.nickName : this.userInfo.pwd;
			},
			/* 设置弹框内容提示 */
			tip:{
				get(){
					return this.flag==0 ? '请输入昵称' : '请输入密码';
				},
				set(value){
					if(value == ''){
						uni.showModal({
						    title: '提示',
						    content: '内容不能为空',
						    success: function (res) {
						        if (res.confirm) {
						            console.log('用户点击确定');
						        } else if (res.cancel) {
						            console.log('用户点击取消');
						        }
						    }
						});
					}
				}
			}
		},
		methods:{
			/* 点击出现弹窗修改内容 */
			inputDialogToggle(content) {
				if(content==this.userInfo.nickName){
					this.flag= 0
				}else if(content==this.userInfo.pwd){
					this.flag= 1
				}
				this.$refs.inputDialog.open()
			},
			/* 信息修改时间 */
			dialogInputConfirm(val) {
				/* 修改后信息加载 */
				uni.showLoading({
					title: '加载中'
				})
				setTimeout(() => {
					uni.hideLoading()
					if(val!=''){
						if(this.flag==0){
							if(val!=this.userInfo.nickName){
								// 更新store中用户昵称信息
								this.$store.commit('SET_USERINFO',{...this.$store.state.userInfo,nickName:val});
								// 向接口发送新数据
								this.$store.dispatch('updateUser',this.userInfo)
								uni.showToast({
									title:'修改成功'
								})
							}else{
								uni.showToast({
									title:'昵称未修改',
									icon:'error'
								})
							}
						}else {
							if(val!=this.userInfo.pwd){
								// 更新store中用户密码信息
								this.$store.commit('SET_USERINFO',{...this.$store.state.userInfo,pwd:val});
								// 向接口发送新数据
								this.$store.dispatch('updateUser',this.userInfo)
								uni.showToast({
									title:'修改成功'
								})
							}else{
								uni.showToast({
									title:'密码未修改',
									icon:'error'
								})
							}
						}
						
					}else {
						return this.tip=''
					}
					// 关闭窗口后，恢复默认内容
					this.$refs.inputDialog.close()
				}, 1000)
			},
			//上传头像
			upfile(){
				uni.chooseImage({ // 从本地相册选择图片或使用相机拍照。
					count: 1,//默认选择1张图片
					sizeType: ['compressed'],//original 原图，compressed 压缩图，默认二者都有
					success:  (res)=> {
						uni.uploadFile({//将本地资源上传到开发者服务器
							url:'http://127.0.0.1:5000/api/students/upAvatar', //接口地址
							filePath: res.tempFilePaths[0],//图片地址
							header:{
								'Content-Type':'multipart/form-data'
							},
							name: 'avatar',
							formData:{
								imageId:this.userInfo.stuId
							},
							success: (uploadFileRes) => {
								uni.request({
									url:uploadFileRes.data,
									success:() => {
										this.avatarUrl = uploadFileRes.data // 替换头像地址接口
										uni.$emit('upAvatar',this.avatarUrl) // 触发头像更新事件，并将新的地址传给上一级
									}
								})
							}
						});
					}
				});
			}
		},
	}
</script>

<style>
	.image-size{
		display: block;
		vertical-align: middle;
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
	} 
</style>