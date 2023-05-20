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
	createRoom: function (reqBody) {},
	updateRoom: function (id, reqBody) {},
	deleteRoom: function (id) {},
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
					msg: 'nice',
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
	login: async function () {},
	getAuthInfo: async function () {},
	refreshAuth: async function () {},
	logout: async function () {},

	register: async function () {},
	registerFromExcel: async function () {},

	update: async function () {},
	delete: async function () {},

	getAll: async function () {},
};

// --------------------------------------
// reservation service
// - get(options)
// - getById(id)
// - create(reqBody)
// - update(id, reqBody)
// - delete(id)
// --------------------------------------
const reservationService = {
	get: async function (
		options = { before: '', after: '', roomName: '', mine: false },
	) {
		// ** options object schema.
		// {
		// 	before : 'YYYY-MM-DD',
		// 	after : 'YYYY-MM-DD',
		// 	roomName : 'string',
		// 	mine : Boolean
		// }

		try {
			// inspect options object & determine request url.
			let reqUrl = `${BASE_URL.RESERVATION_SERVICE}/reservation?mine=${options.mine}`;
			if (options.before) {
				reqUrl += `?before=${options.before}`;
			}
			if (options.after) {
				reqUrl += `?after=${options.after}`;
			}
			if (options.roomName) {
				reqUrl += `?room=${options.roomName}`;
			}

			// fetch data
			// const res = await axios.get(reqUrl);
			const res = {
				// test res
				status: 200,
				data: {
					status: true,
					reservations: TESTDATA.reservations_max_1,
				},
			};

			// check response's status & body's status
			if (res.status !== 200 && res.data.status) {
				return {
					status: false,
					data: res.status,
					msg: 'INVALID_STATUS',
				};
			}

			// get res body (axios's data property)
			const data = res.data;

			// convert raw data to frontend-format data
			const fieldNum =
				data.reservations.length === 0
					? 0
					: Object.keys(data.reservations[0]).length;
			const minmaxType = fieldNum <= 6 ? 'min' : 'max';

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
	getById: function (id) {},
	create: function (reqBody) {},
	update: function (id, reqBody) {},
	delete: function (id) {},
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
