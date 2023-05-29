// 예약 유형
// --- 정기예약 시 종료시점을 결정하는 유형
export const REPEAT_END_TYPE = {
	REPS: 1, // 횟수
	DATE: 2, // 날짜
};
// --- 정기예약 시 반복할 주기
export const REPEAT_INTERVAL_TYPE = {
	MONTH: 1, // 매월
	WEEK: 2, // 매주
	DAY: 3, // 매일
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
// const SERVICE_IP = localStorage.getItem('SEJONG_RESERVATION_SERVICE_IP');
export const BASE_URL = {
	// TODO: 실제로 배포하게 되면 아래 속성들을 사용합니다.
	// USER_SERVICE: `http://${SERVICE_IP}:8080/userservice`,
	// ADMIN_SERVICE: `http://${SERVICE_IP}:8080/adminservice`,
	// RESERVATION_SERVICE: `http://${SERVICE_IP}:8080/reservationservice`,
	// ALERT_SERVICE: `http://${SERVICE_IP}:5000/alert`,
	// WEB_SERVICE : `http://${SERVICE_IP}/webservice`,

	// --------------------------------------------------------------------
	// TODO: 테스트할때는 아래 속성들을 사용합니다.
	// 웹사이트에 접속하는 기기에서 우리 도커컨테이너가 돌아가고 있어야 합니다.
	USER_SERVICE: `http://127.0.0.1:8080/userservice`,
	ADMIN_SERVICE: `http://127.0.0.1:8080/adminservice`,
	RESERVATION_SERVICE: `http://127.0.0.1:8080/reservationservice`,
	ALERT_SERVICE: `http://127.0.0.1:5000/alert`,
	//WEB_SERVICE : `http://127.0.0.1/webservice`,
};
