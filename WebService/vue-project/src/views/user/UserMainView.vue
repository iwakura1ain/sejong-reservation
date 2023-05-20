<template>
	<div id="user-main-view">
		<section-header>예정된 회의</section-header>
		<div class="reservation-card-container">
			<reservation-card
				v-for="item in reservations"
				:key="item.id"
				:rsv-data="item"
				:room-data="fetchedRoomStore.getById(item.roomId)"
			/>
		</div>

		<section-header>모든 예약 내역</section-header>
		<month-calendar />
	</div>
</template>

<script setup>
import { ref } from 'vue';

// import FilledButton from '@/components/atoms/FilledButton.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import ReservationCard from '@/components/atoms/ReservationCard.vue';
import MonthCalendar from '@/components/MonthCalendar.vue';

import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import {
	adminService,
	reservationService,
} from '@/assets/scripts/requests/request.js';

// 초기화 --------------------------------------
init();

// 상태 ----------------------------------------
const reservations = ref([]);

// 함수 ----------------------------------------
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

// 예정된 회의 (오늘, 내일, 모레의 내가 생성한 예약)를 불러오는 함수
async function fetchReservationsInThreeDays() {
	try {
		const res = await reservationService.get({
			mine: true,
		});
		if (res.status) {
			reservations.value = res.data;
		}
	} catch (err) {
		alert('예약내역을 불러오는 중 문제가 생겼습니다.');
		console.error(err);
	}
}

async function init() {
	await fetchRooms();
	await fetchReservationsInThreeDays();
}

// 이벤트 핸들러 ---------------------------------
//
</script>

<style lang="scss" scoped>
#user-main-view {
	.reservation-card-container {
		display: flex;
		justify-content: center;
		flex-wrap: wrap;
	}
}
</style>
