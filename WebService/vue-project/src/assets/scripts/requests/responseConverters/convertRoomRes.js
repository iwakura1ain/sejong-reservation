// 백엔드로부터 응답받은 회의실(room)한 개의 데이터를 프론트엔드에 맞게 변환합니다.
// 1. Mapping
// 2. 백엔드 응답 데이터 스키마
// 3-1. 프론트엔드 데이터 스키마
// 3-2. 프론트엔드 데이터 예시

// --------------------------------------------
// 1. 백엔드 응답 데이터 --> 프론트엔드 데이터 Mapping.
// --------------------------------------------
export default function convertRoomRes(res) {
	const obj = {
		id: res.id, // int -- 0,1,2,...
		name: res.room_name, // String
		address1: res.room_address1, // String
		address2: res.room_address2, // String
		isUsable: res.is_usable, // int -- 0(사용불가), 1(사용가능)
		maxUsers: res.max_users, // int

		// TODO: 시각은 아직 백엔드에서 지원안함.
		time: {
			open: res.open_time ? res.open_time : '09:00', // String -- HH:mm
			close: res.close_time ? res.close_time : '18:00', // String -- HH:mm
		},
		img: res.preview_image, // String -- http link (https://example.com/image.jpg)
	};

	return obj;
}

// --------------------------------------------
// 2. 백엔드 응답 데이터 스키마
// --------------------------------------------
/*
{
	id : Int,
	room_name : String,
	address1 : String,
	address2 : String,
	is_usable : Int (0, 1),
	max_users : Int,
	open_time : String (HH:mm),
	close_time : String (HH:mm),
	preview_image : String (http link)
}
*/

// --------------------------------------------
// 3-1. 프론트엔드 데이터 스키마
// --------------------------------------------
/*
{ 
    id : Int, // 회의실의 식별자 <예시>0,1,2,...
    name : String, // 회의실 이름 
    address1 : String, // 회의실 세부주소
    address2 : String, // 회의실 건물이름
    isUsable : Int, // 사용가능 여부 <예시> 0(사용불가), 1(사용가능)
    maxUsers : Int, // 최대 이용가능 인원수 <예시>0,1,2,...
    time : { // 운영시간(사용가능 시간)
      open : String, // 시작시각 HH:mm
      close : String, // 종료시각 HH:mm
    },
    img : String, // 회의실 미리보기 이미지 http link <예시> https://a.com/img.jpg
}
*/

// --------------------------------------------
// 3-2. 프론트엔드 데이터 예시
// --------------------------------------------
/*
{ // 예시
    id : 1
    name : "835호",
    address1 : "대양AI센터",
    address2 : "8층",
    isUsable : 1,
    maxUsers : 4,
    time : {
      open : "09:00",
      close : "18:00",
    },
    img : "https://example.com/img.jpg",
}
*/
