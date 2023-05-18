<template>
	<div class="month-calendar">
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
				<div class="current-month-text">{{ year }}년 {{ month }}월</div>
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
		<div class="month-calendar-innerwrap" v-hscroll>
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
								@click="selectReservation(item.reservationId)"
							>
								<!-- <p v-if="showRoomName">{{ item.topic }}</p>
								<p>{{ `${item.startTime}-${item.endTime}` }}</p> -->
							</div>
							<div class="reservation single">
								<p v-if="showRoomName">대양AI센터 835aaa호</p>
								<p>19:00-15:00</p>
							</div>
							<div class="reservation multi">
								<p v-if="showRoomName">대양AI센터 835호</p>
								<p>19:00-15:00</p>
							</div>
							<div class="reservation multi">
								<p v-if="showRoomName">대asdfsadfsfasadf호</p>
								<p>19:00-15:00</p>
							</div>
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

defineProps({
	showRoomName: {
		required: false,
		type: Boolean,
		default: true,
	},
});

const router = useRouter();

const nowDateObj = new Date();
const now = {
	y: nowDateObj.getFullYear(),
	m: nowDateObj.getMonth() + 1,
	d: nowDateObj.getDate(),
};
const formattedMonth = now.m < 10 ? `0${now.m}` : now.m;
const formattedDay = now.d < 10 ? `0${now.d}` : now.d;
const todayStr = `${now.y}-${formattedMonth}-${formattedDay}`;

const year = ref(now.y);
const month = ref(now.m);
function updateMonth(type, unit) {
	// type : -1이면 prev, 1이면 next
	if (unit === 'month') {
		month.value += type;
		if (month.value <= 0) {
			month.value = 12;
			year.value -= 1;
		} else if (month.value >= 13) {
			month.value = 1;
			year.value += 1;
		}
	} else if (unit === 'year') {
		year.value += type;
	}
}

const calendarArr = computed(() => {
	console.log('hi', year.value, month.value);
	const arr = getCalendarArray(year.value, month.value);
	// reservations객체 주입
	// const thisMonthReservations = fetchedReservations.getThisMonth

	return arr;
});

// event handlers
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
		margin-bottom: 8px;
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
						min-height: 100px;
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
						.reservation.multi {
							background-color: white;
							border: 1px solid $sejong-grey;
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
}
</style>
