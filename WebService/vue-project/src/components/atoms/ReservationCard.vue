<template>
	<div class="reservation-card">
		<div class="time-container" :class="timeContainerStyleObject">
			<span class="date">
				{{ dayExpression }}
			</span>

			<span>{{ rsvData.meetingDatetime.startTime }}</span>
			<span>─</span>
			<span>{{ rsvData.meetingDatetime.endTime }}</span>
		</div>

		<div class="contents-container">
			<p class="topic">{{ rsvData.topic }}</p>

			<div class="location">
				<img :src="pinIcon" alt="위치를 나타내는 핀 아이콘" />
				<span class="title">{{ roomData.address1 }}</span>
				<span class="value">{{ roomData.address2 }}</span>
				<span class="value">{{ roomData.name }}</span>
			</div>

			<div class="members">
				<img :src="groupIcon" alt="구성원을 의미하는 한 무리의 사람 아이콘" />
				<span class="title" style="margin-left: 2px">
					{{ rsvData.members.length + '명' }}
				</span>
				<span class="value">
					{{ membersNameString }}
				</span>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue';

import pinIcon from '@/assets/images/icons/pin.png';
import groupIcon from '@/assets/images/icons/group.png';

// dayjs
import dayjs from 'dayjs';
import 'dayjs/locale/ko';
import customParseFormat from 'dayjs/plugin/customParseFormat';
dayjs.locale('ko');
dayjs.extend(customParseFormat);

// ----------------------------------

const props = defineProps({
	rsvData: {
		// reservation data
		required: true,
		type: Object,
		default() {
			// 단건예약 예시
			return {
				id: -1,
				reservationType: null,

				meetingDatetime: {
					date: 'YYYY-MM-DD',
					startTime: 'HH:mm',
					endTime: 'HH:mm',
				},
				roomId: -1,
				topic: '',
				members: [{ name: '', email: '' }],
			};
		},
	},
	roomData: {
		required: true,
		type: Object,
		default() {
			return {
				address1: '',
				address2: '',
				name: '',
			};
		},
	},
});

// 초기화 --------------------------------------------------
//

// 상태(state) ---------------------------------------------
const dayExpression = computed(() => {
	return getDayExpressionFromDateStr(props.rsvData.meetingDatetime.date);
});

const timeContainerStyleObject = computed(() => ({
	today: dayExpression.value === '오늘',
	tomorrow: dayExpression.value === '내일',
	others: dayExpression.value !== '오늘' && dayExpression.value !== '내일',
}));

const membersNameString = computed(() => {
	let names = props.rsvData.members.map(item => item.name);
	return names.toString().split(',').join(' ');
});

// 일반 함수 ------------------------------------------
function getDayExpressionFromDateStr(str) {
	// input : 날짜 문자열 (e.g) 'YYYY-MM-DD'
	// output
	//   - 입력 날짜가 오늘인 경우 : '오늘'반환
	//   - 입력 날짜가 내일인 경우 : '내일'반환
	//   - 그 외 input이 유효할 때 : 'MM/dd(요일)'반환
	//   - 올바르지 않은 input일 때 : null반환

	if (!dayjs(str, 'YYYY-MM-DD', true).isValid()) {
		console.error('올바르지 않은 문자열이 입력으로 들어왔습니다. : ', str);
		return null; // 올바르지 않은 input
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
