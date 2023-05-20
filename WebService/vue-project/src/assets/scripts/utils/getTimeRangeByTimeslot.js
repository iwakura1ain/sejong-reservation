// --------------------------------------------------------------------------
// 개요 : getTimeRangeByTimeslot.js
// --------------------------------------------------------------------------

// 백엔드로부터 받아온 날 것의 timeslot배열을 분석하여,
// 전체 시간의 시작시각, 종료시각이 언제인지 알아냅니다.
// 예를 들면, [0,1,2,3,4]와 같은 배열을 "00:00시작 00:50종료" 와 같은 정보로 바꿉니다.

// --------------------------------------------------------------------------
// 설정이 필요한 값
// --------------------------------------------------------------------------

const DIVIDE_MINUTE = 10; // 몇 분 단위로 예약할 수 있는지?
//  -- 예시) 값이 10이면 10분단위 예약이 가능
//           --> 12:00~12:10
//           --> 16:40~17:30

// const NUM_TIMESLOT = 24 * parseInt(60 / DIVIDE_MINUTE); // 타임슬롯의 개수

// --------------------------------------------------------------------------
// --------------------------------------------------------------------------

function getTime(timeslot, type) {
	// timeslot : int(타임슬롯 번호)
	// type : 'start', 'end' (시작시각 뽑을건지, 종료시각 뽑을건지)

	const flag = type === 'start' ? 0 : 1;
	const totalMins = (timeslot + flag) * DIVIDE_MINUTE;

	const hour = parseInt(totalMins / 60);
	const min = totalMins - hour * 60;

	const hourStr = hour < 10 ? `0${hour}` : hour;
	const minStr = min < 10 ? `0${min}` : min;
	return `${hourStr}:${minStr}`;
}

function getTimeRangeByTimeslot(timeslotArr) {
	const obj = {
		start: '00:00',
		end: '00:00',
	};

	const firstSlot = Math.min(...timeslotArr);
	const lastSlot = Math.max(...timeslotArr);

	obj.start = getTime(firstSlot, 'start');
	obj.end = getTime(lastSlot, 'end');

	return obj;
}

export default getTimeRangeByTimeslot;
