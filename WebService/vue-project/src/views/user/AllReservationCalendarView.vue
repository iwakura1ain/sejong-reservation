<template>
	<div id="all-reservation-calendar-view">
		<section-header>모든 예약 살펴보기</section-header>
		<month-calendar
			v-model="targetDate"
			:reservation-list="reservationList"
			:show-room-name="true"
		/>
	</div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import MonthCalendar from '@/components/MonthCalendar.vue';
// import { userStore } from '@/stores/user.js';
import { reservationService } from '@/assets/scripts/requests/request.js';

import getLastDayInMonth from '@/assets/scripts/utils/getLastDayInMonth.js';
import formatDate from '@/assets/scripts/utils/formatDate.js';

// 상태, computed
const nowDateObj = new Date();
const targetDate = ref({
	year: nowDateObj.getFullYear(),
	month: nowDateObj.getMonth() + 1,
	day: nowDateObj.getDate(),
});
const targetMonthInfo = computed(() => {
	const { year, month } = targetDate.value;
	const lastDay = getLastDayInMonth(year, month);
	return {
		firstDate: formatDate(year, month, 0),
		lastDate: formatDate(year, month, lastDay),
	};
});

const reservationList = ref([]);

// 초기화 ----------------------
init();

// 상태 감시 -------------------
watch(
	targetDate,
	() => {
		console.log('hi');
		fetchReservationsInMonth();
		console.log(reservationList.value);
	},
	{ deep: true },
);

// 일반함수 -------------------
async function fetchReservationsInMonth() {
	try {
		const res = await reservationService.get({
			after: `${targetMonthInfo.value.firstDate}`,
			before: `${targetMonthInfo.value.lastDate}`,
		});

		if (!res.status) {
			throw new Error('INVALID_STATUS', res.status);
		}

		reservationList.value = res.data;
	} catch (err) {
		alert('예약내역을 불러오는 중 문제가 생겼습니다.');
		console.error(err);
	}
}

async function init() {
	await fetchReservationsInMonth();
}
</script>

<style lang="scss" scoped>
// #all-reservation-calendar-view {
// }
</style>
