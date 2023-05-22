// 오늘 날짜이지만 시간,분,초,밀리초가 0인 Date객체를 반환합니다.
import formatDate from '@/assets/scripts/utils/formatDate.js';

// 입력 : type ('DATE'이면 Date객체, 'STRING'이면 'YYYY-MM-DD'반환)
export default function getTodayZeroHour(type = 'DATE') {
	const dateObj = new Date();
	dateObj.setHours(0, 0, 0, 0);

	if (type === 'DATE') return dateObj;
	else type === 'STRING';
	return getDateStringFromDateObject(dateObj);
}

function getDateStringFromDateObject(date) {
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, '0');
	const day = String(date.getDate()).padStart(2, '0');
	return `${year}-${month}-${day}`;
}
