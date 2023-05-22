// 백엔드로부터 응답받은 예약(reservation)한 개의 데이터를 프론트엔드에 맞게 변환합니다.
// 1. Mapping
// 2. 백엔드 응답 데이터 스키마
// 3-1. 프론트엔드 데이터 스키마
// 3-2. 프론트엔드 데이터 예시

// --------------------------------------------
// 1. 백엔드 응답 데이터 --> 프론트엔드 데이터 Mapping.
// --------------------------------------------
export default function convertReservationRes(res, minmaxType) {
	// res : 응답받은 rerservation 단일 객체
	// minmaxType : 최소정보인지, 최대정보인지. : "min" 또는 "max"
	let splitted;
	let convertedObj = {}; // res를 변환한 객체가 convertedObj에 담겨 리턴됨.

	// IF : minmaxType === 'min' (최소정보)
	if (minmaxType === 'min') {
		splitted = {
			start_time: res.start_time.split(':'),
			end_time: res.end_time.split(':'),
		};
		convertedObj = {
			id: res.id, // 0, 1, 2, ...
			reservationType: res.reservation_type, // null, "String"

			meetingDatetime: {
				date: res.reservation_date, // YYYY-MM-DD
				startTime: `${splitted.start_time[0]}:${splitted.start_time[1]}`, // HH:mm
				endTime: `${splitted.end_time[0]}:${splitted.end_time[1]}`,
			},

			roomId: res.room_id, // 0, 1, 2, 3,...
			isValid: res.is_valid, // 0, 1
			roomUsed: res.room_used, // 0, 1
		};
	}
	// IF : minmaxType === 'max' (최대정보)
	else if (minmaxType === 'max') {
		splitted = {
			created_at: res.created_at.split(' '),
			start_time: res.start_time.split(':'),
			end_time: res.end_time.split(':'),
		};
		convertedObj = {
			id: res.id, // 0, 1, 2, ...
			reservationType: res.reservation_type, // null, "String"

			meetingDatetime: {
				date: res.reservation_date, // YYYY-MM-DD
				startTime: `${splitted.start_time[0]}:${splitted.start_time[1]}`, // HH:mm
				endTime: `${splitted.end_time[0]}:${splitted.end_time[1]}`,
			},

			roomId: res.room_id, // 0, 1, 2, ...

			topic: res.reservation_topic, // "string"
			members: res.members, // [ {name:'string', email:'string'} ]

			creatorId: res.creatorId, // 0, 1, 2, ...
			createdAt: {
				date: splitted.created_at[0], // YYYY-MM-DD
				time: splitted.created_at[1], // HH:mm:ss
			},
			isValid: res.is_valid, // true, false
			roomUsed: res.room_used, // 0(인증안됨), 1(인증됨)
			code: res.reservation_code, // "string"
		};
	} else {
		console.error('유효하지 않은 minmax 값이 들어왔습니다.');
		throw new Error('UNVALID_MINMAX_ARGUMENT');
	}

	return convertedObj;
}

// --------------------------------------------
// 2. 백엔드 응답 데이터 스키마
// --------------------------------------------
// -- 1) 최소 정보 데이터
/*
{
	id: Int,
	is_valid : int, // 0, 1,
	reservation_date: String, // YYYY-DD-MM
	startTime: String, // HH:mm:ss
	endTime: String, // HH:mm:ss
	room_id: Int, 
	room_used: Int, // 0, 1

	reservation_type: String | null,
}
*/

// -- 2) 최대 정보 데이터
/* 
{
	id: Int,
	reservation_type: String | null,

	created_at: String, // YYYY-DD-MM HH:mm:ss
	room_id: Int, 

	reservation_date: String, // YYYY-DD-MM
	start_time: String, // HH:mm:ss
	end_time: String, // HH:mm:ss

	creator_id: Int
	reservation_topic: String,
	members: [
		{ name: String, email: String }
	],
	room_used: Boolean,
	reservation_code: String
	is_valid : Boolean
};
*/

// --------------------------------------------
// 3-1. 프론트엔드 데이터 스키마
// --------------------------------------------
// -- 1) 최소 정보 데이터
/*
{
	id: Int.
	reservationType: String | null,
	meetingDatetime: {
		date: String // YYYY-MM-DD
		startTime: String, // HH:mm
		endTime: String, // HH:mm
	},
	roomId: Int, // 0, 1, 2, ...
	isValid: Boolean, // true, false
	roomUsed: Int, // 0(인증안됨), 1(인증됨)
}
*/

// -- 2) 최대 정보 데이터
/*
{
	id: Int, // 0, 1, 2, ...
	reservationType: String | null, // null, "String"

	meetingDatetime: {
		date: String, // YYYY-MM-DD
		startTime: String, // HH:mm
		endTime: String,
	},

	roomId: Int, // 0, 1, 2, ...

	topic: String,
	members: [ {name:'String', email:'String'} ],

	creatorId: Int, // 0, 1, 2, ...
	createdAt: {
		date: String, // YYYY-MM-DD
		time: String, // HH:mm:ss
	},
	isValid: Boolean, // true, false
	roomUsed: Int, // 0(인증안됨), 1(인증됨)
	code: String, // "string"
}
*/

// --------------------------------------------
// 3-2. 프론트엔드 데이터 예시
// --------------------------------------------
// -- 1) 최소 정보 데이터
/*
{
	id: 1.
	reservationType: null, 
	// --> null이면 단건예약. 
	// --> 유효한 문자열이면 정기예약이며, reservationType의 값이 정기예약의 식별자
	
	meetingDatetime: {
		date: '2023-05-23',
		startTime: '09:00',
		endTime: '13:00',
	},
	roomId: 0,
	isValid: true
	roomUsed: 0,
}
*/

// -- 2) 최대 정보 데이터
/*
{
	id: 1.
	reservationType: "abcdeabcdeab", 
	// --> null이면 단건예약. 
	// --> 유효한 문자열이면 정기예약이며, reservationType의 값이 정기예약의 식별자
	
	meetingDatetime: {
		date: '2023-05-23',
		startTime: '09:00',
		endTime: '13:00',
	},
	roomId: 0

	topic: '회의주제입니다.',
	members: [ 
		{name:'장호진', email:'hjj@example.com'},
		{name:'이원진', email:'lwj@example.com'},
	],

	creatorId: 3
	createdAt: {
		date: '2023-04-01',
		time: '09:10:11',
	},
	isValid: true
	roomUsed: 0,
	code: '12345',
}
*/
