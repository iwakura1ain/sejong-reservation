export default function getCalendarArray(year, month) {
	const calendarArr = getCalDateArr(year, month).map(week => {
		return week.map(day => {
			return {
				day: day,
				dateStr: day == 0 ? null : formatDate(year, month, day),
				reservations: [],
			};
		});
	});

	return calendarArr;
}

function formatDate(year, month, day) {
	const formattedMonth = month < 10 ? `0${month}` : month;
	const formattedDay = day < 10 ? `0${day}` : day;
	return `${year}-${formattedMonth}-${formattedDay}`;
}

function getCalDateArr(year, month) {
	const calDateArr = [];
	const endDate = new Date(year, month, 0);
	const totalDays = endDate.getDate();

	let currentWeek = [];
	for (let day = 1; day <= totalDays; day++) {
		const date = new Date(year, month - 1, day);
		const weekDay = date.getDay();

		if (weekDay === 0 && currentWeek.length > 0) {
			calDateArr.push(currentWeek);
			currentWeek = [];
		}

		currentWeek.push(day);
	}

	if (currentWeek.length > 0) {
		calDateArr.push(currentWeek);
	}

	// 첫 주 앞에 빈 날짜 채우기
	console.log(calDateArr);
	const firstWeekEmptyNum = 7 - calDateArr[0].length;
	for (let i = 0; i < firstWeekEmptyNum; i++) {
		calDateArr[0].unshift(0);
	}

	// 마지막 주 뒤에 빈 날짜 채우기
	const lastWeekEmptyNum = 7 - calDateArr[calDateArr.length - 1].length;
	for (let i = 0; i < lastWeekEmptyNum; i++) {
		calDateArr[calDateArr.length - 1].push(0);
	}

	return calDateArr;
}
// 테스트
const year = 2023;
const month = 5;
const calDateArr = getCalDateArr(year, month);
console.log(calDateArr);
/*
[ 
  [0, 1, 2, 3, 4, 5, 6]
  [7, 8, 9, 10, 11, 12, 13]
  [14, 15, 16, 17, 18, 19, 20]
  [21, 22, 23, 24, 25, 26, 27]
  [28, 29, 30, 31, 0, 0, 0] 
]
*/
