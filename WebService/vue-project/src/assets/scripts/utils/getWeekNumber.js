// 년 월 일 YYYY-MM-dd를 받아서 이 날짜가 달력상 해당 월의 몇 번째 줄인지 반환합니다.
// 예시 : getWeekNumber('2023-05-19')의 반환값은 3 (세 번째 줄)
// ** 주의 시작은 일요일로 함.

export default function getWeekNumber(dateStr) {
	// const date = new Date(year, month - 1, day);
	const [_year, _month, _day] = dateStr.split('-');
	const year = parseInt(_year);
	const month = parseInt(_month);
	const day = parseInt(_day);

	const firstDateOfMonth = new Date(year, month - 1, 1);

	const firstDateDow = firstDateOfMonth.getDay();
	const firstWeekLength = 7 - firstDateDow;

	if (day <= firstWeekLength) {
		return 1;
	}

	const weekNumber = parseInt(2 + (day - firstWeekLength - 1) / 7);

	return weekNumber;
}
