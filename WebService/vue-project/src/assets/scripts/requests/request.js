// api(백엔드)로 요청하고 받아와서 프론트엔드에 맞게 변환하는 코드입니다.

// 하는 일 (자세한 내용은 ./README.md 참고)
// 1. 데이터를 요청하고 받습니다.
// 2. 받은 데이터를 './responseConverters'폴더 안의 컨버터로 변환합니다.
// 3. { data:'변환된 데이터', msg:'string' } 의 형식으로 callee에 리턴합니다.

// 그 외 작업은 이 코드를 호출한 그곳에서 직접합니다.
// (데이터 본질적 내용의 변경, 상태 변경 등은 여기서 하지 말 것)

// -----------------------------------
// 참고 : constants.js의 BASE_URL객체
// export const BASE_URL = {
// 	USER_SERVICE: 'http://127.0.0.1/userservice',
// 	ADMIN_SERVICE: 'http://127.0.0.1/adminservice',
// 	RESERVATION_SERVICE: 'http://127.0.0.1/reservationservice',
// 	ALERT_SERVICE: 'http://127.0.0.1/alert',
// 	// WEB_SERVICE : "http://127.0.0.1/webservice",
// };

import axios from 'axios';
import { BASE_URL } from '@/assets/constants.js';

import TESTDATA from '@/assets/scripts/requests/TESTDATA.js';

import convertReservationRes from '@/assets/scripts/requests/responseConverters/convertReservationRes.js';
import convertRoomRes from '@/assets/scripts/requests/responseConverters/convertRoomRes.js';
import convertUserRes from '@/assets/scripts/requests/responseConverters/convertUserRes.js';

// --------------------------------------
// admin service
// - getRoom(id)
// - createRoom(reqBody)
// - updateRoom(id, reqBody)
// - deleteRoom(id)
// - getAllRooms()
// --------------------------------------
const adminService = {
	getRoom: function (id) {},
	// --------------------------------------------------------------------------
	createRoom: function (reqBody) {},
	// --------------------------------------------------------------------------
	updateRoom: function (id, reqBody) {},
	// --------------------------------------------------------------------------
	deleteRoom: function (id) {},
	// --------------------------------------------------------------------------
	getAllRooms: async function () {
		try {
			// fetch data
			// const res = await axios.get(`${BASE_URL.ADMIN_SERVICE}/admin/rooms`);
			const res = {
				// test res
				status: 200,
				data: {
					status: true,
					allRooms: TESTDATA.rooms_1,
					msg: 'Room found',
				},
			};

			// check axios's status
			if (res.status !== 200) {
				return {
					status: true,
					data: null,
					msg: 'INVALID_STATUS',
				};
			}

			// get res body (axios's data property)
			const data = res.data;

			// check body's status
			if (data.status) {
				const converted = data.allRooms.map(room => convertRoomRes(room));
				return {
					status: true,
					data: converted,
				};
			} else {
				if (data.msg === 'Not logged in') {
					return {
						status: true,
						data: null,
						msg: 'NOT_LOGGED_IN',
					};
				} else if (data.msg === 'Room not found') {
					return {
						status: true,
						data: null,
						msg: 'ROOM_NOT_FOUND',
					};
				}
			}

			// convert raw data to frontend-format data
			const converted = data.allRooms.map(room => convertRoomRes(room));
			return {
				status: true,
				data: converted,
				msg: 'nice',
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
};

// --------------------------------------
// user service
// - login()
// - getAuthInfo()
// - refreshAuth()
// - logout()
// - register()
// - registerFromExcel()
// - update()
// - delete()
// - getAll()
// --------------------------------------
const userService = {
	login: async function (reqBody) {
		try {
			// 통신
			const res = await axios.post(
				`${BASE_URL.USER_SERVICE}/auth/login`,
				reqBody,
			);
			/*
				res schema = {
					status : int, // axios의 http status code
					data : {
						status : Boolean, // response body의 status field
						access_token : String, // status===true일 때 있음
						refresh_token : String, // status===true일 때 있음
						User : {}, // status===true일 때 있음
						msg : String , // status===false일 때 있음
					}
				}
			*/

			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_RESPONSE:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			// 데이터 컨버팅
			const data = res.data;
			const converted = convertUserRes(data);
			return {
				status: true,
				data: converted,
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	getAuthInfo: async function (accessToken) {
		try {
			// 통신
			const res = await axios.get(`${BASE_URL.USER_SERVICE}/auth/jwt-status`, {
				headers: {
					Authorization: `Bearer ${accessToken}`,
				},
			});

			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_RESPONSE:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			// 데이터 컨버팅
			const data = res.data;
			const converted = convertUserRes(data);
			return {
				status: true,
				data: converted,
				msg: 'authenticated',
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	refreshAuth: async function (refreshToken) {
		try {
			// 통신
			const res = await axios.get(`${BASE_URL.USER_SERVICE}/auth/jwt-refresh`, {
				headers: {
					Authorization: `Bearer ${refreshToken}`,
				},
			});

			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_RESPONSE:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			// 액세스토큰 반환
			const data = res.data;
			return {
				status: true,
				data: data.access_token,
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	logout: async function (accessToken) {
		try {
			// 통신
			const res = await axios.delete(`${BASE_URL.USER_SERVICE}/auth/logout`, {
				headers: {
					Authorization: `Bearer ${accessToken}`,
				},
			});

			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_RESPONSE:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			// 반환
			return {
				status: true,
				msg: res.data.msg,
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	// --------------------------------------------------------------------------
	register: async function (reqBody) {
		try {
			// 통신
			const res = await axios.post(
				`${BASE_URL.USER_SERVICE}/auth/register`,
				reqBody,
			);

			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_RESPONSE:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			// 데이터 컨버팅
			const data = res.data;
			const converted = convertUserRes(data);
			return {
				status: true,
				data: converted,
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	registerFromExcel: async function () {},
	// --------------------------------------------------------------------------
	update: async function (id, reqBody, accessToken) {
		try {
			// 통신
			const res = await axios.patch(
				`${BASE_URL.USER_SERVICE}/users/${id}`,
				reqBody,
				{
					headers: {
						Authorization: `Bearer ${accessToken}`,
					},
				},
			);
			console.log(`${BASE_URL.USER_SERVICE}/users/${id}`);
			console.log(accessToken);
			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_RESPONSE:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			return res.data;
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	delete: async function (id, accessToken) {
		try {
			const res = await axios.delete(`${BASE_URL.USER_SERVICE}/users/${id}`, {
				headers: {
					Authorization: `Bearer ${accessToken}`,
				},
			});

			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_RESPONSE:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			// 반환
			return {
				status: true,
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	// --------------------------------------------------------------------------
	getAll: async function () {},
	// --------------------------------------------------------------------------
};

// --------------------------------------
// reservation service
// - get(options)
// - getById(id)
// - getByReservationType(reservationType)
// - create(reqBody)
// - update(id, reqBody)
// - delete(id)
// --------------------------------------
const reservationService = {
	// --------------------------------------------------------------------------
	get: async function (
		options = {
			before: '',
			after: '',
			room: '',
			creator: null,
			reservationType: null,
		},
	) {
		// ** options object schema.
		// {
		// 	before : 'YYYY-MM-DD', // 이 날짜 포함 이전
		// 	after : 'YYYY-MM-DD', // 이 날짜 포함 이후
		// 	room : Int, // room id
		// 	creator : String
		//	reservationType : String(12),
		// }

		try {
			// options객체 분석 & 요청URL만들기
			let reqUrl = `${BASE_URL.RESERVATION_SERVICE}/reservation`;
			let queryStr = '';
			if (options.before) {
				queryStr += `&before=${options.before}`;
			}
			if (options.after) {
				queryStr += `&after=${options.after}`;
			}
			if (options.room) {
				queryStr += `&room=${options.room}`;
			}
			if (options.creator) {
				queryStr += `&room=${options.creator}`;
			}
			if (options.reservationType) {
				queryStr += `&reservation_type=${options.reservationType}`;
			}

			// BASE URL과 쿼리스트링 결합
			if (queryStr !== '') {
				queryStr = queryStr.slice(1);
				queryStr = '?' + queryStr;
			}
			reqUrl = reqUrl + queryStr;

			// 데이터 불러오기 fetch data
			// const res = await axios.get(reqUrl);
			/*
			res schema = {
				status : int, // axios의 http status code
				data : {
					status : Boolean, // response body의 status field
					reservations : [{}], // status===true일 때 있음
					msg : String , // status===false일 때 있음
				}
			}
			*/
			const res = {
				// test res
				status: 200,
				data: {
					status: true,
					reservations: TESTDATA.reservations_min_1, // 일반 사용자
					// reservations : TESTDATA.reservation_max_1, // 어드민
				},
			};

			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_RESPONSE:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			// get res body (axios's data property)
			const data = res.data;

			// convert raw data to frontend-format data
			const fieldNum =
				data.reservations.length === 0
					? 0
					: Object.keys(data.reservations[0]).length;
			const minmaxType = fieldNum <= 8 ? 'min' : 'max';

			const converted = data.reservations.map(item =>
				convertReservationRes(item, minmaxType),
			);

			return {
				status: true,
				data: converted,
				msg: '',
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	getById: function (id) {
		try {
			// 데이터 불러오기 fetch data
			// const res = await axios.get(`${BASE_URL.RESERVATION_SERVICE}/reservation/${id}}`);
			/*
			res schema = {
				status : int, // axios의 http status code
				data : {
					status : Boolean, // response body의 status field
					reservation : {}, // status===true일 때 있음
					msg : String , // status===false일 때 있음
				}
			}
			*/
			const res = {
				// test res
				status: 200,
				data: {
					status: true,
					// reservation: TESTDATA.a_reservation_max_1_single,
					reservation: TESTDATA.a_reservation_max_2_regular,
				},
			};

			// 응답 정상여부 확인
			if (res.status !== 200 || !res.data) {
				throw new Error(`INVALID_STATUS:${res.status}:${res}`);
			}
			if (!res.data.status) {
				console.error(res.data);
				return res.data;
			}

			// get res body (axios's data property)
			const data = res.data;

			// convert raw data to frontend-format data
			const converted = convertReservationRes(data.reservation, 'max');
			return {
				status: true,
				data: converted,
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	getMyFullData: async function (options) {
		// options객체 스키마 : reservationService.get() 참고
		try {
			// 내가 생성한 예약들의 최소정보 예약객체 불러오기
			const resGet = await reservationService.get(options);
			if (!resGet.status) {
				console.error(resGet.data);
				return resGet.data;
			}

			// 각 최소정보 예약객체의 id로 최대정보 예약객체 불러오기
			const resData = [];
			const getByIdPromises = resGet.data.map(item =>
				reservationService.getById(item.id),
			);
			await Promise.all(getByIdPromises).then(responses => {
				for (let res of responses) {
					if (!res.status) {
						console.error(res.data);
						resData.push(null);
					}
					resData.push(res.data);
				}
			});

			// 내가 생성한 예약의 최대정보 예약객체 리스트 반환
			return {
				status: true,
				data: resData,
				msg: '',
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// --------------------------------------------------------------------------
	create: function (reqBody) {},
	// --------------------------------------------------------------------------
	update: function (id, reqBody) {},
	// --------------------------------------------------------------------------
	delete: function (id) {},

	// ---------------------------
	// ---------------------------
	// test
	TEST_GET_REGULAR_MAXIMIZED_RSV: function ({ reservationType }) {
		const a = TESTDATA.reservations_max_2_regular;
		const converted = a.map(item => convertReservationRes(item, 'max'));
		return {
			status: true,
			data: converted,
			msg: '',
		};
	},
};

// --------------------------------------
// alert service
// --------------------------------------
const alertService = {
	// empty
};

// --------------------------------------
// export
// --------------------------------------
export { adminService, userService, reservationService, alertService };
