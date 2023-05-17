<template>
	<div class="reservation-card">
		<div class="time-container" :class="timeContainerStyleObject">
			<span class="date">
				{{ timeInfo.date }}
			</span>

			<span>{{ timeInfo.start }}</span>
			<span>─</span>
			<span>{{ timeInfo.end }}</span>
		</div>

		<div class="contents-container">
			<p class="topic">{{ contents.topic }}</p>

			<div class="location">
				<img :src="pinIcon" alt="위치를 나타내는 핀 아이콘" />
				<span class="title">{{ contents.building }}</span>
				<span class="value">{{ contents.room }}</span>
			</div>

			<div class="members">
				<img :src="groupIcon" alt="구성원을 의미하는 한 무리의 사람 아이콘" />
				<span class="title" style="margin-left: 2px">
					{{ contents.members.length + '명' }}
				</span>
				<span class="value">
					{{ contents.members.toString().split(',').join(' ') }}
				</span>
			</div>
		</div>
	</div>
</template>

<script setup>
// import : library
import { computed } from 'vue';

import dayjs from 'dayjs';
import 'dayjs/locale/ko';
import customParseFormat from 'dayjs/plugin/customParseFormat';

// import : my script
import getTimeRangeByTimeslot from '@/assets/scripts/getTimeRangeByTimeSlot.js';

// import : etc
import pinIcon from '@/assets/images/icons/pin.png';
import groupIcon from '@/assets/images/icons/group.png';

// imported library setting
dayjs.locale('ko');
dayjs.extend(customParseFormat);
// ----------------------------------

const props = defineProps({
	reservation: {
		required: false,
		default() {
			return {
				reservationID: '-1',
				reservationDate: '0000-00-00', //
				reservationTimeslot: [],
				reservationTopic: '',
				creatorID: -1,
				userName: '',
				members: [],
				reservationRoomID: -1,
				reservationRoomBuilding: '',
				reservationRoomName: '',
				isRegular: false,
			};
		},
	},
});

// contents-container 관련
const contents = computed(() => {
	const obj = {};
	obj.topic = props.reservation.reservationTopic;
	obj.building = props.reservation.reservationRoomBuilding;
	obj.room = props.reservation.reservationRoomName;
	obj.members = props.reservation.members;

	return obj;
});

// time-container 관련
const timeInfo = computed(() => {
	const obj = {};

	const _propDate = props.reservation.reservationDate;
	const _propTimeslot = props.reservation.reservationTimeslot;

	obj.date = getDateStr(_propDate);

	// [0,1,2]를 00:00~00:30 처럼 시간범위로 바꾸는 함수입니다.
	const { start, end } = getTimeRangeByTimeslot(_propTimeslot);
	obj.start = start;
	obj.end = end;

	return obj;
});

const timeContainerStyleObject = computed(() => ({
	today: timeInfo.value.date === '오늘',
	tomorrow: timeInfo.value.date === '내일',
	others: timeInfo.value.date !== '오늘' && timeInfo.value.date !== '내일',
}));

function getDateStr(str) {
	// input : 날짜 문자열 (e.g) 'yyyy-MM-dd'
	// output
	//   - 입력 날짜가 오늘인 경우 : '오늘'반환
	//   - 입력 날짜가 내일인 경우 : '내일'반환
	//   - 그 외 input이 유효할 때 : 'MM/dd(요일)'반환
	//   - 올바르지 않은 input일 때 : 'X'반환

	if (!dayjs(str, 'YYYY-MM-DD', true).isValid()) {
		return 'X'; // 올바르지 않은 input
	}

	const now = dayjs();
	const nowStr = now.format('YYYY-MM-DD');
	const tomorrow = now.add(1, 'day');
	const tomorrowStr = tomorrow.format('YYYY-MM-DD');

	if (str === nowStr) {
		return '오늘';
	} else if (str === tomorrowStr) {
		return '내일';
	} else {
		return dayjs(str, 'YYYY-MM-DD').format('MM/DD(ddd)');
	}
}
</script>

<style lang="scss" scoped>
.reservation-card {
	display: flex;
	width: 512px;

	margin: 12px;

	background-color: white;
	border-radius: $box-radius;

	box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
	-webkit-box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
	-moz-box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);

	cursor: pointer;
	transition: all 0.1s;

	// 시간정보, 내용정보 공통 스타일
	.time-container,
	.contents-container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		padding: 18px 12px;
	}

	// 시간정보
	.time-container {
		align-items: center;
		min-width: 96px;
		border-radius: $box-radius 0 0 $box-radius;

		.date {
			margin-bottom: 12px;
			font-weight: 900;
		}
		span {
			margin: 4px 0;
		}
	}
	.today {
		background-color: $sejong-red;
		color: white;
	}
	.tomorrow {
		background-color: $sejong-grey;
		color: white;
	}
	.others {
		border-right: 1px solid $sejong-grey;
		color: $sejong-grey;
	}

	// 내용정보
	.contents-container {
		.topic {
			font-size: 1.2rem;
			font-weight: bold;
		}
		.location {
			margin: 12px 0 4px 0;
		}

		.title {
			font-weight: bold;
		}
		.value {
			margin-left: 4px;
		}
		img {
			vertical-align: middle;
			display: inline-block;
			height: 24px;
			width: auto;
			margin-right: 8px;
		}
	}
}

.reservation-card:hover {
	filter: brightness(90%);
}
.reservation-card:active {
	transform: scale(105%);
}

@media (max-width: 768px) {
	.reservation-card {
		width: 100%;
	}
}
</style>
