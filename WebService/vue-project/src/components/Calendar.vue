<template>
	<div class="calendar">
		<div class="calendar-nav-container">
			<div class="prev-year-btn"></div>
			<div class="prev-month-btn"></div>
			<div class="current-month"></div>
			<div class="next-month-btn"></div>
			<div class="next-year-btn"></div>
		</div>
		<div class="calendar-body-container"></div>
	</div>
</template>

<script setup>
const props = defineProps({
	interactionTarget: {
		// 상호작용할 대상이 무엇인지
		required: true,
		type: Number,
		default: 0, // 0:상호작용 없음(표시만), 1:날짜(셀)에 상호작용, 2:예약내역에 상호작용
	},
	year: {
		required: true,
		type: Number,
		default: 2023,
	},
	month: {
		required: true,
		type: Number,
		default: 5,
	},
	// reservations: {
	// 	requrired: true,
	// 	type: Array,
	// 	default() {
	// 		return [
	// 			{
	// 				id: -1,
	// 				regularId: -1,
	// 				date: '2023-05-01',
	// 				reservationType: 0,
	// 				meetingTime: {
	// 					start: { HH: '09', mm: '00' },
	// 					end: { HH: '10', mm: '30' },
	// 				},
	// 				roomId: -1,
	// 			},
	// 			{
	// 				id: -1,
	// 				regularId: -1,
	// 				date: '2023-05-03',
	// 				reservationType: 1,
	// 				meetingTime: {
	// 					start: { HH: '11', mm: '22' },
	// 					end: { HH: '22', mm: '33' },
	// 				},
	// 				roomId: -1,
	// 			},
	// 		];
	// 	},
	// },
});
</script>

<style lang="scss" scoped></style>
