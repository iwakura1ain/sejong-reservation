import { ref } from 'vue';

const fetchedReservationStore = ref({
	data: [],

	init: function () {},
	set: function (rawReservations) {},
	getAll: function () {},
	getById: function (id) {
		// id : 정수. 개별예약 아이디.
	},
	getByReservationGroupId: function (reservationGroupId) {
		// reservationGroupId : 정수. 정기예약 아이디.
	},
	getByMonth: function (month) {
		// month : 정수. 월. (1월은 1, 12월은 12)
	},
});

// data의 원소 스키마
/*
{
}
*/

// rawReservations의 원소 스키마
/*
{
}
*/
