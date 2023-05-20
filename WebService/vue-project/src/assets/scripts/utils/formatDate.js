export default function formatDate(year, month, day) {
	const formattedMonth = month < 10 ? `0${month}` : month;
	const formattedDay = day < 10 ? `0${day}` : day;
	return `${year}-${formattedMonth}-${formattedDay}`;
}
