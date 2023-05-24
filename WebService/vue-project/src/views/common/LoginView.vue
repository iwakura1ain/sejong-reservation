<template>
	<div id="login-view">
		<article class="logo-container">
			<img class="logoimg" :src="LogoImgRed" alt="sejong univ. logo" />
			<h1 class="logotext-ko">회의실 예약 시스템</h1>
			<h2 class="logotext-en">Meeting Room Reservation System</h2>
		</article>

		<form class="form-container">
			<div class="field-set">
				<span class="label">계정</span>
				<text-input v-model="id"></text-input>
			</div>
			<div class="field-set">
				<span class="label">비밀번호</span>
				<text-input type="password" v-model="pw"></text-input>
			</div>
			<div class="btn-group">
				<div>
					<router-link to="/register">
						<filled-button class="btn signup" color="white">
							가입하기
						</filled-button>
					</router-link>
				</div>
				<div>
					<filled-button class="btn signin" @click="handleLogin">
						로그인
					</filled-button>
				</div>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import LogoImgRed from '@/assets/images/logo_red.png';
import TextInput from '@/components/atoms/TextInput.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import { userService } from '@/assets/scripts/requests/request.js';
import { userInfoStore } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import { loadingStore } from '@/stores/loading.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

// 상태 -------------------------
const id = ref('');
const pw = ref('');

// 초기화 -----------------------
userInfoStore.clear();
userTokenStore.clear();
const router = useRouter();
if (history.state.failToAuth) {
	makeToast('사용자 인증에 문제가 있습니다', 'error');
}
if (history.state.userDeleted) {
	makeToast('정상적으로 탈퇴 처리되었습니다', 'info');
}

// 이벤트 핸들러 -----------------
async function handleLogin() {
	try {
		loadingStore.start();

		// 입력값 검증
		const req = {
			id: id.value,
			password: pw.value,
		};
		if (!req.id || !req.password) {
			makeToast('계정 또는 비밀번호가 비어있습니다.', 'warning');
			return;
		}
		if (req.password.length < 8) {
			makeToast('비밀번호는 8자 이상입니다', 'warning');
			return;
		}

		// 통신
		const res = await userService.login(req);
		if (!res.status) {
			if (res.msg) throw new Error(res.msg);
			else throw new Error(res);
		}

		// 완료
		userInfoStore.set(res.data);
		userTokenStore.set({
			accessToken: res.data.accessToken,
			refreshToken: res.data.refreshToken,
		});
		router.push({ name: 'UserMain' });
		// ------------------------------
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);

		if (msg === 'User Not Found') {
			makeToast('존재하지 않는 계정입니다.', 'error');
		} else if (msg === 'Wrong Password') {
			makeToast('비밀번호가 틀렸습니다.', 'error');
		} else if (msg === 'key:value pair wrong') {
			makeToast('입력한 내용의 형식이 올바르지 않습니다', 'error');
		} else {
			makeToast('예기치 못한 오류가 발생했습니다.', 'error');
		}
	} finally {
		loadingStore.stop();
	}
}
</script>

<style lang="scss" scoped>
#login-view {
	background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 1)),
		url(@/assets/images/login_bg.jpg) center;
	background-size: cover;

	.logo-container {
		text-align: center;
		font-weight: bold;
		.logoimg {
			width: 196px;
			height: 196px;
		}
		.logotext-ko {
			color: $sejong-grey;
			font-size: 2rem;
			margin: 8px 0;
		}
		.logotext-en {
			color: $sejong-red;
			font-size: 1rem;
		}
	}

	.form-container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: flex-end;
		background-color: white;
		padding: 24px;
		margin-top: 48px;
		border: 1px solid lightgrey;
		border-radius: $box-radius;

		.field-set {
			margin: 12px 0;
			text-align: right;
			.label {
				margin-right: 8px;
			}
		}

		.btn-group {
			display: flex;
			width: 100%;

			> div {
				flex: 1;
				margin: 4px 4px 0 4px;
			}
			.btn {
				// width: 98px;
				text-align: center;
				width: 100%;
			}
		}
	}
}

@media (max-width: 360px) {
	#login-view {
		.logo-container {
			transform: scale(0.6);
			.logotext-ko {
				font-size: 1.6rem;
			}
			.logotext-en {
				font-size: 0.85rem;
			}
		}

		.form-container {
			.field-set {
				display: flex;
				flex-direction: column;
				align-items: center;
				.label {
					margin-bottom: 4px;
				}
			}
			.btn-group {
				margin-top: 4px;
				transform: translateX(-4px);
			}
		}
	}
}
</style>
