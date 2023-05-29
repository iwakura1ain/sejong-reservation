export default function getDayofWeek(dateString) {
	// 입력 : 'YYYY-MM-DD'
	// 출력 : 해당 날짜의 요일
	const date = new Date(dateString);
	const daysOfWeek = ['일', '월', '화', '수', '목', '금', '토'];
	const dayOfWeekIndex = date.getDay();
	const dayOfWeek = daysOfWeek[dayOfWeekIndex];
	return dayOfWeek;
}
// TEST
// const date = '2023-05-21';
// const dayOfWeek = getDayOfWeek(date);
// console.log(dayOfWeek); // '일'
