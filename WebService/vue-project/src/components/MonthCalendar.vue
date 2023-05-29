<template>
	<div class="month-calendar">
		<!-- 상단 컨트롤 컨테이너 -->
		<div class="control-container">
			<div class="month-selector-container">
				<div
					class="month-btn prev-year noselect"
					@click="updateMonth(-1, 'year')"
				>
					{{ '<<' }}
				</div>
				<div
					class="month-btn prev-month noselect"
					@click="updateMonth(-1, 'month')"
				>
					{{ '<' }}
				</div>
				<div class="current-month-text">
					{{ modelValue.year }}년 {{ modelValue.month }}월
				</div>
				<div
					class="month-btn next-month noselect"
					@click="updateMonth(1, 'month')"
				>
					{{ '>' }}
				</div>
				<div
					class="month-btn next-year noselect"
					@click="updateMonth(1, 'year')"
				>
					{{ '>>' }}
				</div>
			</div>
		</div>

		<!-- 달력 본문 -->
		<div class="month-calendar-innerwrap">
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
				<div v-for="(week, index) in calendarArr" :key="index" class="week">
					<div
						v-for="(dayObj, index) in week"
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
								v-for="(item, index) in dayObj.reservations"
								:key="index"
								class="reservation"
								:class="{
									regular: item.reservationType,
									single: !item.reservationType,
								}"
								@click="selectReservation(item.reservationId)"
							>
								<p v-if="showRoomName">{{ getRoomDescString(item.roomId) }}</p>
								<p>
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

		<!-- 하단 컨트롤 컨테이너 -->
		<div class="control-container">
			<div class="month-selector-container">
				<div
					class="month-btn prev-year noselect"
					@click="updateMonth(-1, 'year')"
				>
					{{ '<<' }}
				</div>
				<div
					class="month-btn prev-month noselect"
					@click="updateMonth(-1, 'month')"
				>
					{{ '<' }}
				</div>
				<div class="current-month-text">
					{{ modelValue.year }}년 {{ modelValue.month }}월
				</div>
				<div
					class="month-btn next-month noselect"
					@click="updateMonth(1, 'month')"
				>
					{{ '>' }}
				</div>
				<div
					class="month-btn next-year noselect"
					@click="updateMonth(1, 'year')"
				>
					{{ '>>' }}
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, unref } from 'vue';
import { useRouter } from 'vue-router';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import getCalendarArray from '@/assets/scripts/utils/getCalendarArray.js';
import getWeekNumber from '@/assets/scripts/utils/getWeekNumber.js';
import getTodayZeroHour from '@/assets/scripts/utils/getTodayZeroHour.js';

// props, emits -------------------------
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
			};
			return now;
		},
	},
});

const emits = defineEmits(['update:modelValue']);

// state, computed
const calendarArr = computed(() => {
	const _year = props.modelValue.year;
	const _month = props.modelValue.month;
	const arr = getCalendarArray(_year, _month);

	// reservations객체 주입
	props.reservationList.forEach(rsv => {
		const dateObj = new Date(rsv.meetingDatetime.date);
		const weekNum = getWeekNumber(rsv.meetingDatetime.date);
		arr[weekNum - 1][dateObj.getDay()].reservations.push(rsv);
	});
	return arr;
});

// 초기화 -------------------------------------
const todayStr = getTodayZeroHour('STRING');
const router = useRouter();

// event handlers ----------------------
function updateMonth(type, unit) {
	let _year = unref(props.modelValue.year);
	let _month = unref(props.modelValue.month);

	// type : -1이면 prev, 1이면 next
	if (unit === 'month') {
		_month += type;
		if (_month <= 0) {
			_month = 12;
			_year -= 1;
		} else if (_month >= 13) {
			_month = 1;
			_year += 1;
		}
	} else if (unit === 'year') {
		_year += type;
	}

	emits('update:modelValue', {
		...props.modelValue,
		year: _year,
		month: _month,
		day: props.modelValue.day,
	});
}

// 일반 함수 -------------------------
function getRoomDescString(roomId) {
	const info = fetchedRoomStore.getById(roomId);
	return `${info.address1} ${info.address2} ${info.name}`;
}

// 이벤트 핸들러 ---------------------
function selectDayNumber(dateStr) {
	alert(dateStr);

	router.push({
		name: 'MakeReservation',
		query: {
			startDateProp: dateStr,
		},
	});
}

function selectReservation(reservationId) {
	alert(reservationId);
}
</script>

<style lang="scss" scoped>
.month-calendar {
	$cell-min-width: 100px;
	// width: 95vw;
	width: 100%;

	color: $sejong-grey;
	.control-container {
		padding: 4px 0;
		border: 2px solid lightgrey;
		border-radius: $box-radius;
		margin: 8px 0;
		.month-selector-container {
			display: flex;
			justify-content: center;
			font-size: 1.2rem;
			padding: 8px 0;
			.month-btn,
			.current-month-text {
				text-align: center;
				min-width: 32px;
				background-color: white;
				transition: all 0.2s;
				padding: 8px 4px;
				border-radius: $box-radius;
				font-weight: bold;
			}

			.prev-month,
			.prev-year {
				cursor: pointer;
				padding-left: 0;
			}
			.next-month,
			.next-year {
				cursor: pointer;
				padding-right: 0;
			}

			.month-btn:hover {
				filter: brightness(80%);
			}
		}
	}

	.month-calendar-innerwrap {
		overflow-x: auto;
		.header-container {
			display: flex;

			border-top-left-radius: $box-radius;
			border-top-right-radius: $box-radius;
			border: 1px solid lightgrey;
			border-bottom: none;
			border-top-left-radius: $box-radius;
			border-top-right-radius: $box-radius;

			.header-cell {
				flex: 1;
				display: flex;
				justify-content: center;
				padding: 12px 4px;
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
			.week {
				display: flex;
				.day {
					flex: 1;
					border: 1px solid lightgrey;
					padding: 0 2px;
					background-color: white;

					min-width: $cell-min-width;
					.day-number {
						padding: 4px;
						font-size: 1rem;
						background-color: white;
						transition: all 0.2s;
						cursor: pointer;
						&:hover {
							color: white;
							background-color: $sejong-red;
							&::after {
								content: '일 예약';
							}
						}
					}
					.reservation-container {
						min-height: 32px;
						.reservation {
							display: flex;
							flex-wrap: wrap;
							padding: 4px;
							margin: 4px 0;
							border-radius: $box-radius;
							cursor: pointer;
							p {
								font-size: 0.9rem;
								word-break: break-all;
							}

							&:hover {
								font-weight: bold;
								filter: brightness(70%) !important;
							}
						}
						.reservation.single {
							// color: ;
							color: white;
							background-color: $sejong-grey-80;
						}
						.reservation.regular {
							background-color: white;
							border: 1px solid $sejong-grey;
						}
					}
				}
				.today {
					background-color: $almost-sejong-red;
					transition: background-color 0.2s;
					.day-number {
						background-color: transparent;
						color: white;
						font-weight: bold;
					}
					&:hover {
						background-color: $sejong-red;
						// .day-number {
						// 	background-color: $sejong-red;
						// }
					}
				}
			}
		}
	}
}
</style>
