// 두 Date겍체 사이의 차이를 구합니다.
// 월 단위 차이, 주 단위 차이, 일 단위 차이입니다. 모두 내림처리합니다.

export default function getDateDifference(date1, date2) {
	// var diff = Math.abs(date2.getTime() - date1.getTime());
	var diff = Math.abs(date2 - date1);
	return {
		// monthDiff: Math.floor(diff / (1000 * 60 * 60 * 24 * 30)), // 달 차이,
		// weekDiff: Math.floor(diff / (1000 * 60 * 60 * 24 * 7)), // 주 차이,
		// dayDiff: Math.floor(diff / (1000 * 60 * 60 * 24)) - 1, // 일 차이
		monthDiff: Math.ceil(diff / (1000 * 60 * 60 * 24 * 30)), // 달 차이,
		weekDiff: Math.ceil(diff / (1000 * 60 * 60 * 24 * 7)), // 주 차이,
		dayDiff: diff / (1000 * 60 * 60 * 24), // 일 차이
	};
}

// var date1 = new Date(2023, 6, 30);
// var date2 = new Date(2023, 7, 3);
// var diff = getDateDifference(date1, date2);
// console.log(diff);
