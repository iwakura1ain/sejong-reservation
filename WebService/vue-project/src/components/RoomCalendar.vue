<template>
	<div class="room-calendar">
		<div class="calendar-type-selector">
			<radio-group
				v-model="calendarType"
				:buttons="[
					{ text: '월 조회', value: 'month' },
					{ text: '주차 주회', value: 'week' },
				]"
			/>
		</div>
		<month-calendar v-if="calendarType === 'month'" :showRoomName="false" />
		<week-calendar v-if="calendarType === 'week'" />
	</div>
</template>

<script setup>
import { ref } from 'vue';
import MonthCalendar from '@/components/MonthCalendar.vue';
import WeekCalendar from '@/components/WeekCalendar.vue';
import RadioGroup from '@/components/RadioGroup.vue';

const calendarType = ref('month'); // month, week
</script>

<style lang="scss" scoped>
.room-calendar {
	width: 100%;
	.calendar-type-selector {
		display: flex;
		justify-content: flex-end;
		margin-bottom: 8px;
	}
}
</style>
