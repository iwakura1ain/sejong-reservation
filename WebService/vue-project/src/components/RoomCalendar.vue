<template>
	<div class="room-calendar">
		<p style="font-size: 1.2rem; font-weight: bold; margin-bottom: 12px">
			{{ meetingRoomStr }}
		</p>
		<div v-if="!isOpened">
			<filled-button @click="showCalendar"> 예약현황 열기 </filled-button>
		</div>
		<template v-else>
			<div style="display: flex; align-items: center; flex-wrap: wrap">
				<div
					class="calendar-type-selector"
					style="margin: 0 0 2px 8px; height: 36px"
				>
					<radio-group
						v-model="calendarType"
						:buttons="[
							{ text: '월별 조회', value: 'month' },
							{ text: '주차별 조회', value: 'week' },
						]"
					/>
				</div>
				<text-button
					@click="unshowCalendar"
					style="margin: 0 0 0 auto; height: 36px; vertical-align: text-bottom"
				>
					예약현황 닫기
				</text-button>
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
			<div style="text-align: right">
				<text-button @click="unshowCalendar" style="margin-top: 0">
					예약현황 닫기
				</text-button>
			</div>
		</template>
	</div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import MonthCalendar from '@/components/MonthCalendar.vue';
import WeekCalendar from '@/components/WeekCalendar.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextButton from '@/components/atoms/TextButton.vue';
import { userTokenStore } from '@/stores/userToken.js';
import { reservationService } from '@/assets/scripts/requests/request.js';
import getLastDayInMonth from '@/assets/scripts/utils/getLastDayInMonth.js';
import formatDate from '@/assets/scripts/utils/formatDate.js';
import getWeekNumber from '@/assets/scripts/utils/getWeekNumber.js';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';

//
const props = defineProps({
	isOpened: {
		required: false,
		type: Boolean,
		default: false,
	},
	fetchTrigger: {
		required: true,
	},
	roomId: {
		required: true,
		type: Number,
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

// const roomData = computed(() => {
// 	return fetchedRoomStore.getById(id);
// });

const meetingRoomStr = computed(() => {
	if (props.roomId) {
		const { address1, address2, name } = fetchedRoomStore.getById(props.roomId);
		return `${address1} ${address2} ${name}`;
	} else {
		return '';
	}
});

// 초기화 ----------------------
init();

// 상태 감시 -------------------
watch(
	[targetDate, props.fetchTrigger],
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
			item => item.roomId === props.roomId,
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
