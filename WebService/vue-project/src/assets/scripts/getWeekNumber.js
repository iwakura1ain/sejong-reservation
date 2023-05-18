// 년 월 일(숫자)를 받아서 이 날짜가 전체 해당 월의 몇 번째 주인지 반환합니다.
// 예시 : getWeekNumber(2023,5,19)의 반환값은 4 (네 번째 주)
export default function getWeekNumber(year, month, day) {
	const date = new Date(year, month - 1, day);
	const startOfMonth = new Date(year, month - 1, 1);
	const startOfWeek = startOfMonth.getDay() || 7;
	const adjustedDate = date.getDate() + startOfWeek - 1;
	const weekNumber = Math.ceil(adjustedDate / 7);

	return weekNumber;
}
