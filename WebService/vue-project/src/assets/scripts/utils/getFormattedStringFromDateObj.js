// 입력 : dateObj (Date객체)
// 입력 : formatString ('YYYY-MM-DD' 또는 'YYYY-MM-DD(ddd)')

// 출력 : String
// --- formatString='YYYY-MM-DD'이면 '2023-05-23'
// --- formatString='YYYY-MM-DD(ddd)'이면 '2023-05-23(화)'
import getDayofWeek from '@/assets/scripts/utils/getDayofWeek.js';

export default function getFormattedStringFromDateObj(dateObj, formatString) {
	const year = dateObj.getFullYear();
	const month = String(dateObj.getMonth() + 1).padStart(2, '0');
	const day = String(dateObj.getDate()).padStart(2, '0');
	const dow = getDayofWeek(`${year}-${month}-${day}`);

	if (formatString === 'YYYY-MM-DD') {
		return `${year}-${month}-${day}`;
	} else if (formatString === 'YYYY-MM-DD(ddd)') {
		return `${year}-${month}-${day}(${dow})`;
	}
}
