<template>
	<div class="room-calendar">
		<div v-if="!isOpened">
			<filled-button @click="showCalendar"> 달력 열기 </filled-button>
		</div>
		<template v-else>
			<filled-button color="white" @click="unshowCalendar">
				달력 닫기
			</filled-button>

			<div class="calendar-type-selector">
				<radio-group
					v-model="calendarType"
					:buttons="[
						{ text: '월별 조회', value: 'month' },
						{ text: '주차별 조회', value: 'week' },
					]"
				/>
			</div>
			<month-calendar
				v-if="calendarType === 'month'"
				v-model="targetDate"
				:reservation-list="reservationList"
				:showRoomName="false"
			/>
			<week-calendar
				v-if="calendarType === 'week'"
				v-model="targetDate"
				:reservation-list="reservationList"
				:showRoomName="false"
			/>

			<filled-button color="white" @click="unshowCalendar">
				달력 닫기
			</filled-button>
		</template>
	</div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import MonthCalendar from '@/components/MonthCalendar.vue';
import WeekCalendar from '@/components/WeekCalendar.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import { userTokenStore } from '@/stores/userToken.js';
import { reservationService } from '@/assets/scripts/requests/request.js';
import getLastDayInMonth from '@/assets/scripts/utils/getLastDayInMonth.js';
import formatDate from '@/assets/scripts/utils/formatDate.js';
import getWeekNumber from '@/assets/scripts/utils/getWeekNumber.js';
import { makeRsvFormStore } from '@/stores/makeRsvForm.js';

//
defineProps({
	isOpened: {
		required: false,
		type: Boolean,
		default: false,
	},
});
const emits = defineEmits(['update:is-opened']);

// 상태, computed
const calendarType = ref('month'); // month, week

const nowDateObj = new Date();
const targetDate = ref({
	year: nowDateObj.getFullYear(),
	month: nowDateObj.getMonth() + 1,
	day: nowDateObj.getDate(),
	week: getWeekNumber(
		`${nowDateObj.getFullYear()}-${
			nowDateObj.getMonth() + 1
		}-${nowDateObj.getDate()}`,
	),
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
	[targetDate, makeRsvFormStore.common],
	() => {
		fetchReservationsInMonth();
	},
	{ deep: true },
);

// 일반함수 -------------------
async function fetchReservationsInMonth() {
	try {
		const accessToken = userTokenStore.getAccessToken();
		const res = await reservationService.get(
			{
				after: `${targetMonthInfo.value.firstDate}`,
				before: `${targetMonthInfo.value.lastDate}`,
			},
			accessToken,
		);

		if (!res.status) {
			throw new Error('INVALID_STATUS', res.status);
		}

		reservationList.value = res.data.filter(
			item => item.roomId === makeRsvFormStore.common.roomId,
		);
	} catch (err) {
		alert('예약내역을 불러오는 중 문제가 생겼습니다.');
		console.error(err);
	}
}

async function init() {
	await fetchReservationsInMonth();
}

// 이벤트 핸들러 --------------------
function showCalendar() {
	// isCalendarShown.value = true;
	emits('update:is-opened', true);
}
function unshowCalendar() {
	// isCalendarShown.value = false;
	emits('update:is-opened', false);
}
</script>

<style lang="scss" scoped>
.room-calendar {
	width: fit-content;
	// width: 100%;
	overflow-x: auto;
	text-align: center;
	.calendar-type-selector {
		display: flex;
		justify-content: center;
		margin-bottom: 8px;
	}
}

@media (max-width: 768px) {
	.room-calendar {
		width: 100%;
	}
}
</style>
