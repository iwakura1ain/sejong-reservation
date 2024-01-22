<template>
	<div class="datetime-availability-checker">
		<div class="item" v-for="(item, index) in targetDates" :key="index">
			<p>{{ item.dateString }}</p>
			<span v-if="item.available" style="color: green">✅예약가능</span>
			<span v-else style="color: $sejong-red">❌예약불가</span>
		</div>
	</div>
</template>

<script setup>
import { computed, watch } from 'vue';
import { REPEAT_END_TYPE } from '@/assets/constants.js';

import dayjs from 'dayjs';
import 'dayjs/locale/ko';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
import customParseFormat from 'dayjs/plugin/customParseFormat';
dayjs.locale('ko');
dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(customParseFormat);
dayjs.tz.setDefault('Asia/Seoul');

// states
import { datetimeAvailability } from '@/stores/reservation.js';

const props = defineProps({
	data: {
		required: true,
		type: Object,
		default() {
			return {
				repeatEndType: -1,
				startDate: new Date(),

				endReps: -1,
				endDate: new Date(),
			};
		},
	},
});
// const emits = defineEmits(['updateDatetimeAvailability']);

const targetDates = computed(computeTargetDates);
watch(
	targetDates,
	() => {
		datetimeAvailability.value = targetDates.value;
	},
	{ immediate: true },
);

function computeTargetDates() {
	console.log('hi');
	const { repeatEndType, startDate, endDate, endReps } = props.data;
	// console.log(reservationType, repeatEndType, startDate, endDate, endReps);

	// 현재 설정에 따라 사용자가 예약하기를 원하는 모든 날짜를 알아봅니다.
	const parsedStartDate = dayjs(startDate);
	const candidateDates = [];
	candidateDates.push(parsedStartDate);

	if (repeatEndType === REPEAT_END_TYPE.REPS) {
		for (let i = 1; i < endReps; i++) {
			candidateDates.push(parsedStartDate.add(i, 'week'));
		}
	} else if (repeatEndType === REPEAT_END_TYPE.DATE) {
		const parsedEndDate = dayjs(endDate);
		const diff = parsedEndDate.diff(parsedStartDate, 'week');

		for (let i = 1; i <= diff; i++) {
			candidateDates.push(parsedStartDate.add(i, 'week'));
		}
	}

	// console.log(candidateDates, repeatEndType, endReps);

	// 알아본 모든 날짜(candidateDates)중에서
	// 어떤 날짜가 예약 가능한지, 예약 불가능한지 검증합니다. (validatedDates)

	// -- 일단 다 된다고 가정
	// const validatedDates = [];
	const validatedDates = candidateDates.map(cand => {
		const obj = {
			year: cand.year(), // 년
			month: cand.month(), // 월
			day: cand.date(), // 일 (e.g., 1일, 2일, 3일, ...)
			dayofTheWeek: cand.day(), // 요일 (e.g., 월요일, 화요일, ...)
			dateString: cand.format('YYYY-MM-DD (dd)'),
		};
		// 여기서! 백엔드와 통신해서 이 예약 가능한지 확인 -------------
		return {
			...obj,
			available: true,
		};
	});

	return validatedDates;
}
</script>

<style lang="scss" scoped>
.datetime-availability-checker {
	padding: 8px;
	border: 1px solid $sejong-grey;
	border-radius: $box-radius;

	.item {
		display: flex;
		margin: 8px 0;
		> span {
			margin-left: 4px;
			font-weight: bold;
		}
	}
}

@media (max-width: 320px) {
	.datetime-availability-checher {
		font-size: 0.9rem;
	}
}
</style>
