import axios from 'axios';
import { BASE_URL } from '@/assets/constants.js';

// --------------------------
export const attendenceChecker = {
	registerRoom: async function (id, accessToken) {
		try {
			// 통신
			const res = await axios
				.get(`${BASE_URL.RESERVATION_SERVICE}/check-in/${id}/register`, {
					headers: {
						Authorization: `Bearer ${accessToken}`,
					},
				})
				.catch(function (err) {
					console.error(err);
					if (err.response.status !== 400) {
						throw new Error(err);
					} else {
						return err.response;
					}
				});

			if (!res.data.status) {
				console.error(res);
				return res.data;
			}

			// 반환
			return {
				status: true,
				data: res.data.room_hash,
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
	// ---------------------------
	checkin: async function (id, reqBody) {
		try {
			const res = await axios
				.post(`${BASE_URL.RESERVATION_SERVICE}/check-in/${id}`, reqBody)
				.catch(function (err) {
					console.error(err);
					if (err.response.status !== 400) {
						throw new Error(err);
					} else {
						return err.response;
					}
				});

			console.log(res);
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
};
