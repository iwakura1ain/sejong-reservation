import { ref } from 'vue';
import getTodayZeroHour from '@/assets/scripts/utils/getTodayZeroHour.js';
import { RESERVATION_TYPE, REPEAT_END_TYPE } from '@/assets/constants.js';

// RoomSelector --------------------------------------------------------
export const selectedRoom = ref({});

// MeetingDatetimeSelector --------------------------------------------------
export const reservationType = ref(RESERVATION_TYPE.SINGLE); // 일정 유형 (단건, 정기)
export const startDate = ref(getTodayZeroHour()); // 예약 날짜

export const pickedTime = ref({
	start: { HH: '', mm: '' },
	end: { HH: '', mm: '' },
});

export const repeatEndType = ref(REPEAT_END_TYPE.REPS); // 종료시점 (횟수, 날짜)
export const endReps = ref(1); // 종료시점 - 횟수
export const endDate = ref(getTodayZeroHour()); // 종료시점 - 날짜

export const datetimeAvailability = ref([]); // 사용자가 예약하고자 하는 일시, 그 일시가 예약 가능한지 여부
// │ 원소는 Object인데, 필드는 아래와 같음
// │ {
// │ 	year, month, day, : 년 월 일
// │  dayofTheWeek : 요일(일요일 0, 토요일 6)
// │  dateString : 'YYYY-MM-DD (dd)' 꼴 문자열
// │ 	available : true 또는 false
// └ }

// MeetingMemberWriter --------------------------------------------------
export const topic = ref('');
export const members = ref([
	{
		name: '',
		email: '',
	},
]);
