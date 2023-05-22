// 예약 유형
export const RESERVATION_TYPE = {
	SINGLE: 0, // 단건 예약
	MULTI: 1, // 정기 예약
};

// 정기예약 시 종료시점을 결정하는 유형
export const REPEAT_END_TYPE = {
	REPS: 0, // 횟수
	DATE: 1, // 날짜
};

// 사용자 구분 유형
export const USER_TYPE = {
	ADMIN: 1, // 관리자
	PROFESSOR: 2, // 교수
	GRAD_STUDENT: 3, // 대학원생
	UNDER_GRAD_STUDENT: 4, // 학부생
};

// 학과 구분 유형
export const DEPT_TYPE = {
	COMPUTER: 1, // 컴퓨터공학과
	OTHERS: 2, // 기타학과
};

// 백엔드로 요청 넣을 베이스 URL
export const BASE_URL = {
	USER_SERVICE: 'http://127.0.0.1:8080/userservice',
	ADMIN_SERVICE: 'http://127.0.0.1:8080/adminservice',
	RESERVATION_SERVICE: 'http://127.0.0.1:8080/reservationservice',
	ALERT_SERVICE: 'http://127.0.0.1:5000/alert',
	// WEB_SERVICE : "http://127.0.0.1/webservice",
};
