<template>
	<div id="user-main-view">
		<section-header>예정된 회의</section-header>
		<div class="reservation-card-container">
			<reservation-card
				v-for="item in reservationList"
				:key="item.id"
				:rsv-data="item"
				:room-data="fetchedRoomStore.getById(item.roomId)"
				:user-name="userInfoStore.get().name"
				@click="goDetailPage(item.id, item.reservationType)"
			/>
		</div>
	</div>
</template>

<script setup>
import { ref /*, watch*/ } from 'vue';
import { useRouter } from 'vue-router';

import SectionHeader from '@/components/atoms/SectionHeader.vue';
import ReservationCard from '@/components/atoms/ReservationCard.vue';
// import MonthCalendar from '@/components/MonthCalendar.vue';

import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { userInfoStore } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import { reservationService } from '@/assets/scripts/requests/request.js';
import getDateStringInThreeDays from '@/assets/scripts/utils/getDateStringInThreeDays';
import { loadingStore } from '@/stores/loading.js';

// 상태 ---------------------------------------
const reservationList = ref([]);

// 초기화 --------------------------------------
const router = useRouter();
init();
console.log(fetchedRoomStore);

// 일반 함수 -----------------------------------
async function fetchReservationsInThreeDays() {
	// 예정된 회의 (오늘, 내일, 모레의 내가 생성한 예약)를 불러오는 함수
	try {
		const { today, afterTomorrow } = getDateStringInThreeDays();
		const accessToken = userTokenStore.getAccessToken();
		await userInfoStore.setFromBackend(accessToken);
		const res = await reservationService.getMyFullData(
			{
				after: today,
				before: afterTomorrow,
				creator: userInfoStore.get().id,
			},
			accessToken,
		);

		if (!res.status) {
			throw new Error('INVALID_STATUS', res.status);
		}

		reservationList.value = res.data;
		console.log(reservationList.value);
	} catch (err) {
		alert('예약내역을 불러오는 중 문제가 생겼습니다.');
		console.error(err);
	}
}

async function init() {
	try {
		loadingStore.start();
		await fetchReservationsInThreeDays();
	} catch (err) {
		console.error(err);
	} finally {
		loadingStore.stop();
	}
}

// 이벤트 핸들러 ---------------------------------
function goDetailPage(id, reservationType) {
	console.log(id, reservationType);
	router.push({
		name: 'ReservationDetail',
		state: {
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
