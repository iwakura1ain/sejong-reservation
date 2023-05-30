<template>
	<div class="general-datetime-selector">
		<!-- <p>{{ meetingRoomStr }}</p> -->
		<div>
			<span>일정 유형</span>
			<!-- 학부생은 단건예약만 가능. 대학원생,교수,관리자는 단건/정기예약 가능. -->
			<template v-if="userInfoStore.get().type < 4">
				<radio-group
					:buttons="[
						{ text: '단건예약', value: false },
						{ text: '정기예약', value: true },
					]"
					v-model="makeRsvFormStore.common.useRepeat"
				/>
			</template>
			<template v-else>
				<filled-button style="margin-left: 0; padding: 10px"
					>단건예약</filled-button
				>
			</template>
		</div>

		<div>
			<span v-if="!makeRsvFormStore.common.useRepeat">예약 날짜</span>
			<span v-else>시작 날짜</span>
			<vue3-datepicker-wrapper v-model="makeRsvFormStore.common.startDate" />
		</div>

		<div class="timepick-container">
			<span>예약 시간</span>
			<div class="can-be-newline">
				<vue3-timepicker-wrapper
					v-model="makeRsvFormStore.defaultTime.start"
					placeholder="시작하는 시각"
				/>

				<div>
					<span class="range-mark">~</span>
					<vue3-timepicker-wrapper
						v-model="makeRsvFormStore.defaultTime.end"
						placeholder="끝나는 시각"
					/>
				</div>
			</div>
		</div>

		<div v-if="makeRsvFormStore.common.useRepeat" class="repeat-end-container">
			<span>반복 주기</span>
			<div class="can-be-newline">
				<radio-group
					:buttons="[
						{ text: '매월', value: REPEAT_INTERVAL_TYPE.MONTH },
						{ text: '매주', value: REPEAT_INTERVAL_TYPE.WEEK },
						{ text: '매일', value: REPEAT_INTERVAL_TYPE.DAY },
					]"
					v-model="makeRsvFormStore.common.repeatOption.interval"
					class="radio-group"
				/>
			</div>
		</div>

		<div v-if="makeRsvFormStore.common.useRepeat" class="repeat-end-container">
			<span>종료 시점</span>
			<div class="can-be-newline">
				<radio-group
					:buttons="[
						{ text: '횟수', value: REPEAT_END_TYPE.REPS },
						{ text: '날짜', value: REPEAT_END_TYPE.DATE },
					]"
					v-model="makeRsvFormStore.common.repeatOption.endType"
					class="radio-group"
				/>

				<div
					v-if="
						makeRsvFormStore.common.repeatOption.endType ===
						REPEAT_END_TYPE.REPS
					"
					class="repeat-value"
				>
					<num-input
						v-model="makeRsvFormStore.common.repeatOption.endReps"
						:no-zero="false"
						:style="{ width: '64px', textAlign: 'center' }"
						:max="REPEAT_END_CONDITION_MAX.REPS"
					/>
					<span>번 반복</span>
				</div>
				<div
					v-else-if="
						makeRsvFormStore.common.repeatOption.endType ===
						REPEAT_END_TYPE.DATE
					"
					class="repeat-value"
				>
					<vue3-datepicker-wrapper
						v-model="makeRsvFormStore.common.repeatOption.endDate"
						:max="REPEAT_END_CONDITION_MAX.DATE"
					/>
					<span style="margin-left: 4px">까지</span>
				</div>
			</div>
		</div>

		<div class="rsv-list-preview-container">
			<span class="title">예약 내용 미리보기</span>
			<span class="desc">다음 단계에서 내용을 수정할 수 있습니다</span>

			<template v-if="makeRsvFormStore.isGeneralFormRequirementFulfilled.value">
				<filled-button class="validate-btn" @click="handleCheckAvail()">
					{{ makeRsvFormStore.each.length }}건 예약 가능 여부 확인하기
				</filled-button>
			</template>
			<template v-else>
				<filled-button color="disabled">
					0건 예약 가능 여부 확인하기
				</filled-button>
			</template>

			<div
				v-for="(rsv, index) in makeRsvFormStore.each"
				:key="index"
				class="rsv-preview-item"
			>
				<span>{{
					getFormattedStringFromDateObj(rsv.date, 'YYYY-MM-DD(ddd)')
				}}</span>
				<span>{{ formattedDefaultTime }} </span>
				<span v-if="rsv.conflict !== null">
					{{ rsv.conflict ? '❌예약불가' : '✅예약가능' }}
				</span>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, watch } from 'vue';

import Vue3DatepickerWrapper from '@/components/wrappers/Vue3DatepickerWrapper.vue';
import Vue3TimepickerWrapper from '@/components/wrappers/Vue3TimepickerWrapper.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import NumInput from '@/components/atoms/NumInput.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';

import {
	REPEAT_END_TYPE,
	REPEAT_INTERVAL_TYPE,
	REPEAT_END_CONDITION_MAX,
} from '@/assets/constants.js';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { makeRsvFormStore } from '@/stores/makeRsvForm.js';
import { userInfoStore } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import { loadingStore } from '@/stores/loading.js';

import { reservationService } from '@/assets/scripts/requests/request.js';

import generateRange from '@/assets/scripts/utils/generateRange.js';
import getDateDifference from '@/assets/scripts/utils/getDateDifference.js';
import getFormattedStringFromDateObj from '@/assets/scripts/utils/getFormattedStringFromDateObj.js';
import validateDateTime from '@/assets/scripts/utils/validateDateTime.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

// props, event ------------------------------------------
defineEmits([]);
// 상태, computed ----------------------------------------
// const roomData = computed(() => {
// 	const id = makeRsvFormStore.common.roomId;
// 	return fetchedRoomStore.getById(id);
// });

// const meetingRoomStr = computed(() => {
// 	const { address1, address2, name } = roomData.value;
// 	return `${address1} ${address2} ${name}`;
// });

const formattedDefaultTime = computed(() => {
	const { start, end } = makeRsvFormStore.defaultTime;
	return `${start.HH}:${start.mm}-${end.HH}:${end.mm}`;
});

// 상태감시 -----------------------------------------------
// form이 바뀌면 makeRsvFormStore.each를 재구성함
watch(
	[makeRsvFormStore.common, makeRsvFormStore.defaultTime],
	() => {
		if (!makeRsvFormStore.isGeneralFormRequirementFulfilled.value) {
			return;
		}
		makeRsvFormStore.each.splice(0);

		const startDate = makeRsvFormStore.common.startDate;
		const defaultTime = { ...makeRsvFormStore.defaultTime }; // defaultTime : 내부 start, end는 반응형임

		makeRsvFormStore.each.push({
			// startDate에 대한 원소
			date: startDate,
			time: { ...defaultTime },
			conflict: null,
			include: true,
		});

		// "단건예약"인 경우 여기서 끝
		if (!makeRsvFormStore.common.useRepeat) {
			//console.log(makeRsvFormStore.each);
			return;
		}

		// ============================================
		// ============================================
		// ============================================

		// "정기예약"인 경우 아래 내용 실행
		const startDateSplitted = {
			year: startDate.getFullYear(),
			month: startDate.getMonth(),
			day: startDate.getDate(),
		};

		const interval = makeRsvFormStore.common.repeatOption.interval;
		const intervalAdder = {
			month: interval === REPEAT_INTERVAL_TYPE.MONTH ? 1 : 0,
			week: interval === REPEAT_INTERVAL_TYPE.WEEK ? 1 : 0,
			day: interval === REPEAT_INTERVAL_TYPE.DAY ? 1 : 0,
		};

		const endType = makeRsvFormStore.common.repeatOption.endType;
		// ---- TODO: MAX_NUM --> 별도 상수파일로 분리필요
		// const MAX_NUM = 100; // 한 번에 최대 100개 예약까지만 가능

		// 준비한 데이터들로 Form에 맞는 예약 객체 하나씩 만들어서
		// makeRsvFormStore.each에 넣기
		// ---- 1) 종료 유형이 "횟수"인 경우
		if (endType === REPEAT_END_TYPE.REPS) {
			const endReps = makeRsvFormStore.common.repeatOption.endReps;
			for (let i = 1; i < endReps; i++) {
				makeRsvFormStore.each.push({
					date: new Date(
						startDateSplitted.year,
						startDateSplitted.month + intervalAdder.month * i,
						startDateSplitted.day +
							intervalAdder.week * 7 * i +
							intervalAdder.day * i,
					),
					time: { ...defaultTime },
					conflict: null,
					include: true,
				});
			}
		}
		// ---- 2) 종료 유형이 "날짜"인 경우
		else if (endType === REPEAT_END_TYPE.DATE) {
			const endDate = makeRsvFormStore.common.repeatOption.endDate;
			const diff = getDateDifference(startDate, endDate);

			let endRepsFromDiff = 0;

			if (interval === REPEAT_INTERVAL_TYPE.MONTH) {
				endRepsFromDiff = diff.monthDiff;
			} else if (interval === REPEAT_INTERVAL_TYPE.WEEK) {
				endRepsFromDiff = diff.weekDiff;
			} else if (interval === REPEAT_INTERVAL_TYPE.DAY) {
				endRepsFromDiff = diff.dayDiff;
			}

			for (let i = 1; i < endRepsFromDiff; i++) {
				makeRsvFormStore.each.push({
					date: new Date(
						startDateSplitted.year,
						startDateSplitted.month + intervalAdder.month * i,
						startDateSplitted.day +
							intervalAdder.week * 7 * i +
							intervalAdder.day * i,
					),
					time: { ...defaultTime },
					conflict: null,
					include: true,
				});
			}
		}

		//console.log(makeRsvFormStore.each);
	},
	{ deep: true },
);

// 초기화 -------------------------------------------------
if (history.state.startDateFromCalendar) {
	const dateObj = new Date(history.state.startDateFromCalendar);
	dateObj.setHours(0, 0, 0, 0);
	makeRsvFormStore.common.startDate = dateObj;
}

// 일반함수 -----------------------------------------------
function buildReqBodyElement(rsv) {
	const rsvDateStr = getFormattedStringFromDateObj(rsv.date, 'YYYY-MM-DD');
	const startTimeFormattedStr = `${rsv.time.start.HH}:${rsv.time.start.mm}`;
	const endTimeFormattedStr = `${rsv.time.end.HH}:${rsv.time.end.mm}`;
	return {
		reservation_date: rsvDateStr,
		start_time: startTimeFormattedStr,
		end_time: endTimeFormattedStr,
		room_id: makeRsvFormStore.common.roomId,
		creator_id: userInfoStore.get().id,
		members: makeRsvFormStore.common.members,
	};
}

// event handlers
async function handleCheckAvail() {
	if (
		!validateDateTime(
			makeRsvFormStore.common.startDate,
			makeRsvFormStore.defaultTime,
		)
	) {
		return;
	} else {
		const range = generateRange(makeRsvFormStore.each.length);
		await validateRsvConflict(range);
	}
}
async function validateRsvConflict(targetIdxArr) {
	// 입력 : [0,1,3] -->  makeRsvFormStore.each의 0번, 1번, 3번에 대해서 검증하라는 뜻.

	try {
		loadingStore.start();
		const reservations = makeRsvFormStore.each
			.map((rsv, index) => {
				if (targetIdxArr.includes(index)) {
					return buildReqBodyElement(rsv);
				}
			})
			.filter(rsv => rsv);

		const req = { reservations };
		const accessToken = userTokenStore.getAccessToken();

		// 모든 예약이 생성 가능한지 확인
		const res = await reservationService.checkIfReservationOk(req, accessToken);
		console.log(res);
		if (res.status) {
			// 예약가능하다고 표시
			targetIdxArr.forEach(idx => {
				makeRsvFormStore.each[idx].conflict = false;
			});
		} else {
			if (res.msg === 'Conflict in reservations') {
				// 시간이 충돌하는 예약이 있음.
				// 충돌하는 객체 모아서, 해당하는 reservation_date를 가진 애들 conflict를 true로 설정
				const conflictDate = res.reservations.map(
					item => item.reservation_date,
				);
				targetIdxArr.forEach(idx => {
					const formattedStr = getFormattedStringFromDateObj(
						makeRsvFormStore.each[idx].date,
						'YYYY-MM-DD',
					);
					if (conflictDate.includes(formattedStr)) {
						makeRsvFormStore.each[idx].conflict = true;
					} else {
						makeRsvFormStore.each[idx].conflict = false;
					}
				});

				makeToast('시간이 겹쳐 예약할 수 없는 항목이 있습니다', 'error');
			} else if (res.msg === 'reservation not in room open hours') {
				targetIdxArr.forEach(idx => {
					makeRsvFormStore.each[idx].conflict = true;
				});
				makeToast(
					`선택한 예약 시간이 회의실 운영시간을 벗어났습니다.`,
					'error',
				);
			} else if (res.msg === 'Invalid reservation') {
				// 폼 검증을 통과하지 못함
				targetIdxArr.forEach(idx => {
					makeRsvFormStore.each[idx].conflict = true;
				});
				makeToast(`형식에 적합하지 않은 입력값이 있습니다`, 'error');
			} else if (res.msg === 'User cannot reserve that far into future') {
				makeToast(
					`현재 사용자유형으로 선택할 수 없는 너무 먼 예약입니다.`,
					'error',
				);
			} else {
				makeToast('알 수 없는 오류입니다', 'error');
				throw new Error(res);
			}
		}
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);
		makeToast('알 수 없는 오류입니다', 'error');
	} finally {
		loadingStore.stop();
	}
}
</script>

<style lang="scss" scoped>
.general-datetime-selector {
	display: flex;
	flex-direction: column;

	p {
		font-size: 1.6rem;
		font-weight: bold;
	}

	> div {
		margin: 12px 0;
		display: flex;
		align-items: center;
		> span {
			margin-right: 8px;
		}
	}

	.timepick-container,
	.repeat-end-container {
		display: flex;
		flex-wrap: wrap;
		margin: 8px 0;

		.can-be-newline {
			display: flex;
			align-items: center;
			> * {
				margin: 4px 0;
			}

			/* timepick-container */
			.range-mark {
				font-size: 32px;
				vertical-align: bottom;
				color: $sejong-grey;
				margin: 0 4px;
			}

			/* repeat-end-container */
			> .radio-group {
				margin-right: 4px;
			}
			.repeat-value {
				display: flex;
				align-items: center;
			}
		}
	}

	.rsv-list-preview-container {
		display: flex;
		flex-direction: column;
		align-items: flex-start;

		.title {
			margin-bottom: 8px;
		}
		.desc {
			font-color: $sejong-grey;
			font-size: 0.8rem;
			margin-bottom: 8px;
		}
		.validate-btn {
			margin-left: 0;
		}
		.rsv-preview-item {
			margin: 8px 0;
			span {
				font-size: 0.9rem;
				margin-right: 4px;
			}
		}
	}
}

@media (max-width: 768px) {
	.can-be-newline {
		flex: 1;
		display: flex;
		flex-wrap: wrap;
	}
}

@media (max-width: 320px) {
	.general-datetime-selector {
		// font-size: 0.8rem;
		p {
			font-size: 1.2rem;
		}

		> div {
			flex-direction: column;
			align-items: flex-start;
			> span {
				margin-bottom: 4px;
			}
		}

		.rsv-list-preview-container {
			.rsv-preview-item {
				span {
					font-size: 0.8rem;
				}
			}
		}
	}
}
</style>

<style lang="scss">
.general-datetime-selector {
	.date-picker {
		font-size: 1rem;
	}
}
@media (max-width: 320px) {
	.general-datetime-selector {
		.vue3-timepicker-wrapper--time-picker input[type='text'] {
			font-size: 0.9rem;
		}
		.date-picker {
			font-size: 0.9rem;
		}
	}
}
</style>
