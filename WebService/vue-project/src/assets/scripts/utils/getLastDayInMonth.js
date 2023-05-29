export default function getLastDayInMonth(year, month) {
	const yearInt = parseInt(year);
	const monthInt = parseInt(month);

	const nextMonth = new Date(yearInt, monthInt, 1);
	const lastDay = new Date(nextMonth.getTime() - 86400000).getDate();

	return lastDay.toString().padStart(2, '0');
}

// const lastDay = getLastDay('2023', '05');
// console.log(lastDay); '31'
