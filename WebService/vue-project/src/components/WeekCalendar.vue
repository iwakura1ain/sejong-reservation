<template>
	<div class="week-calendar">
		<div class="control-container">
			<div class="week-selector-container">
				<div
					class="week-btn prev-month noselect"
					@click="updateWeek(-1, 'month')"
				>
					{{ '<<' }}
				</div>
				<div
					class="week-btn prev-week noselect"
					@click="updateWeek(-1, 'week')"
				>
					{{ '<' }}
				</div>
				<div class="current-week-text">
					<span>{{ year }}년 {{ month }}월 </span>
					<span>{{ week }}주차</span>
				</div>
				<div class="week-btn next-week noselect" @click="updateWeek(1, 'week')">
					{{ '>' }}
				</div>
				<div
					class="week-btn next-month noselect"
					@click="updateWeek(1, 'month')"
				>
					{{ '>>' }}
				</div>
			</div>
		</div>

		<div class="week-calendar-innerwrap">
			<div class="header-container">
				<div class="header-cell sun">일</div>
				<div class="header-cell mon">월</div>
				<div class="header-cell tue">화</div>
				<div class="header-cell wed">수</div>
				<div class="header-cell thr">목</div>
				<div class="header-cell fri">금</div>
				<div class="header-cell sat">토</div>
			</div>

			<div class="body-container">
				<div
					v-for="(dayObj, index) in calendarArr[week - 1]"
					:key="index"
					class="day"
					:class="{ today: dayObj.dateStr === todayStr }"
				>
					<div
						v-if="dayObj.day !== 0"
						class="day-number"
						@click="selectDayNumber(dayObj.dateStr)"
					>
						{{ dayObj.day }}
					</div>
					<div v-if="dayObj.day !== 0" class="reservation-container">
						<div
							class="lines"
							style="width: 100%; position: relative; top: 0; left: 0"
						>
							<div
								class="timeline"
								v-for="index in Array.from({ length: 25 }, (v, i) => i)"
								:key="index"
								:style="`position:absolute; top:${
									(60 / minutePerPx) * index
								}px; width: 100%; border: 1px solid lightgrey`"
							></div>
						</div>

						<div
							class="blocks"
							style="
								width: 100%;
								position: relative;
								top: 0;
								left: 0;
								display: flex;
								justify-content: center;
							"
						>
							<div
								class="block"
								:class="{ single: item.type === 0, multi: item.type === 1 }"
								v-for="(item, index) in dayObj.reservations"
								:key="index"
								:style="`height:${getTimeBlockHeight(
									item.startTime,
									item.endTime,
								)}px; top:${getTimeBlockPosition(item.startTime)}px`"
							></div>

							<!-- 테스트 엘리먼트 -->
							<div
								class="block single"
								:style="`height:${getTimeBlockHeight(
									'06:00',
									'11:35',
								)}px; top:${getTimeBlockPosition('06:00')}px`"
							>
								<p>06:00</p>
								<p>-</p>
								<p>11:35</p>
							</div>
							<div
								class="block multi"
								:style="`height:${getTimeBlockHeight(
									'15:00',
									'22:11',
								)}px; top:${getTimeBlockPosition('15:00')}px`"
							>
								<p>15:00</p>
								<p>-</p>
								<p>22:11</p>
							</div>

							<!-- 테스트 엘리먼트 -->
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import getCalendarArray from '@/assets/scripts/getCalendarArray.js';
import getWeekNumber from '@/assets/scripts/getWeekNumber.js';

defineProps({
	showRoomName: {
		required: false,
		type: Boolean,
		default: true,
	},
});

const router = useRouter();

const minutePerPx = 3; // 표에서 높이 1픽셀당 3분을 나타냄.

const nowDateObj = new Date();
const now = {
	y: nowDateObj.getFullYear(),
	m: nowDateObj.getMonth() + 1,
	d: nowDateObj.getDate(),
};
now.w = getWeekNumber(now.y, now.m, now.d);

const formattedMonth = now.m < 10 ? `0${now.m}` : now.m;
const formattedDay = now.d < 10 ? `0${now.d}` : now.d;
const todayStr = `${now.y}-${formattedMonth}-${formattedDay}`;

const year = ref(now.y);
const month = ref(now.m);
const week = ref(now.w);

const calendarArr = computed(() => {
	console.log('hi', year.value, month.value);
	const arr = getCalendarArray(year.value, month.value);
	// reservations객체 주입
	// const thisMonthReservations = fetchedReservations.getThisMonth

	return arr;
});

const maxWeek = computed(() => {
	return calendarArr.value.length;
});

function getTimeBlockHeight(startTime, endTime) {
	// startTime 예시 ) "13:10"
	// endTime 예시 ) "17:53"
	const [st_h, st_m] = startTime.split(':');
	const startTimeAsMinute = parseInt(st_h) * 60 + parseInt(st_m);

	const [et_h, et_m] = endTime.split(':');
	const endTimeAsMinute = parseInt(et_h) * 60 + parseInt(et_m);

	const diffAsMinute = endTimeAsMinute - startTimeAsMinute;
	const blockPixelHeight = parseInt(diffAsMinute / minutePerPx);

	console.log(startTimeAsMinute, endTimeAsMinute, blockPixelHeight);
	return blockPixelHeight;
}

function getTimeBlockPosition(startTime) {
	// startTime 예시 ) "13:10"
	const [st_h, st_m] = startTime.split(':');
	const startTimeAsMinute = parseInt(st_h) * 60 + parseInt(st_m);
	const blockPixelPosition = parseInt(startTimeAsMinute / minutePerPx);
	console.log(blockPixelPosition);
	return blockPixelPosition;
}

// event handlers
function updateWeek(type, unit) {
	// type : -1이면 prev, 1이면 next
	if (unit === 'week') {
		week.value += type;
		if (week.value <= 0) {
			month.value -= 1;
			week.value = maxWeek.value;
		} else if (week.value > maxWeek.value) {
			month.value += 1;
			week.value = 1;
		}
	} else if (unit === 'month') {
		month.value += type;
	}

	if (month.value <= 0) {
		year.value -= 1;
		month.value = 12;
	} else if (month.value >= 13) {
		year.value += 1;
		month.value = 1;
	}
}

function selectDayNumber(dateStr) {
	alert(dateStr);

	router.push({
		name: 'MakeReservation',
		query: {
			startDateProp: dateStr,
		},
	});
}
</script>

<style lang="scss" scoped>
.week-calendar {
	$cell-min-width: 100px;

	width: 100%;

	color: $sejong-grey;
	.control-container {
		padding: 4px 0;
		border: 2px solid lightgrey;
		border-radius: $box-radius;
		margin-bottom: 8px;
		.week-selector-container {
			display: flex;
			justify-content: center;
			font-size: 1.2rem;
			padding: 8px 0;

			.week-btn,
			.current-week-text {
				text-align: center;
				min-width: 32px;
				background-color: white;
				transition: all 0.2s;
				padding: 8px 4px;
				border-radius: $box-radius;
				font-weight: bold;
			}

			.current-week-text {
				display: flex;
				justify-content: center;
				flex-wrap: wrap;
			}
			.prev-week,
			.prev-month {
				cursor: pointer;
				padding-left: 0;
			}
			.next-week,
			.next-month {
				cursor: pointer;
				padding-right: 0;
			}

			.week-btn:hover {
				filter: brightness(80%);
			}
		}
	}

	.week-calendar-innerwrap {
		overflow-x: auto;
		.header-container {
			display: flex;

			border-top-left-radius: $box-radius;
			border-top-right-radius: $box-radius;
			border: 1px solid lightgrey;
			border-bottom: none;

			.header-cell {
				flex: 1;
				display: flex;
				justify-content: center;
				// padding: 12px 4px;
				padding: 12px 0;
				border: 1px solid $sejong-red;
				background-color: $sejong-red;
				color: white;
				font-size: 1.2rem;

				min-width: $cell-min-width;
			}
		}
		.body-container {
			border-bottom-left-radius: $box-radius;
			border-bottom-right-radius: $box-radius;
			border: 1px solid lightgrey;
			border-top: none;
			display: flex;

			.day {
				flex: 1;
				border: 1px solid lightgrey;
				// padding: 0 2px;
				background-color: white;

				min-width: $cell-min-width;
				.day-number {
					padding: 4px;
					font-size: 1rem;
					background-color: white;
					text-align: center;
					transition: all 0.2s;
					cursor: pointer;
					&:hover {
						color: white;
						background-color: $sejong-red;
						&::after {
							font-size: 0.8rem;
							content: ' 예약';
						}
					}
				}
				.reservation-container {
					$miniute-per-px: 3;
					min-height: calc(calc(60 / ($miniute-per-px)) * 24px);

					// position: relative;

					.block {
						position: absolute;
						width: 80%;

						display: flex;
						flex-direction: column;
						justify-content: center;
						align-items: center;
						border-radius: $box-radius;
						font-size: 1rem;
					}
					@media (max-width: 450px) {
						.block {
							font-size: 0.75rem;
							width: 100%;
						}
					}
					.block.single {
						color: white;
						background-color: $sejong-grey-80;
					}
					.block.multi {
						background-color: #ffffff80;
						border: 2px solid $sejong-grey;
					}
				}
			}
			.today {
				.day-number {
					background-color: $sejong-red-30;
					color: $sejong-red;
					// &::after {
					// 	content: '(오늘)';
					// }
				}
			}
		}
	}
}
</style>
