import { reactive } from 'vue';

export const fetchedRoomStore = reactive({
	data: [],
	init: function () {
		this.data = [];
	},
	setAll: function (rooms) {
		this.data = rooms;
	},
	getAll: function () {
		return this.data;
	},
	getById: function (id) {
		return this.data.find(elem => elem.id === id);
	},
});

// 데이터 스키마 : 아래 파일의 '프론트엔드 데이터 스키마'참고
// src/assets/scripts/requests/responseConverters/convertRoomRes.js

// 아래에 옮겨둠.

// -----------------------------
// 프론트엔드 데이터 스키마
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

// 프론트엔드 데이터 예시
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
