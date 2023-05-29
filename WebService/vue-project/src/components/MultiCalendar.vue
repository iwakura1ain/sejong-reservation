<template>
	<div class="multi-calendar">
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
		</div>

		<month-calendar
			v-if="calendarType === 'month'"
			v-model="localTargetDate"
			:reservation-list="reservationList"
			:showRoomName="true"
		/>
		<week-calendar
			v-if="calendarType === 'week'"
			v-model="localTargetDate"
			:reservation-list="reservationList"
			:showRoomName="false"
		/>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';
import MonthCalendar from '@/components/MonthCalendar.vue';
import WeekCalendar from '@/components/WeekCalendar.vue';
import RadioGroup from '@/components/RadioGroup.vue';

const props = defineProps({
	reservationList: {
		required: false,
		type: Array,
	},
	targetDate: {
		required: true,
		type: Object,
	},
});
const emits = defineEmits(['update:targetDate']);
const calendarType = ref('month'); // month, week
const localTargetDate = computed({
	get() {
		return props.targetDate;
	},
	set(newValue) {
		emits('update:targetDate', newValue);
	},
});
</script>

<style lang="scss" scoped>
.multi-calendar {
	// width: fit-content;
	width: 100%;
	// overflow-x: auto;
	// text-align: center;
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
