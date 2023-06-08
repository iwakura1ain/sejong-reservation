<template>
	<div class="datetime-editor">
		<div class="control-section">
			<!-- 수정/삭제 -->
			<div v-if="selectedIdx.length > 0" class="modify-btn-container">
				<div>
					<filled-button @click="handleOpenModify('date')">
						{{ selectedIdx.length }}건 날짜수정
					</filled-button>
					<filled-button @click="handleOpenModify('time')">
						{{ selectedIdx.length }}건 시간수정
					</filled-button>
				</div>
			</div>
			<div v-else class="modify-btn-container">
				<div>
					<filled-button color="disabled"> 0건 날짜수정 </filled-button>
					<filled-button color="disabled"> 0건 시간수정 </filled-button>
				</div>
			</div>

			<!-- 수정 컨테이너 -->
			<div v-if="modifyContainerShow" class="modify-container">
				<div v-if="modifyContainerMode === 'date'" class="modify-date">
					<span class="label">날짜 수정</span>
					<div class="picker">
						<vue3-datepicker-wrapper v-model="newDate" />
					</div>
					<div class="btn-group">
						<filled-button color="white" @click="handleCloseModify">
							취소
						</filled-button>
						<filled-button @click="handleModifyDate">적용</filled-button>
					</div>
				</div>
				<div v-if="modifyContainerMode === 'time'" class="modify-time">
					<span class="label">시간 수정</span>
					<div class="picker">
						<vue3-timepicker-wrapper
							v-model="newTime.start"
							placeholder="시작하는 시각"
						/>
						<div>
							<span class="range-mark">~</span>
							<vue3-timepicker-wrapper
								v-model="newTime.end"
								placeholder="끝나는 시각"
							/>
						</div>
					</div>
					<div class="btn-group">
						<filled-button color="white" @click="handleCloseModify">
							취소
						</filled-button>
						<filled-button @click="handleModifyTime">적용</filled-button>
					</div>
				</div>
			</div>

			<!-- 선택 버튼 -->
			<div class="select-btn-container">
				<div class="all-select-btn">
					<text-button
						v-if="selectedIdx.length < updateRsvFormStore.reservations.length"
						@click="handleSelectAll"
					>
						전체선택
					</text-button>

					<filled-button v-else @click="handleUnselectAll" color="white">
						선택해제
					</filled-button>
				</div>
				<div class="rollback-btn">
					<filled-button
						v-if="selectedIdx.length > 0"
						color="white"
						@click="handleRollback"
					>
						{{ selectedIdx.length }}건 되돌리기
					</filled-button>
					<text-button v-else color="disabled"> 0건 되돌리기 </text-button>
				</div>
			</div>
		</div>

		<!-- 세부 일정 목록 -->
		<div class="contents-section">
			<div
				v-for="(item, index) in updateRsvFormStore.reservations"
				:key="index"
				class="content-container reservation-item"
				@click="handleClickRsvItem(index)"
			>
				<check-box :checked="selectedIdx.includes(index)" />
				<div class="values">
					<span class="content date">
						{{
							`${item.toBeChanged.date}(${getDayofWeek(item.toBeChanged.date)})`
						}}
					</span>
					<span class="content time">
						{{ `${item.toBeChanged.startTime}-${item.toBeChanged.endTime}` }}
					</span>
					<span class="content conflict" v-if="item.conflict !== null">
						{{ item.conflict ? '❌예약불가' : '✅예약가능' }}
					</span>
				</div>
			</div>
		</div>

		<section-header></section-header>
		<div class="submit-btn-container">
			<filled-button class="submit-btn" @click="handleSubmit">
				{{ `예약 수정하기` }}
			</filled-button>
		</div>
	</div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import Vue3DatepickerWrapper from '@/components/wrappers/Vue3DatepickerWrapper.vue';
import Vue3TimepickerWrapper from '@/components/wrappers/Vue3TimepickerWrapper.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextButton from '@/components/atoms/TextButton.vue';
import CheckBox from '@/components/atoms/CheckBox.vue';
import { reservationService } from '@/assets/scripts/requests/request.js';
import { updateRsvFormStore } from '@/stores/updateRsvForm.js';
import { loadingStore } from '@/stores/loading.js';
import { userTokenStore } from '@/stores/userToken.js';
import generateRange from '@/assets/scripts/utils/generateRange.js';
import getFormattedStringFromDateObj from '@/assets/scripts/utils/getFormattedStringFromDateObj.js';
import validateDateTime from '@/assets/scripts/utils/validateDateTime.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import getDayofWeek from '@/assets/scripts/utils/getDayofWeek.js';

// 상태, computed ------------

const selectedIdx = ref([]);
const newDate = ref(null);
const newTime = ref(null);

const modifyContainerShow = ref(false); // true, false
const modifyContainerMode = ref(null); // 'date','time'

const previousRoomId = ref(updateRsvFormStore.common.toBeChanged.roomId);
const props = defineProps({
	parentInitCompleted: {
		required: true,
		type: Boolean,
	},
});

// 초기화 --------------------
const router = useRouter();

// 상태감시
// 선택된 회의실 id가 변하면 예약가능여부 재검증
watch(
	() => props.parentInitCompleted,
	async () => {
		if (props.parentInitCompleted) {
			const arr = generateRange(updateRsvFormStore.reservations.length);
			await checkConflict(arr);
		}
	},
	{ immediate: true },
);

watch(updateRsvFormStore.common.toBeChanged, async newValue => {
	if (newValue.roomId === previousRoomId.value) {
		return;
	}
	previousRoomId.value = newValue.roomId;
	const arr = generateRange(updateRsvFormStore.reservations.length);
	await checkConflict(arr);
});

// 일반함수 -------------------
function buildConflictCheckReqBody(rsv) {
	// 충돌체크용
	return {
		reservation_date: rsv.toBeChanged.date,
		start_time: rsv.toBeChanged.startTime,
		end_time: rsv.toBeChanged.endTime,
		room_id: updateRsvFormStore.common.toBeChanged.roomId,
	};
}

function buildRollbackReqBody(rsv) {
	// 원상복구용
	return {
		reservation_date: rsv.origin.date,
		start_time: rsv.origin.startTime,
		end_time: rsv.origin.endTime,
		room_id: updateRsvFormStore.common.origin.roomId,
	};
}

function buildUpdateReqBody(rsv) {
	// 아직 시작시간이 지나지 않은 예약들에 대한 실제 update용
	return {
		reservation_date: rsv.toBeChanged.date,
		start_time: rsv.toBeChanged.startTime,
		end_time: rsv.toBeChanged.endTime,
		room_id: updateRsvFormStore.common.toBeChanged.roomId,
		members: updateRsvFormStore.common.toBeChanged.members,
		reservation_topic: updateRsvFormStore.common.toBeChanged.topic,
	};
}

function handleErrorMsg(res) {
	if (res.msg === 'Conflict in reservations') {
		makeToast('시간이 겹쳐 예약할 수 없는 항목이 있습니다', 'error');
	} else if (res.msg === 'reservation not in room open hours') {
		makeToast(`선택한 예약 시간이 회의실 운영시간을 벗어났습니다.`, 'error');
	} else if (res.msg === 'Invalid reservation') {
		makeToast(`형식에 적합하지 않은 입력값이 있습니다`, 'error');
	} else if (res.msg === 'User cannot reserve that far into future') {
		makeToast(
			`현재 사용자유형으로 선택할 수 없는 너무 먼 예약입니다.`,
			'error',
		);
	} else if (res.msg === 'Invalid room ID') {
		makeToast(`존재하지 않는 회의실입니다`, 'error');
	} else if (res.msg === 'Unauthenticated') {
		makeToast(`로그인 정보가 올바르지 않습니다`, 'error');
	} else if (res.msg === 'Reservation edit failed') {
		makeToast(`수정 권한이 없는 사용자입니다`, 'error');
	} else {
		makeToast('알 수 없는 오류입니다', 'error');
		console.error(res);
	}
}

async function checkConflict(targetIdxArr) {
	// 입력 : [0,1,3] -->  updateRsvFormStore.reservations의 0번, 1번, 3번에 대해서 검증하라는 뜻.
	try {
		loadingStore.start();
		let result = true;
		const accessToken = userTokenStore.getAccessToken();

		// 모든 예약이 생성 가능한지 확인 (patch 시도)
		// -- request body와 예약 id 모으기
		const reqs = updateRsvFormStore.reservations
			.map((rsv, index) => {
				if (targetIdxArr.includes(index)) {
					return {
						id: rsv.id,
						conflictCheckBody: buildConflictCheckReqBody(rsv),
						rollbackBody: buildRollbackReqBody(rsv),
					};
				}
			})
			.filter(rsv => rsv);

		// -- 요청날려서 정상응답 나오면 conflict=false, 비정상응답 나오면 conflict=true 마킹.
		const reqPromises = reqs.map(req => {
			return reservationService.update(
				req.id,
				req.conflictCheckBody,
				accessToken,
			);
		});
		await Promise.all(reqPromises)
			.then(responses => {
				let i = 0;
				let errorHandled = false;
				for (let res of responses) {
					const index = targetIdxArr[i];
					if (res.status) {
						updateRsvFormStore.reservations[index].conflict = false;
					} else {
						updateRsvFormStore.reservations[index].conflict = true;
						if (!errorHandled) {
							handleErrorMsg(res);
							errorHandled = true;
						}
						result = false;
					}
					i += 1;
				}
			})
			.catch(err => {
				console.error(err);
				makeToast('알 수 없는 오류입니다', 'error');
			});

		// -- 확인하느라 patch로 바꾼 내용들 원상복구
		const rollbackPromises = reqs.map(req => {
			return reservationService.update(req.id, req.rollbackBody, accessToken);
		});
		await Promise.all(rollbackPromises)
			.then(responses => {
				for (let res of responses) {
					if (!res.status) {
						console.error(res);
					}
				}
			})
			.catch(err => {
				console.error(err);
				makeToast('알 수 없는 오류입니다', 'error');
			});
		return result;
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);
	} finally {
		loadingStore.stop();
	}
}

// 이벤트핸들러 ----------------
function handleSelectAll() {
	const len = updateRsvFormStore.reservations.length;
	for (let i = 0; i < len; i++) {
		if (!selectedIdx.value.includes(i)) {
			selectedIdx.value.push(i);
		}
	}
}
function handleUnselectAll() {
	selectedIdx.value.splice(0);
}

async function handleRollback() {
	for (let idx of selectedIdx.value) {
		updateRsvFormStore.reservations[idx].toBeChanged = {
			...updateRsvFormStore.reservations[idx].origin,
		};
		updateRsvFormStore.reservations[idx].conflict = null;
	}
	handleUnselectAll();
	const arr = generateRange(updateRsvFormStore.reservations.length);
	await checkConflict(arr);
}

function handleClickRsvItem(index) {
	if (selectedIdx.value.includes(index)) {
		const idx = selectedIdx.value.indexOf(index);
		selectedIdx.value.splice(idx, 1);
	} else {
		selectedIdx.value.push(index);
	}
}

function handleOpenModify(mode) {
	// mode : 'date', 'time'
	modifyContainerMode.value = mode;

	const i = selectedIdx.value[0];
	if (mode === 'date') {
		newDate.value = new Date(
			updateRsvFormStore.reservations[i].toBeChanged.date,
		);
	} else if (mode === 'time') {
		const { startTime, endTime } =
			updateRsvFormStore.reservations[i].toBeChanged;
		const [startHH, startmm] = startTime.split(':');
		const [endHH, endmm] = endTime.split(':');

		newTime.value = {
			start: { HH: startHH, mm: startmm },
			end: { HH: endHH, mm: endmm },
		};
	}

	modifyContainerShow.value = true;
}

function handleCloseModify() {
	modifyContainerMode.value = null;
	modifyContainerShow.value = false;
}

async function handleModifyDate() {
	try {
		const dateStr = getFormattedStringFromDateObj(newDate.value, 'YYYY-MM-DD');
		selectedIdx.value.map(idx => {
			updateRsvFormStore.reservations[idx].toBeChanged.date = dateStr;
		});
		console.log(selectedIdx.value);
		const res = await checkConflict(selectedIdx.value);
		if (res) {
			handleUnselectAll();
			handleCloseModify();
			makeToast('이 날짜로 변경이 가능합니다', 'info');
		}
	} catch (err) {
		console.error(err);
	}
}

async function handleModifyTime() {
	try {
		for (let idx of selectedIdx.value) {
			if (
				!validateDateTime(
					new Date(updateRsvFormStore.reservations[idx].toBeChanged.date),
					newTime.value,
				)
			) {
				return;
			}
		}

		for (let idx of selectedIdx.value) {
			const { start, end } = newTime.value;
			updateRsvFormStore.reservations[
				idx
			].toBeChanged.startTime = `${start.HH}:${start.mm}`;
			updateRsvFormStore.reservations[
				idx
			].toBeChanged.endTime = `${end.HH}:${end.mm}`;
		}

		const res = await checkConflict(selectedIdx.value);
		if (res) {
			handleUnselectAll();
			handleCloseModify();
			makeToast('이 시간으로 변경이 가능합니다', 'info');
		}
	} catch (err) {
		console.error(err);
	}
}

async function handleSubmit() {
	try {
		loadingStore.start();

		// 주제, 참여자 검증
		const infoValid = updateRsvFormStore.checkTopicAndMembersFormValid();
		if (!infoValid.status) {
			const msg = infoValid.msg;
			if (msg === 'EMPTY_TOPIC') {
				makeToast('회의 주제 항목이 비었습니다', 'error');
			} else if (msg === 'EMPTY_MEMBER') {
				makeToast('참여자 항목이 비었습니다', 'error');
			} else if (msg === 'LONG_TOPIC') {
				makeToast('회의 주제는 최대 100자입니다', 'error');
			} else if (msg === 'INVALID_EMAIL_FORMAT') {
				makeToast(
					'이메일의 형식이 올바르지 않습니다 (sejong@example.com)',
					'error',
				);
			} else {
				makeToast('알 수 없는 오류입니다', 'error');
			}

			return;
		}

		// 실제 업데이트
		const accessToken = userTokenStore.getAccessToken();

		// 유의미한 예약들(아직 시작시각이 지나지 않은 예약들)에 대한 update
		const reqs = updateRsvFormStore.reservations
			.map(rsv => {
				return {
					id: rsv.id,
					reqBody: buildUpdateReqBody(rsv),
				};
			})
			.filter(rsv => rsv);

		const reqPromises = reqs.map(req =>
			reservationService.update(req.id, req.reqBody, accessToken),
		);
		await Promise.all(reqPromises)
			.then(responses => {
				let errorHandled = false;
				for (let res of responses) {
					if (!res.status && !errorHandled) {
						handleErrorMsg(res);
						errorHandled = true;
					}
					console.log(res);
				}
			})
			.catch(err => {
				console.error(err);
				makeToast('알 수 없는 오류입니다', 'error');
				throw new Error(err);
			});

		// 의미없는 예약들(시작시각이 이미 지난 예약들)에 대한 update
		// console.log(updateRsvFormStore.disabledIds);
		// const disabledReqs = updateRsvFormStore.disabledReservations
		// 	.map(rsv => {
		// 		return {
		// 			id: rsv.id,
		// 			reqBody: {
		// 				reservation_date: rsv.date,
		// 				start_time: rsv.startTime,
		// 				end_time: rsv.endTime,
		// 				room_id: updateRsvFormStore.common.toBeChanged.roomId,
		// 				members: updateRsvFormStore.common.toBeChanged.members,
		// 				reservation_topic: updateRsvFormStore.common.toBeChanged.topic,
		// 			},
		// 		};
		// 	})
		// 	.filter(rsv => rsv);
		// console.log(disabledReqs);
		// const disabledReqPromises = disabledReqs.map(req => {
		// 	return reservationService.update(req.id, req.reqBody, accessToken);
		// });
		// await Promise.all(disabledReqPromises)
		// 	.then(responses => {
		// 		let errorHandled = false;
		// 		for (let res of responses) {
		// 			if (!res.status && !errorHandled) {
		// 				handleErrorMsg(res);
		// 				errorHandled = true;
		// 			}
		// 		}
		// 	})
		// 	.catch(err => {
		// 		console.error(err);
		// 		makeToast('알 수 없는 오류입니다', 'error');
		// 		throw new Error(err);
		// 	});

		// 정리
		updateRsvFormStore.clear();
		router.push({
			name: 'ReservationDetail',
			state: {
				id: updateRsvFormStore.history.detailId,
				reservationType: updateRsvFormStore.history.reservationType,
				reservationUpdated: true,
			},
		});
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);
	} finally {
		loadingStore.stop();
	}
}
</script>

<style lang="scss" scoped>
.datetime-editor {
	width: 100%;
	.control-section {
		width: 100%;
		margin-bottom: 24px;
		display: flex;
		flex-direction: column;
		.select-btn-container {
			margin-top: 12px;
			display: flex;
			justify-content: flex-start;
			flex-wrap: wrap;
		}
		.modify-btn-container {
			display: flex;
			justify-content: flex-start;
			flex-wrap: wrap;
		}

		.modify-container {
			margin-top: 12px;
			> div {
				display: flex;
				flex-direction: column;
				align-items: flex-start;
			}
			.label {
				font-weight: bold;
			}
			.picker {
				margin: 8px 0;
			}
		}
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
			opacity: 40%;
			transition: none;
			margin-left: 24px;
			transition: all 0.2s;
			&:hover {
				background-color: transparent;
			}
		}
	}

	.submit-btn-container {
		text-align: center;
		.submit-btn {
			font-size: 1.5rem;
			padding: 24px;
		}
	}
}

@media (max-width: 768px) {
	.datetime-editor {
		font-size: 0.9rem;
		.control-section {
			.modify-btn-container {
				justify-content: center;
			}
		}
	}
}
</style>

<style lang="scss">
.datetime-editor {
	.vue3-timepicker-wrapper--time-picker input[type='text'] {
		font-size: 0.9rem;
		margin: 4px;
	}
	.date-picker {
		font-size: 0.9rem;
	}
}
</style>
