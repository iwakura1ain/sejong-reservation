//
// ModifyRservationForm
//
// ** Rsv : "R" e "s" er "v" ation

import { reactive } from 'vue';

// ==== common ====================================================================
// 모든 회의에 공통적으로 적용되는 내용
// (schema)
// {
// 	roomId : Int,
// 	topic : String(100Byte), // 최대 100바이트 문자열
// 	members : [ {name: String, email: String}],
// }
const common = reactive({
	origin: {
		topic: '', // 회의 주제
		members: [
			// 회의 참여자 (예약자 제외)
			// {
			// 	name: '', //
			// 	email: '',
			// },
		],
		roomId: 0, // 사용자가 선택한 회의실 id
	},
	toBeChanged: {
		topic: '',
		members: [],
		roomId: 0,
	},
});

// ========================================================================
// 개별 예약들의 배열
// - reservations : 수정 가능한 예약들

// 예약객체 스키마
// {
// 		id : Int,
// 		conflict : Boolean | null,
// 		origin : {
// 				date : String, // YYYY-MM-dd
// 				startTime : String, // HH:mm
// 				endTime : String, // HH:mm
// 		},
// 		toBeChanged : {
// 				date : String, // YYYY-MM-dd
// 				startTime : String, // HH:mm
// 				endTime : String, // HH:mm
// 		},

// }
const reservations = reactive([
	// {
	// 	id : 1,
	// 	conflict : false,
	// 	origin : {  },
	// 	toBeChanged : {  },
	// }
]);

// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------

function checkTopicAndMembersFormValid() {
	let regex = new RegExp('[a-z0-9]+@[a-z0-9]+.[a-z0-9]');

	common.toBeChanged.topic = common.toBeChanged.topic.trim();
	if (!common.toBeChanged.topic) {
		return { status: false, msg: 'EMPTY_TOPIC' };
	}

	if (common.toBeChanged.topic.length > 100) {
		return { status: false, msg: 'LONG_TOPIC' };
	}

	const len = common.toBeChanged.members.length;
	for (let i = 0; i < len; i++) {
		common.toBeChanged.members[i].name =
			common.toBeChanged.members[i].name.trim();
		common.toBeChanged.members[i].email =
			common.toBeChanged.members[i].email.trim();

		const name = common.toBeChanged.members[i].name;
		const email = common.toBeChanged.members[i].email;

		if (!name || !email) {
			return { status: false, msg: 'EMPTY_MEMBER' };
		}
		if (!regex.test(email)) {
			return { status: false, msg: 'INVALID_EMAIL_FORMAT' };
		}
	}

	return { status: true };
}

function clear() {
	common.toBeChanged.roomId = 0;
	common.toBeChanged.topic = '';
	common.toBeChanged.members = [];
	common.origin.roomId = 0;
	common.origin.topic = '';
	common.origin.members = [];
	reservations.splice(0);
}

// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------

const history = {
	detailId: -1,
	reservationType: '',
};

export const updateRsvFormStore = {
	common,
	reservations,
	// disabledReservations,
	checkTopicAndMembersFormValid,
	clear,
	history,
};
