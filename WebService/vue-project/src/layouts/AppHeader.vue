<template>
	<div id="app-header">
		<router-link :to="{ name: 'UserMain' }">
			<div class="logo-container">
				<img :src="sejongLogo" />
				<span>회의실 예약 시스템</span>
			</div>
		</router-link>

		<div class="l-container">
			<!-- <router-link :to="{ name: 'MakeQuickReservation' }">
				<text-button color="white">빠른예약</text-button>
			</router-link> -->
			<template v-if="userIsLogin">
				<router-link :to="{ name: 'MakeReservation' }">
					<text-button color="white">예약하기</text-button>
				</router-link>
				<router-link :to="{ name: 'ReservationHistory' }">
					<text-button color="white">내 예약</text-button>
				</router-link>
				<router-link :to="{ name: 'AllReservationCalendar' }">
					<text-button color="white">모든예약</text-button>
				</router-link>
			</template>
		</div>

		<div class="r-container">
			<template v-if="userIsLogin">
				<router-link :to="{ name: 'UserMyPage' }" class="username-text">
					<text-button color="white">{{ userinfoString }}</text-button>
				</router-link>
				<div class="r-container-btns">
					<router-link
						v-if="userInfoStore.get().type === 1"
						:to="{ name: 'ManageMain' }"
					>
						<filled-button color="white">관리</filled-button>
					</router-link>
					<filled-button color="red" @click="handleLogout"
						>로그아웃</filled-button
					>
				</div>
			</template>
			<template v-else>
				<router-link :to="{ name: 'CheckAttendenceGateway' }">
					<text-button color="white">사용 인증하기</text-button>
				</router-link>
			</template>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

import sejongLogo from '@/assets/images/logo_white.png';
import TextButton from '@/components/atoms/TextButton.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import makeToast from '@/assets/scripts/utils/makeToast.js';

import { userService } from '@/assets/scripts/requests/request.js';
import { userInfoStore, userIsLogin, userTypeStr } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import { loadingStore } from '@/stores/loading.js';

// ----------------------------------

// 상태 ----------------------------------
const userinfoString = computed(() => {
	const { name } = userInfoStore.get();
	return `(${name} | ${userTypeStr.value})`;
});

// 초기화 ----------------------------
const router = useRouter();

// 이벤트 핸들러 ----------------------
async function handleLogout() {
	try {
		loadingStore.start();

		const res = await userService.logout(userTokenStore.getAccessToken());
		if (!res.status) {
			if (res.msg) throw new Error(res.msg);
			else throw new Error(res);
		}
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);

		if (msg === 'Token has been revoked') {
			makeToast('이미 로그아웃 되었습니다.', 'error');
		} else {
			makeToast('예기치 못한 오류가 발생했습니다.', 'error');
		}
	} finally {
		userInfoStore.clear();
		userTokenStore.clear();
		router.push({ name: 'Login' });
		loadingStore.stop();
	}
}
</script>

<style lang="scss" scoped>
#app-header {
	display: flex;
	align-items: center;

	// height: $header-height;
	padding: 24px 24px;
	color: white;
	background-color: $sejong-red;

	.logo-container,
	.l-container,
	.r-container {
		display: flex;

		align-items: center;

		.username-text {
			word-break: break-all;
		}
		.r-container-btns {
			display: flex;
		}
	}

	.logo-container {
		cursor: pointer;

		img {
			height: 42px;
			width: auto;
			margin-right: 12px;
		}
		span {
			color: white;
			font-size: 1.2rem;
		}
	}

	.l-container {
		margin: 0 12px;
	}

	.r-container {
		margin-left: auto;
	}
}

@media (max-width: 850px) {
	#app-header {
		flex-direction: column;
		padding: 24px 12px;

		.l-container {
			margin: 8px 0px;
		}
		.r-container {
			margin-left: 0;
		}
	}
}

@media (max-width: 320px) {
	#app-header {
		.r-container {
			flex-direction: column;
		}
	}
}
</style>
