<template>
	<div id="update-reservation-view">
		<section-header>예약 수정하기</section-header>

		<!-- 주제, 예약자 수정 -->
		<div class="topic-member-editor-container">
			<section-header size="small">주제/참여자 정보 수정</section-header>
			<topic-member-editor></topic-member-editor>
		</div>

		<!-- 회의실 수정 -->
		<div class="room-editor-container">
			<section-header size="small">회의실 수정</section-header>
			<room-selector v-model="updateRsvFormStore.common.toBeChanged.roomId" />
		</div>

		<!-- <div class="datetime-section"> -->
		<!-- 회의실 예약현황 달력 -->
		<!-- <div class="datetime-section-child"> -->
		<div>
			<div style="display: flex; align-items: center; flex-direction: column">
				<section-header size="small">회의실 예약현황</section-header>
				<RoomCalendar
					v-model:is-opened="isCalendarOpened"
					:fetch-trigger="updateRsvFormStore.common.toBeChanged"
					:room-id="updateRsvFormStore.common.toBeChanged.roomId"
				/>
			</div>
		</div>

		<!-- 일정 수정 -->
		<!-- <div class="datetime-section-child datetime-editor-container"> -->
		<div class="datetime-editor-container">
			<section-header size="small">일정 수정</section-header>
			<datetime-editor :parent-init-completed="initCompleted"></datetime-editor>
		</div>
		<!-- </div> -->
	</div>
</template>

<script setup>
import { ref } from 'vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import DatetimeEditor from '@/layouts/UpdateReservation/DatetimeEditor.vue';
import TopicMemberEditor from '@/layouts/UpdateReservation/TopicMemberEditor.vue';
import RoomSelector from '@/components/RoomSelector.vue';
import RoomCalendar from '@/components/RoomCalendar.vue';
import { reservationService } from '@/assets/scripts/requests/request.js';
import { updateRsvFormStore } from '@/stores/updateRsvForm.js';
import { userTokenStore } from '@/stores/userToken.js';
import { loadingStore } from '@/stores/loading.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

const initCompleted = ref(false);
const isCalendarOpened = ref(true);
// 초기화 ----------------------------------------
const historyState = {
	// disabledIds: history.state.disabledIds,
	includedIds: history.state.includedIds,
	reservationType: history.state.reservationType,

	// ReservationDetail로 되돌아갈때 사용
	detailId: history.state.detailId,
};

async function init() {
	try {
		loadingStore.start();
		updateRsvFormStore.clear();
		updateRsvFormStore.history.detailId = historyState.detailId;
		updateRsvFormStore.history.reservationType = historyState.reservationType;

		await fetchRsvs();
		// updateRsvFormStore.disabledIds = historyState.disabledIds;

		initCompleted.value = true;
	} catch (err) {
		console.error(err);
	} finally {
		loadingStore.stop();
	}
}
init();

// 일반함수 ----------------------------------------

async function fetchRsvs() {
	try {
		const accessToken = userTokenStore.getAccessToken();

		// 예약 가져오기
		// -- 단건예약인 경우
		if (historyState.reservationType === null) {
			const res = await reservationService.getById(
				historyState.includedIds[0],
				accessToken,
			);
			if (!res.status) {
				console.error(res);
				throw new Error(res);
			}
			const { topic, members, roomId } = res.data;
			updateRsvFormStore.common.origin.topic = topic;
			updateRsvFormStore.common.origin.members = [...members];
			updateRsvFormStore.common.origin.roomId = roomId;
			updateRsvFormStore.common.toBeChanged.topic = topic;
			updateRsvFormStore.common.toBeChanged.members = [...members];
			updateRsvFormStore.common.toBeChanged.roomId = roomId;

			updateRsvFormStore.reservations.push({
				id: res.data.id,
				conflict: null,
				origin: { ...res.data.meetingDatetime },
				toBeChanged: { ...res.data.meetingDatetime },
			});
		}
		// -- 정기예약인 경우
		else {
			// 유효한(시작시각이 아직 지나지 않은) 예약 불러오기
			const promises = historyState.includedIds.map(id =>
				reservationService.getById(id, accessToken),
			);
			await Promise.all(promises).then(responses => {
				const { topic, members, roomId } = {
					...responses[responses.length - 1].data,
				};
				updateRsvFormStore.common.origin.topic = topic;
				updateRsvFormStore.common.origin.members = [...members];
				updateRsvFormStore.common.origin.roomId = roomId;
				updateRsvFormStore.common.toBeChanged.topic = topic;
				updateRsvFormStore.common.toBeChanged.members = [...members];
				updateRsvFormStore.common.toBeChanged.roomId = roomId;

				for (let res of responses) {
					if (!res.status) {
						console.error(res);
						throw new Error(res);
					}
					updateRsvFormStore.reservations.push({
						id: res.data.id,
						conflict: null,
						origin: { ...res.data.meetingDatetime },
						toBeChanged: { ...res.data.meetingDatetime },
					});
				}
			});

			// // 의미없는(시작시각이 이미 지난) 예약 불러오기
			// const disabledRsvPromises = historyState.disabledIds.map(id =>
			// 	reservationService.getById(id, accessToken),
			// );
			// await Promise.all(disabledRsvPromises).then(responses => {
			// 	for (let res of responses) {
			// 		if (!res.status) {
			// 			console.error(res);
			// 			throw new Error(res);
			// 		}
			// 		updateRsvFormStore.disabledReservations.push({
			// 			id: res.data.id,
			// 			...res.data.meetingDatetime,
			// 		});
			// 	}
			// });
		}
	} catch (err) {
		console.error(err);
		makeToast('예약을 가져오는 중 문제가 발생했습니다', 'error');
	}
}

//-------------------------------------------------------------------------
//-------------------------------------------------------------------------
</script>

<style lang="scss" scoped>
#update-reservation-view {
	.topic-member-editor-container,
	.room-editor-container,
	.datetime-editor-container {
		// width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	// .datetime-section {
	// 	width: 100%;
	// 	display: flex;
	// 	flex-wrap: wrap;
	// 	align-items: flex-start;
	// 	margin-top: 24px;
	// 	.datetime-section-child {
	// 		display: flex;
	// 		flex: 1;
	// 		flex-direction: column;
	// 		justify-content: center;
	// 		padding: 0 24px;
	// 	}
	// }
	// @media (max-width: 1280px) {
	// 	.datetime-section {
	// 		flex-direction: column;
	// 		align-items: center;
	// 		width: fit-content;
	// 	}
	// }
}
</style>
