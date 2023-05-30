<template>
	<calendar-view
		:items="items"
		:itemTop="'1.4rem'"
		:itemContentHeight="'3.6rem'"
		:show-date="showDate"
		:displayPeriodUom="'month'"
		class="calendar-view-wrap theme-default"
	>
		<template #header="{ headerProps }">
			<calendar-view-header
				:header-props="{ ...headerProps, currentPeriodLabel: '현재' }"
				@input="setShowDate"
			/>
		</template>
	</calendar-view>
</template>
<!-- :itemTop="'1.4rem'"
		:itemContentHeight="'2.8rem'" -->
<script setup>
import { ref } from 'vue';
import { CalendarView, CalendarViewHeader } from 'vue-simple-calendar';
import '@/../node_modules/vue-simple-calendar/dist/style.css';
import '@/../node_modules/vue-simple-calendar/dist/css/default.css';

const props = defineProps({
	items: {
		type: Array,
		default() {
			return [
				{
					id: 'e10',
					startDate: '2023-05-19',
					title: 'Same day 6',
					classes: 'orange',
				},
				{
					id: 'e11',
					startDate: '2023-05-18',
					title: 'Same day 7',
				},
			];
		},
	},
});
const showDate = ref(new Date());
function setShowDate(d) {
	showDate.value = d;
}
</script>

<style lang="scss" scoped></style>

<style lang="scss">
.calendar-view-wrap {
	min-height: 512px;
	// overflow-y: visible;
	// .cv-day.past {
	// 	color: lightgrey;
	// 	filter: brightness(90%);
	// }
	.cv-day:hover {
		border: 1px solid blue;
	}
	.cv-day.outsideOfMonth {
		color: grey;
		filter: brightness(90%);
	}
	.cv-day.today {
		background-color: $sejong-red-30;
		border: 1px solid $sejong-red;
		color: $sejong-red;
		font-weight: bold;
	}
	.cv-item {
		text-overflow: clip;
		white-space: pre-wrap;
		word-break: keep-all;
		font-size: 0.8rem;
	}
	.cv-week {
		min-height: 150px;
	}

	// header
	.cv-header {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-direction: column-reverse;
		padding-bottom: 8px;
		background-color: white;
		.cv-header-nav {
			border-radius: $box-radius;
			border: 1px solid $sejong-grey;
			display: flex;
			justify-content: flex-end;
			button {
				color: black;
				transition: all 0.2s;
				cursor: pointer;
				border-radius: $box-radius;
				border: none;
				background-color: white;
			}
			button:hover {
				filter: brightness(80%);
			}
		}
		.periodLabel {
			margin: 0;
		}
	}
}

@media (max-width: 768px) {
	// header
	.cv-header {
		.periodLabel {
			margin: 0;
			padding: 4px;
		}
	}
	// .calendar-view-wrap .cv-item {
	// 	font-size: 0.7rem;
	// }
}

// @media (max-width: 768px) {
// 	.calendar-view-wrap .cv-item {
// 		font-size: 0.6rem;
// 	}
// }
</style>
