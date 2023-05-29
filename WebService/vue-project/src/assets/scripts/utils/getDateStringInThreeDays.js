// 오늘, 내일, 모레의 날짜를 'YYYY-MM-DD'형태의 문자열로 반환합니다.

// 입력 인수 : 없음
// 반환 값
/*
{
  today : 오늘 문자열,
  tomorrow : 내일 문자열,
  afterTomorrow : 모레 문자열
}
*/

export default function getDateStringInThreeDays() {
	function formatDate(date) {
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		return `${year}-${month}-${day}`;
	}

	const today = new Date();
	const tomorrow = new Date();
	tomorrow.setDate(today.getDate() + 1);
	const afterTomorrow = new Date();
	afterTomorrow.setDate(today.getDate() + 2);

	const formattedToday = formatDate(today);
	const formattedTomorrow = formatDate(tomorrow);
	const formattedAfterTomorrow = formatDate(afterTomorrow);

	return {
		today: formattedToday,
		tomorrow: formattedTomorrow,
		afterTomorrow: formattedAfterTomorrow,
	};
}
