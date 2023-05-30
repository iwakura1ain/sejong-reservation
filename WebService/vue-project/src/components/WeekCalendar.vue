<template>
	<div class="week-calendar">
		<!-- 상단 컨트롤바 -->
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
					<span>{{ modelValue.year }}년 {{ modelValue.month }}월 </span>
					<span>{{ modelValue.week }}주차</span>
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

		<!-- 달력 -->
		<div class="week-calendar-innerwrap">
			<!-- 요일 표시 공간 -->
			<div class="header-container">
				<!-- 가로선별 시각표시 공간 헤더-->
				<div class="header-cell hour-tip"></div>
				<!-- 이하 요일별 헤더 -->
				<div class="header-cell sun">일</div>
				<div class="header-cell mon">월</div>
				<div class="header-cell tue">화</div>
				<div class="header-cell wed">수</div>
				<div class="header-cell thr">목</div>
				<div class="header-cell fri">금</div>
				<div class="header-cell sat">토</div>
			</div>

			<!--  -->
			<div class="body-container">
				<div class="day hour-tip">
					<div class="day-number hour-tip"></div>
					<div class="reservation-container hour-tip">
						<div
							class="lines hour-tip"
							style="width: 100%; position: relative; top: 0; left: 0"
						>
							<div
								class="timeline hour-tip"
								v-for="index in Array.from({ length: 24 }, (v, i) => i)"
								:key="index"
								:style="`position:absolute; top:${
									(60 / minutePerPx) * index - 6
								}px; width: 100%; font-size : 0.8rem; text-align:right; padding-right : 4px`"
							>
								{{ index }}
							</div>
						</div>
					</div>
				</div>

				<!-- 실제 예약내용 표시 -->
				<div
					v-for="(dayObj, index) in calendarArr[modelValue.week - 1]"
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
								v-for="index in Array.from({ length: 24 }, (v, i) => i)"
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
								:class="{
									single: item.reservationType === null,
									regular: item.reservationType !== null,
								}"
								v-for="(item, index) in dayObj.reservations"
								:key="index"
								:style="`height:${getTimeBlockHeight(
									item.meetingDatetime.startTime,
									item.meetingDatetime.endTime,
								)}px; top:${getTimeBlockPosition(
									item.meetingDatetime.startTime,
								)}px`"
								:title="`${item.meetingDatetime.startTime}-${item.meetingDatetime.endTime}`"
							>
								<p
									style="font-size: 0.75rem"
									v-if="
										getTimeBlockHeight(
											item.meetingDatetime.startTime,
											item.meetingDatetime.endTime,
										) > 16
									"
								>
									{{
										`${item.meetingDatetime.startTime}-${item.meetingDatetime.endTime}`
									}}
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- 하단 컨트롤바 -->
		<div class="control-container">
			<!-- 상단 컨트롤바 -->
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
					<span>{{ modelValue.year }}년 {{ modelValue.month }}월 </span>
					<span>{{ modelValue.week }}주차</span>
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
	</div>
</template>

<script setup>
import { unref, computed } from 'vue';
import { useRouter } from 'vue-router';
import getCalendarArray from '@/assets/scripts/utils/getCalendarArray.js';
import getWeekNumber from '@/assets/scripts/utils/getWeekNumber.js';

const props = defineProps({
	showRoomName: {
		required: false,
		type: Boolean,
		default: true,
	},
	reservationList: {
		required: false,
		type: Array,
	},
	modelValue: {
		required: false,
		type: Object,

		default() {
			const nowDateObj = new Date();
			const now = {
				year: nowDateObj.getFullYear(),
				month: nowDateObj.getMonth() + 1,
				day: nowDateObj.getDate(),
				week: getWeekNumber(
					`${nowDateObj.getFullYear()}-${
						nowDateObj.getMonth() + 1
					}-${nowDateObj.getDate()}`,
				),
			};
			return now;
		},
	},
});

const emits = defineEmits(['update:modelValue']);

// 초기화 ----------------------------
const router = useRouter();
const minutePerPx = 3; // 표에서 높이 1픽셀당 3분을 나타냄.

const formattedMonth =
	props.modelValue.month < 10
		? `0${props.modelValue.month}`
		: props.modelValue.month;
const formattedDay =
	props.modelValue.day < 10 ? `0${props.modelValue.day}` : props.modelValue.day;
const todayStr = `${props.modelValue.year}-${formattedMonth}-${formattedDay}`;

const calendarArr = computed(() => {
	const arr = getCalendarArray(props.modelValue.year, props.modelValue.month);
	// reservations객체 주입
	props.reservationList.forEach(rsv => {
		const dateObj = new Date(rsv.meetingDatetime.date);
		const weekNum = getWeekNumber(rsv.meetingDatetime.date);
		if (
			arr[weekNum - 1][dateObj.getDay()].dateStr === rsv.meetingDatetime.date
		) {
			arr[weekNum - 1][dateObj.getDay()].reservations.push(rsv);
		}
	});
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

	const minHeight = 5;
	return blockPixelHeight > minHeight ? blockPixelHeight : minHeight;
}

function getTimeBlockPosition(startTime) {
	// startTime 예시 ) "13:10"
	const [st_h, st_m] = startTime.split(':');
	const startTimeAsMinute = parseInt(st_h) * 60 + parseInt(st_m);
	const blockPixelPosition = parseInt(startTimeAsMinute / minutePerPx);

	return blockPixelPosition;
}

// event handlers
function updateWeek(type, unit) {
	// type : -1이면 prev, 1이면 next
	let _year = unref(props.modelValue.year);
	let _month = unref(props.modelValue.month);
	let _week = unref(props.modelValue.week);

	if (unit === 'week') {
		_week += type;
		if (_week <= 0) {
			_month -= 1;
			_week = maxWeek.value;
		} else if (_week > maxWeek.value) {
			_month += 1;
			_week = 1;
		}
	} else if (unit === 'month') {
		_month += type;
	}

	if (_month <= 0) {
		_year -= 1;
		_month = 12;
	} else if (_month >= 13) {
		_year += 1;
		_month = 1;
	}

	emits('update:modelValue', {
		...props.modelValue,
		year: _year,
		month: _month,
		day: props.modelValue.day,
		week: _week,
	});
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
		margin: 8px 0;
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
		border-radius: $box-radius;

		border: 2px solid lightgrey;
		background-color: $sejong-red;
		overflow-x: auto;
		.header-container {
			display: flex;

			// border-top-left-radius: $box-radius;
			// border-top-right-radius: $box-radius;
			// border: 1px solid lightgrey;
			border-bottom: none;
			// background-color: $sejong-red;
			.header-cell {
				flex: 1;
				display: flex;
				justify-content: center;
				// padding: 12px 4px;
				padding: 12px 0;
				// border: 1px solid $sejong-red;
				// background-color: $sejong-red;
				color: white;
				font-size: 1.2rem;

				min-width: $cell-min-width;
			}
			.hour-tip.header-cell {
				min-width: 32px;
				border: none;
			}
		}
		.body-container {
			border-bottom-left-radius: $box-radius;
			border-bottom-right-radius: $box-radius;
			// border: 1px solid red;
			// border-top: none;
			display: flex;

			.day {
				flex: 1;
				border-left: 2px solid lightgrey;

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
							// width: 100%;
						}
					}
					.block.single {
						color: white;
						background-color: $sejong-grey-80;
					}
					.block.regular {
						background-color: #ffffff80;
						border: 2px solid $sejong-grey;
					}
				}
			}

			.hour-tip.day {
				min-width: 32px;
				border: none;
				.day-number {
					min-height: 24px;
				}
			}

			.today {
				.day-number {
					background-color: $sejong-red-30;
					color: $sejong-red;
				}
			}
		}
	}
}
</style>
