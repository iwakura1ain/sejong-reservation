<template>
	<app-header :isLogin="userIsLogin" />
	<Transition appear>
		<router-view class="app-router-view"></router-view>
	</Transition>
	<app-footer> </app-footer>

	<loading-overay :loading="loadingStore.data" />
</template>

<script setup>
import { ref } from 'vue';
import AppHeader from '@/layouts/AppHeader.vue';
import AppFooter from '@/layouts/AppFooter.vue';
import LoadingOveray from '@/components/atoms/LoadingOveray.vue';

import { adminService } from '@/assets/scripts/requests/request.js';
import { userService } from '@/assets/scripts/requests/request.js';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { loadingStore } from '@/stores/loading.js';
import { userInfoStore, userIsLogin } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

// 상태 (state) -----------------------
//

// 초기화 -----------------------------
init();

// 일반 함수 --------------------------

async function fetchRooms() {
	// 모든 회의실을 불러오는 함수
	try {
		const res = await adminService.getAllRooms();
		if (res.status) {
			fetchedRoomStore.value.setAll(res.data);
			console.log('rooms are fetched', fetchedRoomStore.value);
		}
	} catch (err) {
		alert('회의실 목록을 불러오는 중 문제가 생겼습니다.');
		console.error(err);
	}
}

async function init() {
	await fetchRooms();

	// 저장된 토큰이 있으면 유저정보 가져오기
	try {
		if (!userTokenStore.exist()) {
			return;
		}

		// refresh auth하고 새로운 액세스토큰 가져와 저장하기
		// const refreshToken = userTokenStore.getRefreshToken();
		// const res = await userService.refreshAuth(refreshToken);
		// if (!res.status) {
		// 	throw new Error();
		// }
		// userTokenStore.set({
		// 	accessToken: res.data,
		// 	refreshToken,
		// });

		// 새로운 액세스토큰으로 유저 정보 가져오기
		const newAccessToken = userTokenStore.getAccessToken();
		const infoRes = await userService.getAuthInfo(newAccessToken);
		if (!infoRes.status) {
			throw new Error(infoRes);
		}
		userInfoStore.set(infoRes.data);
	} catch (err) {
		const msg = err.msg;
		console.error(err, msg);
		if (msg === 'Token has expired') {
			makeToast('로그인이 만료되었습니다', 'error');
		} else {
			makeToast('사용자 정보를 정상적으로 불러오지 못했습니다', 'error');
		}
	}
}
</script>

<style lang="scss" scoped>
.app-router-view {
	min-height: $routerview-minheight;

	display: flex;
	flex-direction: column;
	align-items: center;

	width: 100%;

	padding: $routerview-padding;
}
@media (max-width: 768px) {
	.app-router-view {
		padding: $routerview-mobile-padding;
	}
}
</style>

<style lang="scss">
.v-enter-active,
.v-leave-active {
	transition: opacity 1s ease;
}

.v-enter-from,
.v-leave-to {
	opacity: 0;
}
</style>
