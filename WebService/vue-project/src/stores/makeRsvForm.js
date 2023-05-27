// MakeReservationFromStore
// ** Rsv : "R" e "s" er "v" ation

import { reactive, computed } from 'vue';
import getTodayZeroHour from '@/assets/scripts/utils/getTodayZeroHour.js';
import { REPEAT_END_TYPE, REPEAT_INTERVAL_TYPE } from '@/assets/constants.js';

// * 사용하는 곳 : 이 Store는 'src/views/user/MakeReservationView.vue'와 'src/layouts/MakeReservation/'에서 사용함
// * getter, setter : 별도 getter, setter는 제공하지 않으며, 값에 직접 접근하여 get, set함
// * 전체 schema
// {
//  formStep : Int, // 1~5
// 	common : {
// 			roomId : Int,
// 			useRepeat : Boolean,
// 			startDate : Date,

// 			topic : String(100Byte),
// 			members : [ {name: String, email: String}],
// 			repeatOption : {
// 				interval : Int,
// 				endType : Int,
// 				endReps : Int,
// 				endDate : Date,
// 	},
// 	defaultTime: {
// 		start: { HH: String(2Byte), mm: String(2Byte) }, // HH, mm은 두 자리 String (e.g., "09")
// 		end: { HH: String(2Byte), mm: String(2Byte) },
// 	},
// 	each : {
// 		date : Date,
// 		time : { HH: String(2Byte), mm: String(2Byte) }, // HH, mm은 두 자리 문자열 (e.g., "09")
// 		conflict : Boolean | Null,
// 		include : Boolean,
// 	}
// }

// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------

// ==== formState ==================================================================
// 예약생성 form 전체를 관리하기 위한 상태
const formState = reactive({
	step: 1,
	// 1:회의실 선택, 2:일반 일정 선택, 3:세부 일정 선택,
	// 4:주제&참여자 입력, 5:최종검토 및 예약생성
});

// ==== common ====================================================================
// 모든 회의에 공통적으로 적용되는 내용
//
// (schema)
// {
// 	roomId : Int,
// 	useRepeat : Boolean,
// 	startDate : Date,

// 	topic : String(100Byte), // 최대 100바이트 문자열
// 	members : [ {name: String, email: String}],
// 	repeatOption : {
// 		interval : Int, // 0:MONTH, 1:WEEK, 2:DAY (매월, 매주, 매일)
// 		endType : Int, // 0:반복횟수, 1:종료날짜 -- startDate로부터 365일 뒤 날짜까지만 되도록 관리
// 		endReps : Int, // 1 ~ 366
// 		endDate : Date, // startDate로부터 365일 뒤 날짜
// 		// 								(2022년이 365일이라고 가정하면, startDate가 2022-01-01일 때 endDate는 2022-01-01 ~ 2023-01-01 사이 지정 가능 )
// 	}
// }
const common = reactive({
	roomId: 0, // 사용자가 선택한 회의실 id
	useRepeat: false, // false : 단건예약, true : 정기예약
	startDate: getTodayZeroHour(), // 단건예약의 회의날짜 / 정기예약의 첫 회의날짜

	topic: '', // 회의 주제
	members: [
		// 회의 참여자 (예약자 제외)
		// {
		// 	name: '', //
		// 	email: '',
		// },
	],

	repeatOption: {
		interval: REPEAT_INTERVAL_TYPE.MONTH,
		endType: REPEAT_END_TYPE.REPS,
		endReps: 1,
		endDate: getTodayZeroHour(),
	},
});

// ==== defaultTime ====================================================================
// 기본(default) 회의시간을 의미함
// 이 시간정보로 일단 each배열의 각 예약객체의 time값을 채움
// 사용자가 예외처리를 해 각 객체의 time값이 바뀌면 바뀐 그 값을 따름 (commonTime은 무시)
//
// (예시) :
// 1. 사용자가 2023-01-01에 예약을 하려고 한다.
// 2. commonTime의 값으로 start를 09:00, end를 12:00으로 설정했다.
// 3. 2023-01-01날짜에 대한 예약객체는 each[1]자리에 삽입되었다.
// 4. 이후 each[1]에 대해 예외처리를 해 start를 11:00으로 바꾸었다
// 5. 이 경우 2023-01-01의 예약 시간은 11:00~12:00이 된다.
//
// (schema)
// {
//  start: { HH: String(2Byte), mm: String(2Byte) }, // HH, mm은 두 자리 String (e.g., "09")
// 	end: { HH: String(2Byte), mm: String(2Byte) },
// }
const defaultTime = reactive({
	start: { HH: '', mm: '' },
	end: { HH: '', mm: '' },
});

// ==== each ====================================================================
// common를 바탕으로 만든 각 날짜별 예약의 배열
// 이 데이터에 대해 사용자가 예외처리(시간변경, 제외)함
// 예외처리 완료된 eachData와 commonData를 결합해 실제 예약 생성
//
// (element의 schema)
// {
// 	date : Date,
//  time : {
//  	start: { HH: String(2Byte), mm: String(2Byte) }, // HH, mm은 두 자리 String (e.g., "09")
// 		end: { HH: String(2Byte), mm: String(2Byte) },
// 	}
// 	conflict : Boolean|Null, // true:예약불가(충돌), false:예약가능(충돌없음), null:알수없음(초기값)
// 	include : Boolean, // true:예약할 것, false:예약하지 않을 것(제외)
// }
const each = reactive([
	// { // example data
	// 	date : new Date(),
	// 	time : { start : { HH: '13', mm: '18' }, end : { HH: '18', mm: '10' } },
	// 	include : true,
	// 	conflict : false,
	// },
]);

// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------

const isGeneralFormRequirementFulfilled = computed(() => {
	if (makeRsvFormStore.common.useRepeat) {
		return (
			makeRsvFormStore.common.startDate &&
			makeRsvFormStore.defaultTime.start.HH &&
			makeRsvFormStore.defaultTime.start.mm &&
			makeRsvFormStore.defaultTime.end.HH &&
			makeRsvFormStore.defaultTime.end.mm &&
			makeRsvFormStore.common.repeatOption.interval &&
			(makeRsvFormStore.common.repeatOption.endReps ||
				makeRsvFormStore.common.repeatOption.endDate)
		);
	} else {
		return (
			makeRsvFormStore.common.startDate &&
			makeRsvFormStore.defaultTime.start.HH &&
			makeRsvFormStore.defaultTime.start.mm &&
			makeRsvFormStore.defaultTime.end.HH &&
			makeRsvFormStore.defaultTime.end.mm
		);
	}
});

function checkMeetingInfoFormValid() {
	let valid = true;
	let regex = new RegExp('[a-z0-9]+@[a-z0-9]+.[a-z0-9]');

	makeRsvFormStore.common.topic = makeRsvFormStore.common.topic.trim();
	if (!makeRsvFormStore.common.topic) {
		valid = false;
		console.log(valid);
		return valid;
	}

	const len = makeRsvFormStore.common.members.length;
	for (let i = 0; i < len; i++) {
		makeRsvFormStore.common.members[i].name =
			makeRsvFormStore.common.members[i].name.trim();
		makeRsvFormStore.common.members[i].email =
			makeRsvFormStore.common.members[i].email.trim();

		const name = makeRsvFormStore.common.members[i].name;
		const email = makeRsvFormStore.common.members[i].email;

		if (!name || !email) {
			valid = false;
			break;
		}
		if (!regex.test(email)) {
			valid = false;

			break;
		}
	}
	console.log(valid);
	return valid;
}

function clear() {
	formState.step = 1;
	common.roomId = 0;
	common.useRepeat = false;
	common.startDate = getTodayZeroHour();
	common.topic = '';
	common.members = [];
	common.repeatOption.interval = REPEAT_INTERVAL_TYPE.MONTH;
	common.repeatOption.endType = REPEAT_END_TYPE.REPS;
	common.repeatOption.endReps = 1;
	common.repeatOption.endData = getTodayZeroHour();
	defaultTime.start.HH = '';
	defaultTime.start.mm = '';
	defaultTime.end.HH = '';
	defaultTime.end.mm = '';
	this.each.splice(0);
}

// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------

export const makeRsvFormStore = {
	formState,
	common,
	defaultTime,
	each,
	isGeneralFormRequirementFulfilled,
	checkMeetingInfoFormValid,
	clear,
};

// 참고 : DB Reservation 테이블 (2023-05-25 main branch 기준)
// CREATE TABLE Reservation (
// 	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
// 	is_valid BOOLEAN NOT NULL DEFAULT 1,
// 	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
// 	reservation_code VARCHAR(8) NOT NULL,
// 	reservation_type VARCHAR(12) DEFAULT NULL,
// 	reservation_topic VARCHAR(100) DEFAULT '',
// 	reservation_date DATE NOT NULL,
// 	start_time TIME NOT NULL,
// 	end_time TIME NOT NULL,
// 	room_id INT NOT NULL,
// 	CONSTRAINT reservation_to_room
// 	FOREIGN KEY (room_id) REFERENCES Room(id)
// 	ON UPDATE CASCADE
// 	ON DELETE CASCADE,
// 	creator_id VARCHAR(10) NOT NULL,
// 	CONSTRAINT reservation_to_user
// 	FOREIGN KEY (creator_id) REFERENCES User(id)
// 	ON UPDATE CASCADE
// 	ON DELETE CASCADE,
// 	members JSON NOT NULL DEFAULT '{}'
// 	CHECK (JSON_VALID(members)),
// 	room_used BOOLEAN NOT NULL DEFAULT 0
// ) DEFAULT CHARSET=utf8;
