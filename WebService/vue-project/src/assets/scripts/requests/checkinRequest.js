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

			// const data = res.data;
			if (!res.status) {
				console.error(res);
				return res;
			}
			console.log(res);

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
			//    통신
			console.log('id:', id, 'id type:', typeof id);
			console.log('id.id:', id.id, 'id.id type:', typeof id.id);
			console.log('reqBody:', id.reqBody, 'reqBody type:', typeof id.reqBody);

			const res = await axios
				.post(`${BASE_URL.RESERVATION_SERVICE}/check-in/${id.id}`, id.reqBody)
				.catch(function (err) {
					console.error(err);
					if (err.response.status !== 400) {
						throw new Error(err);
					} else {
						return err.response;
					}
				});

			const data = res.data;
			console.log('data: ', data);
			if (!data.status) {
				return data;
			}

			// 반환
			return {
				status: true,
				// data: null,
				msg: data.msg,
			};
		} catch (err) {
			console.error(err);
			throw new Error(err, { cause: err });
		}
	},
};

// import axios from 'axios';
// import { BASE_URL } from '@/assets/constants.js';

// // --------------------------
// export const attendenceChecker = {
//     registerRoom: async function (id, accessToken) {
//         try {
//            // 통신
//            const res = await axios
//               .get(`${BASE_URL.RESERVATION_SERVICE}/check-in/${id}/register`, {
//                  headers: {
//                     Authorization: `Bearer ${accessToken}`,
//                  },
//               })
//               .catch(function (err) {
//                  console.error(err);
//                  if (err.response.status !== 400) {
//                     throw new Error(err);
//                  } else {
//                     return err.response;
//                  }
//               });

//            const data = res.data;

//            // 반환
//            return data.room_hash;
//         } catch (err) {
//            console.error(err);
//            throw new Error(err, { cause: err });
//         }
//      },
//      // ---------------------------
//     checkin: async function (id, reqBody){
//         try {
//         //    통신
//            console.log("id:", id, "id type:",typeof(id));
//            console.log("id.id:", id.id, "id.id type:",typeof(id.id));
//            console.log("reqBody:", id.reqBody, "reqBody type:", typeof(id.reqBody));

//            const res = await axios
//               .post(`${BASE_URL.RESERVATION_SERVICE}/check-in/${id.id}`, id.reqBody)
//               .catch(function (err) {
//                  console.error(err);
//                  if (err.response.status !== 400) {
//                     throw new Error(err);
//                  } else {
//                     return err.response;
//                  }
//               });

//            const data = res.data;
//            console.log('data: ', data);
//            if(!data.status) {
//               return data
//            }

//            // 반환
//            return {
//               status: true,
//               // data: null,
//               msg: data.msg,
//            };
//         } catch (err) {
//            console.error(err);
//            throw new Error(err, { cause: err });
//         }
//     },
// }
