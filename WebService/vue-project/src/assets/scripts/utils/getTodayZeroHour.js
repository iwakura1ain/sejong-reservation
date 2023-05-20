// 오늘 날짜이지만 시간,분,초,밀리초가 0인 Date객체를 반환합니다.

export default function getTodayZeroHour() {
	const dateObj = new Date();
	dateObj.setHours(0, 0, 0, 0);

	return dateObj;
}
