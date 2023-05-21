<template>
	<div id="user-main-view">
		<section-header>예정된 회의</section-header>
		<div class="reservation-card-container">
			<reservation-card
				v-for="item in reservations"
				:key="item.id"
				:rsv-data="item"
				:room-data="fetchedRoomStore.getById(item.roomId)"
				@click="goDetailPage(item.id, item.reservationType)"
			/>
		</div>

		<section-header>모든 예약 내역</section-header>
		<month-calendar />
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// import FilledButton from '@/components/atoms/FilledButton.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import ReservationCard from '@/components/atoms/ReservationCard.vue';
import MonthCalendar from '@/components/MonthCalendar.vue';

import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { reservationService } from '@/assets/scripts/requests/request.js';

// 초기화 --------------------------------------
const router = useRouter();
init();

// 상태 ----------------------------------------
const reservations = ref([]);

// 함수 ----------------------------------------

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
	await fetchReservationsInThreeDays();
}

// 이벤트 핸들러 ---------------------------------
function goDetailPage(id, reservationType) {
	console.log(id, reservationType);
	router.push({
		name: 'ReservationDetail',
		query: {
			id,
			reservationType,
		},
	});
}
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
