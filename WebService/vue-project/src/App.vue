<template>
	<app-header :isLogin="true" :user-info="userinfo"> </app-header>
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
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { loadingStore } from '@/stores/loading.js';

// 초기화 -----------------------------
init();

// 상태 (state) -----------------------
// test data
const userinfo = ref({
	username: '이원진',
	email: '',
	level: '학부생',
	isAdmin: false,
	noShowCount: 0,
	isBanned: false,
});

// 일반 함수 --------------------------

// 모든 회의실을 불러오는 함수
async function fetchRooms() {
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
