<template>
	<div class="room-calendar">
		<div v-if="!isCalendarShown">
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
			<month-calendar v-if="calendarType === 'month'" :showRoomName="false" />
			<week-calendar v-if="calendarType === 'week'" />

			<filled-button color="white" @click="unshowCalendar">
				달력 닫기
			</filled-button>
		</template>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import MonthCalendar from '@/components/MonthCalendar.vue';
import WeekCalendar from '@/components/WeekCalendar.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';

const calendarType = ref('month'); // month, week

const isCalendarShown = ref(false);
function showCalendar() {
	isCalendarShown.value = true;
}
function unshowCalendar() {
	isCalendarShown.value = false;
}
</script>

<style lang="scss" scoped>
.room-calendar {
	width: fit-content;
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
