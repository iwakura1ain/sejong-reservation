// 예약을 생성하거나 수정할 때 거치는 검증입니다.
import makeToast from '@/assets/scripts/utils/makeToast.js';

export default function validateDateTime(dateObj, timepickerObj) {
	//  timepickerObj : {
	//  	start: { HH: String(2Byte), mm: String(2Byte) }, // HH, mm은 두 자리 String (e.g., "09")
	// 		end: { HH: String(2Byte), mm: String(2Byte) },
	// 	}

	let result = true;

	// 종료시각이 시작시각 이후인가?
	const { start, end } = timepickerObj;
	const startTimeToSec = parseInt(start.HH) * 60 + parseInt(start.mm);
	const endTimeToSec = parseInt(end.HH) * 60 + parseInt(end.mm);
	if (startTimeToSec >= endTimeToSec) {
		result = false;
		makeToast('종료시각은 시작시각 이후여야 합니다', 'warning');
	}

	// 지정된 시각이 현재시각 이전인가?
	var now = new Date();
	const nowToSec = now.getHours() * 60 + now.getMinutes();

	if (
		dateObj <= now &&
		(startTimeToSec < nowToSec || endTimeToSec < nowToSec)
	) {
		result = false;
		makeToast('현재보다 과거에 예약을 생성할 수 없습니다', 'warning');
	}

	return result;
}
