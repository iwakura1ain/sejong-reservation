<template>
	<div id="reservation-detail-view">
		<section-header>예약 내역 상세</section-header>
		<div>
			<filled-button color="white" @click="handleGoPreviousPage">
				돌아가기
			</filled-button>
		</div>

		<!-- 기본 정보 -->
		<section-header size="small">기본 정보</section-header>
		<div class="control-section common-data">
			<filled-button @click="handleModifyCommonData">
				기본 정보 수정
			</filled-button>
		</div>
		<div class="contents-section common-data">
			<div class="field-set topic">
				<p class="label">주제</p>
				<p class="content">{{ reservationCommonField.topic }}</p>
			</div>
			<div class="field-set reservation-type">
				<p class="label">예약 유형</p>
				<p class="content">{{ !reservationType ? '단건예약' : '정기예약' }}</p>
			</div>
			<div class="field-set meeting-room">
				<p class="label">회의실</p>
				<p class="content">{{ roomStr }}</p>
			</div>

			<div class="field-set members">
				<p class="label">
					참여자
					<span class="member-num" style="font-weight: bold">
						{{ reservationCommonField.members.length + 1 }}명
					</span>
				</p>
				<div class="content-container">
					<p class="content member creator">
						{{ userStore.getInfo().name }} {{ userStore.getInfo().email }}
					</p>
					<p
						v-for="(member, index) in reservationCommonField.members"
						:key="index"
						class="content member"
					>
						{{ member.name }} {{ member.email }}
					</p>
				</div>
			</div>

			<div class="field-set created-at">
				<p class="label">예약 생성일시</p>
				<p class="content">{{ createdAtKorStr }}</p>
			</div>
		</div>

		<!-- 시간 정보 -->
		<section-header size="small">일정</section-header>
		<div>{{ reservationData.length }} {{ selectedReservationIds.length }}</div>
		<!-- 전체선택/해제 -->
		<div class="control-section time-data">
			<template v-if="!showDeleteConfirm">
				<div
					v-if="selectedReservationIds.length < reservationDataFromNow.length"
				>
					<filled-button @click="handleSelectAllRsvItem">
						전체선택
					</filled-button>
				</div>
				<div v-else>
					<filled-button @click="handleUnselectAllRsvItem" color="white">
						선택해제
					</filled-button>
				</div>
				<!-- 수정/삭제 -->
				<div v-if="selectedReservationIds.length > 0">
					<filled-button @click="handleModifyTimeData">
						{{ selectedReservationIds.length }}건 수정
					</filled-button>
					<filled-button @click="toggleShowDeleteConfirm">
						{{ selectedReservationIds.length }}건 삭제
					</filled-button>
				</div>
				<div v-else>
					<filled-button color="disabled"> 0건 수정 </filled-button>
					<filled-button color="disabled"> 0건 삭제 </filled-button>
				</div>
			</template>
			<!-- 삭제확인 -->
			<div v-if="showDeleteConfirm">
				<filled-button color="white" @click="toggleShowDeleteConfirm">
					취소
				</filled-button>
				<filled-button @click="handleDeleteReservation">삭제</filled-button>
				<span style="margin-left: 4px">정말로 지울까요?</span>
			</div>
		</div>

		<!-- 종료시각이 현재보다 이전 : reservationDataBeforeNow -->
		<div class="contents-section datetime-contents">
			<div
				v-for="(item, index) in reservationDataBeforeNow"
				:key="index"
				class="content-container reservation-item-disabled"
			>
				<check-box :disabled="true" />
				<div class="values">
					<span class="content date">
						{{ getDateStringWithDow(item.meetingDatetime.date) }}
					</span>
					<span class="content time">
						{{
							`${item.meetingDatetime.startTime}-${item.meetingDatetime.endTime}`
						}}
					</span>

					<!-- no show 여부 : 이용안함(노쇼), 이용예정 -->
					<span
						v-if="item.roomUsed"
						class="content is-used"
						style="color: green"
					>
						🟢이용완료
					</span>
					<span v-else class="content is-used" style="color: red">
						🔴이용안함
					</span>
				</div>
			</div>
			<!-- 종료시각이 현재와 같거나 이후 reservationDataFromNow -->
			<div
				v-for="(item, index) in reservationDataFromNow"
				:key="index"
				class="content-container reservation-item"
				@click="handleClickRsvItem(item.id)"
			>
				<check-box :checked="selectedReservationIds.includes(item.id)" />
				<div class="values">
					<span class="content date">
						{{ getDateStringWithDow(item.meetingDatetime.date) }}
					</span>
					<span class="content time">
						{{
							`${item.meetingDatetime.startTime}-${item.meetingDatetime.endTime}`
						}}
					</span>

					<!-- no show 여부 : 이용완료, 이용예정 -->
					<span
						v-if="item.roomUsed"
						class="content is-used"
						style="color: green"
					>
						🟢이용완료
					</span>
					<span v-else class="content is-used" style="color: grey">
						⚪이용예정
					</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { useRouter } from 'vue-router';

import SectionHeader from '@/components/atoms/SectionHeader.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import CheckBox from '@/components/atoms/CheckBox.vue';
import { reservationService } from '@/assets/scripts/requests/request.js';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { userStore } from '@/stores/user.js';

import getDayofWeek from '@/assets/scripts/utils/getDayofWeek.js';

// 초기화 1/2 : 상태, computed 정의------------------
const isThereNoReservation = ref(false);

const reservationData = ref([]); // array
const reservationDataBeforeNow = computed(() => {
	// 회의 종료시각이 현재보다 이전인 reservationData
	return reservationData.value.filter(rsv =>
		endTimeIsOvered(rsv.meetingDatetime),
	);
});
const reservationDataFromNow = computed(() => {
	// 회의 종료시각이 현재와 같거나 이후인 reservationData
	return reservationData.value.filter(
		rsv => !endTimeIsOvered(rsv.meetingDatetime),
	);
});

const reservationCommonField = ref({
	topic: '',
	createdAt: '', // YYYY-MM-DD HH:mm:ss
	members: [], // [ {name:String, email:String} ]
	roomInfo: {
		address1: '',
		address2: '',
		name: '',
	},
});

const selectedReservationIds = ref([]);
const showDeleteConfirm = ref(false); // false:삭제확인창 닫힘, true:열림

const roomStr = computed(() => {
	const { address1, address2, name } = reservationCommonField.value.roomInfo;
	return `${address1} ${address2} ${name}`;
});
const createdAtKorStr = computed(() => {
	const date = reservationCommonField.value.createdAt.date;
	const time = reservationCommonField.value.createdAt.time;
	const dow = getDayofWeek(date);
	return `${date}(${dow}) ${time}`;
});

let sampledReservation = null;

// 초기화 2/2 : 일반 변수, init호출 --------------
const historyState = {
	id: history.state.id,
	reservationType: history.state.reservationType,
};
const router = useRouter();

init();

// 상태 감시 ------------------
watch(
	selectedReservationIds,
	() => {
		showDeleteConfirm.value = false;
	},
	{ deep: true },
);

// 일반 함수 ------------------

async function fetchSingleReservation(id) {
	// 단건예약을 불러오는 함수
	// 인수 : reservation의 id
	// 결과 : reservationData에 Object가 대입됨.
	try {
		const res = await reservationService.getById(id);
		if (res.status) {
			reservationData.value = [res.data];
			sampledReservation = res.data;
		}
	} catch (err) {
		alert('단건 예약을 불러오는 중 문제가 생겼습니다.');
		console.error(err);
	}
}

async function fetchRegularReservation(rt) {
	// 정기예약을 불러오는 함수
	// 인수 : reservationType
	// 결과 : reservationData에 Object의 배열의 대입됨.
	try {
		// const res = await reservationService.get({
		// 	reservationType: rt,
		// });
		// ▼ T E S T
		const res = reservationService.TEST_GET_REGULAR_MAXIMIZED_RSV({
			reservationType: rt,
		});
		// ▲ T E S T
		if (res.status) {
			reservationData.value = res.data;
			if (res.data.length <= 0) {
				return;
			}
			sampledReservation = res.data[0];
		}
	} catch (err) {
		alert('정기예약 내역을 불러오는 중 문제가 생겼습니다.');
		console.error(err);
	}
}

function getDateStringWithDow(dateStr) {
	const dow = getDayofWeek(dateStr);
	return `${dateStr}(${dow})`;
}

function endTimeIsOvered({ date, endTime }) {
	const nowDate = new Date();
	const endTimeDate = new Date(`${date}T${endTime}:00`);
	return endTimeDate < nowDate;
}

async function init() {
	// ReservationDetailView 초기화함수
	console.log(historyState);
	selectedReservationIds.value = [];
	showDeleteConfirm.value = false;

	// 예약 fetching & reservationData 채우기
	// sampledReservation 설정
	if (historyState.reservationType) {
		// 정기예약이면
		await fetchRegularReservation(historyState.reservationType);
	} else if (historyState.id || historyState.id === 0) {
		// 단건예약이면
		await fetchSingleReservation(historyState.id);
	} else {
		// id가 유효한 값이 아니면 (e.g., null, Nan)
		console.error('[ReservationDetailView] 올바르지 않은 router query');
		router.push({ name: 'NotFound' });
		return;
	}

	// sampledReservation으로 reservationCommonField 채우기
	if (!sampledReservation) {
		isThereNoReservation.value = true;
		console.error('예약이 없습니다');
		return;
	}
	reservationCommonField.value.topic = sampledReservation.topic;
	reservationCommonField.value.createdAt = sampledReservation.createdAt;
	reservationCommonField.value.members = sampledReservation.members;

	const room = fetchedRoomStore.value.getById(sampledReservation.roomId);
	reservationCommonField.value.roomInfo.address1 = room.address1;
	reservationCommonField.value.roomInfo.address2 = room.address2;
	reservationCommonField.value.roomInfo.name = room.name;

	console.log(reservationCommonField.value);
}

// 이벤트 핸들러 ----------------------
function handleGoPreviousPage() {
	router.go(-1);
}

function handleModifyCommonData() {
	router.push({
		name: 'ModifyReservationCommonData',
		state: {
			// 단건예약 : reservationIds의 길이 1, reservationType은 null
			// 정기예약 : reservationIds의 길이 1이상, reservatioType은 Striing.
			reservationIds: reservationData.value.map(item => item.id),
			reservationType: historyState.reservationType,
		},
	});
}

function handleModifyTimeData() {
	const mapped = selectedReservationIds.value.map(item => item);
	mapped.sort(function (a, b) {
		return a - b;
	});
	router.push({
		name: 'ModifyReservationTimeData',
		state: {
			// 단건예약 : reservationIds의 길이 1
			// 정기예약 : reservationIds의 길이 1이상
			reservationIds: mapped,
		},
	});
}

function toggleShowDeleteConfirm() {
	showDeleteConfirm.value = !showDeleteConfirm.value;
}
function handleDeleteReservation() {
	alert('삭제 : ' + selectedReservationIds.value);
	init();
}

function handleSelectAllRsvItem() {
	selectedReservationIds.value = reservationDataFromNow.value.map(item => {
		return item.id;
	});
}
function handleUnselectAllRsvItem() {
	selectedReservationIds.value = [];
}

function handleClickRsvItem(id) {
	if (selectedReservationIds.value.includes(id)) {
		const idx = selectedReservationIds.value.indexOf(id);
		selectedReservationIds.value.splice(idx, 1);
	} else {
		selectedReservationIds.value.push(id);
	}
	console.log(selectedReservationIds.value);
}
</script>

<style lang="scss" scoped>
#reservation-detail-view {
	.control-section {
		width: 100%;
		margin-bottom: 24px;
		display: flex;
	}
	.contents-section {
		width: 100%;
		display: flex;
		flex-direction: column;
		.field-set {
			padding: 4px;
			margin-bottom: 12px;
			.label {
				font-weight: bold;
				margin-bottom: 4px;
			}
			.content {
				padding: 4px 0;
			}
		}

		.reservation-item,
		.reservation-item-disabled {
			display: flex;
			// flex-wrap: wrap;
			width: fit-content;
			align-items: center;
			padding: 4px;
			cursor: pointer;
			.values {
				display: flex;
				flex-wrap: wrap;
				align-items: center;
				padding-top: 2px;
				margin-left: 8px;
				// text-align: right;
				.date,
				.time {
					margin-right: 4px;
				}
			}

			transition: all 0.2s;
			&:hover {
				border-radius: $box-radius;
				background-color: $sejong-grey-20;
			}
		}
		.reservation-item-disabled {
			opacity: 50%;
			cursor: not-allowed;
			transition: none;
			&:hover {
				background-color: transparent;
			}
		}
	}
}
</style>
