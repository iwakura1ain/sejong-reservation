<template>
	<div class="meeting-datetime-selector">
		<p>{{ selectedRoom.buildingName }} {{ selectedRoom.roomName }}</p>
		<div>
			<span>일정 유형</span>
			<radio-group
				:buttons="[
					{ text: '단건예약', value: RESERVATION_TYPE.SINGLE },
					{ text: '정기예약', value: RESERVATION_TYPE.MULTI },
				]"
				v-model="reservationType"
			/>
		</div>

		<div>
			<span>예약 날짜</span>
			<vue3-datepicker-wrapper v-model="startDate" />
		</div>

		<div class="timepick-container">
			<span>예약 시간</span>
			<div class="can-be-newline">
				<vue3-timepicker-wrapper
					v-model="pickedTime.start"
					placeholder="시작하는 시각"
				/>

				<div>
					<span class="range-mark">~</span>
					<vue3-timepicker-wrapper
						v-model="pickedTime.end"
						placeholder="끝나는 시각"
					/>
				</div>
			</div>
		</div>

		<div
			v-if="reservationType === RESERVATION_TYPE.MULTI"
			class="repeat-end-container"
		>
			<span>종료 시점</span>
			<div class="can-be-newline">
				<radio-group
					:buttons="[
						{ text: '횟수', value: REPEAT_END_TYPE.REPS },
						{ text: '날짜', value: REPEAT_END_TYPE.DATE },
					]"
					v-model="repeatEndType"
					class="radio-group"
				/>

				<div v-if="repeatEndType === REPEAT_END_TYPE.REPS" class="repeat-value">
					<num-input
						v-model="endReps"
						:no-zero="true"
						:style="{ width: '64px', textAlign: 'center' }"
					/>
					<span>번 반복</span>
				</div>
				<div
					v-else-if="repeatEndType === REPEAT_END_TYPE.DATE"
					class="repeat-value"
				>
					<vue3-datepicker-wrapper v-model="endDate" />
					<span style="margin-left: 4px">까지</span>
				</div>
			</div>
		</div>

		<div v-if="datetimeIsPicked" style="align-items: flex-start">
			<span>확인 결과</span>
			<!-- <datetime-availability-checker
				@update-datetime-availability="updateDatetimeAvailability"
				:data="{ repeatEndType, startDate, endReps, endDate }"
			/> -->
			<datetime-availability-checker
				:data="{ repeatEndType, startDate, endReps, endDate }"
			/>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue';

import RadioGroup from '@/components/RadioGroup.vue';
import Vue3DatepickerWrapper from '@/components/wrappers/Vue3DatepickerWrapper.vue';
import Vue3TimepickerWrapper from '@/components/wrappers/Vue3TimepickerWrapper.vue';
import NumInput from '@/components/atoms/NumInput.vue';
import DatetimeAvailabilityChecker from '@/layouts/MakeReservation/DatetimeAvailabilityChecker.vue';

import { RESERVATION_TYPE, REPEAT_END_TYPE } from '@/assets/constants.js';

// states
import {
	reservationType,
	startDate,
	pickedTime,
	repeatEndType,
	endReps,
	endDate,
	// datetimeAvailability,
} from '@/stores/reservation.js';

// define props, events
defineProps({
	selectedRoom: {
		required: true,
		type: Object,
	},
});
defineEmits([]);

// [ states --> stores/reservation.js ]
// const reservationType = ref(RESERVATION_TYPE.SINGLE); // 일정 유형 (단건, 정기)
// const startDate = ref(getTodayZeroHour()); // 예약 날짜

// const pickedTime = ref({
// 	start: { HH: '', mm: '' },
// 	end: { HH: '', mm: '' },
// });

// const repeatEndType = ref(REPEAT_END_TYPE.REPS); // 종료시점 (횟수, 날짜)
// const endReps = ref(1); // 종료시점 - 횟수
// const endDate = ref(getTodayZeroHour()); // 종료시점 - 날짜

// const datetimeAvailability = ref([]); // 사용자가 예약하고자 하는 일시, 그 일시가 예약 가능한지 여부
// // │ 원소는 Object인데, 필드는 아래와 같음
// // │ {
// // │ 	year, month, day, : 년 월 일
// // │  dayofTheWeek : 요일(일요일 0, 토요일 6)
// // │  dateString : 'YYYY-MM-DD (dd)' 꼴 문자열
// // │ 	available : true 또는 false
// // └ }

const datetimeIsPicked = computed(() => {
	const { start, end } = pickedTime.value;
	return start.HH && start.mm && end.HH && end.mm && startDate.value;
});

// event handlers
// function updateDatetimeAvailability(arr) {
// 	datetimeAvailability.value = arr;
// }
</script>

<style lang="scss" scoped>
.meeting-datetime-selector {
	display: flex;
	flex-direction: column;

	p {
		font-size: 1.6rem;
		font-weight: bold;
	}

	> div {
		margin: 12px 0;
		display: flex;
		align-items: center;
		> span {
			margin-right: 8px;
		}
	}

	.timepick-container,
	.repeat-end-container {
		display: flex;
		flex-wrap: wrap;
		margin: 8px 0;

		.can-be-newline {
			display: flex;
			align-items: center;
			> * {
				margin: 4px 0;
			}

			/* timepick-container */
			.range-mark {
				font-size: 32px;
				vertical-align: bottom;
				color: $sejong-grey;
				margin: 0 4px;
			}

			/* repeat-end-container */
			> .radio-group {
				margin-right: 4px;
			}
			.repeat-value {
				display: flex;
				align-items: center;
			}
		}
	}
}

@media (max-width: 768px) {
	.can-be-newline {
		flex: 1;
		display: flex;
		flex-wrap: wrap;
	}
}

@media (max-width: 320px) {
	.meeting-datetime-selector {
		> div {
			flex-direction: column;
			align-items: flex-start;
			> span {
				margin-bottom: 4px;
			}
		}
	}
}
</style>
