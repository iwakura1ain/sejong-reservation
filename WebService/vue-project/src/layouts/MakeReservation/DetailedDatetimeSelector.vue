<template>
	<div class="detailed-datetime-selector">
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
				<div>
					<filled-button @click="handleInclude">
						{{ selectedIdx.length }}건 포함하기
					</filled-button>
					<filled-button @click="handleExclude">
						{{ selectedIdx.length }}건 제외하기
					</filled-button>
				</div>
			</div>
			<div v-else class="modify-btn-container">
				<div>
					<filled-button color="disabled"> 0건 날짜수정 </filled-button>
					<filled-button color="disabled"> 0건 시간수정 </filled-button>
				</div>
				<div>
					<filled-button color="disabled"> 0건 포함하기 </filled-button>
					<filled-button color="disabled"> 0건 제외하기 </filled-button>
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
						<filled-button color="white" @click="handleCancelModify">
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
						<filled-button color="white" @click="handleCancelModify">
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
						v-if="selectedIdx.length < makeRsvFormStore.each.length"
						@click="handleSelectAll('all')"
					>
						전체선택
					</text-button>

					<filled-button v-else @click="handleUnselectAll('all')" color="white">
						선택해제
					</filled-button>
				</div>

				<div class="include-select-btn">
					<text-button
						v-if="includedItemNum > selectedIncludedItemNum"
						@click="handleSelectAll('include')"
					>
						포함일정 전체선택
					</text-button>
					<filled-button
						v-else
						@click="handleUnselectAll('include')"
						color="white"
					>
						포함일정 선택해제
					</filled-button>
				</div>
			</div>
		</div>

		<!-- 세부 일정 목록 -->
		<div class="contents-section">
			<div
				v-for="(item, index) in makeRsvFormStore.each"
				:key="index"
				class="content-container reservation-item"
				:class="{
					'reservation-item': item.include,
					'reservation-item-disabled': !item.include,
				}"
				@click="handleClickRsvItem(index)"
			>
				<check-box :checked="selectedIdx.includes(index)" />
				<div class="values">
					<span class="content date">
						{{ getFormattedStringFromDateObj(item.date, 'YYYY-MM-DD(ddd)') }}
					</span>
					<span class="content time">
						{{ formatTimepickerObj(item.time) }}
					</span>
					<span class="content conflict" v-if="item.conflict !== null">
						{{ item.conflict ? '❌예약불가' : '✅예약가능' }}
					</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, ref } from 'vue';
import Vue3DatepickerWrapper from '@/components/wrappers/Vue3DatepickerWrapper.vue';
import Vue3TimepickerWrapper from '@/components/wrappers/Vue3TimepickerWrapper.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextButton from '@/components/atoms/TextButton.vue';
import CheckBox from '@/components/atoms/CheckBox.vue';
import { reservationService } from '@/assets/scripts/requests/request.js';
import { userInfoStore } from '@/stores/userInfo.js';
import { makeRsvFormStore } from '@/stores/makeRsvForm.js';
import { loadingStore } from '@/stores/loading.js';
import { userTokenStore } from '@/stores/userToken.js';
import generateRange from '@/assets/scripts/utils/generateRange.js';
import getFormattedStringFromDateObj from '@/assets/scripts/utils/getFormattedStringFromDateObj.js';
import validateDateTime from '@/assets/scripts/utils/validateDateTime.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

// 상태, computed ------------
const selectedIdx = ref([]);
const newDate = ref(null);
const newTime = ref(null);

const modifyContainerShow = ref(false); // true, false
const modifyContainerMode = ref(null); // 'date','time'

const includedItemNum = computed(() => {
	return makeRsvFormStore.each.reduce((cnt, item) => cnt + item.include, 0);
});
const selectedIncludedItemNum = computed(() => {
	return selectedIdx.value.reduce(
		(cnt, idx) => cnt + makeRsvFormStore.each[idx].include,
		0,
	);
});

// 초기화 --------------------
const allIdx = generateRange(makeRsvFormStore.each.length);
validateRsvConflict(allIdx);
console.log(allIdx);

// 일반함수 -------------------
function formatTimepickerObj(timepickerObj) {
	const { start, end } = timepickerObj;
	return `${start.HH}:${start.mm}-${end.HH}:${end.mm}`;
}

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
		// console.log(req);
		// console.log(targetIdxArr);
		// 모든 예약이 생성 가능한지 확인 (create시도)
		const res = await reservationService.create(req, accessToken);
		console.log(res);
		if (res.status) {
			// 만들어졌으면 확인했으니 만든 예약 삭제함.
			const ids = res.data.map(item => item.id);
			console.log(ids, res.data);
			const promises = ids.map(id =>
				reservationService.delete(id, accessToken),
			);
			await Promise.all(promises).catch(err => {
				console.error(err);
				makeToast('알 수 없는 오류입니다', 'error');
			});

			// 예약가능하다고 표시
			targetIdxArr.forEach(idx => {
				makeRsvFormStore.each[idx].conflict = false;
			});

			return true;
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
				console.error(res);
				throw new Error(res);
			}
		}
		return false;
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);
	} finally {
		loadingStore.stop();
	}
}

// 이벤트핸들러 ----------------
function handleSelectAll(target) {
	const len = makeRsvFormStore.each.length;
	if (target === 'all') {
		for (let i = 0; i < len; i++) {
			if (!selectedIdx.value.includes(i)) {
				selectedIdx.value.push(i);
			}
		}
	} else if (target === 'include') {
		for (let i = 0; i < len; i++) {
			if (makeRsvFormStore.each[i].include && !selectedIdx.value.includes(i)) {
				selectedIdx.value.push(i);
			}
		}
	}
}
function handleUnselectAll(target) {
	if (target === 'all') {
		selectedIdx.value.splice(0);
	} else if (target === 'include') {
		const excludeInSelected = selectedIdx.value.filter(
			idx => !makeRsvFormStore.each[idx].include,
		);
		selectedIdx.value.splice(0);
		for (let el of excludeInSelected) {
			selectedIdx.value.push(el);
		}
	}
}

function handleClickRsvItem(id) {
	if (selectedIdx.value.includes(id)) {
		const idx = selectedIdx.value.indexOf(id);
		selectedIdx.value.splice(idx, 1);
	} else {
		selectedIdx.value.push(id);
	}
	console.log(makeRsvFormStore.each);
}

function handleOpenModify(mode) {
	// mode : 'date', 'time'
	modifyContainerMode.value = mode;

	const i = selectedIdx.value[0];
	if (mode === 'date') {
		newDate.value = makeRsvFormStore.each[i].date;
	} else if (mode === 'time') {
		newTime.value = { ...makeRsvFormStore.each[i].time };
	}

	modifyContainerShow.value = true;
}
function handleCancelModify() {
	modifyContainerMode.value = null;
	modifyContainerShow.value = false;
}

async function handleModifyDate() {
	try {
		selectedIdx.value.map(idx => {
			makeRsvFormStore.each[idx].date = newDate.value;
		});
		const res = await validateRsvConflict(selectedIdx.value);
		if (res) {
			selectedIdx.value.splice(0);
			modifyContainerShow.value = false;
			makeToast('날짜가 변경되었습니다', 'info');
		}
	} catch (err) {
		console.error(err);
	}
}

async function handleModifyTime() {
	try {
		for (let idx of selectedIdx.value) {
			if (!validateDateTime(makeRsvFormStore.each[idx].date, newTime.value)) {
				return;
			}
			makeRsvFormStore.each[idx].time = newTime.value;
		}
		const res = await validateRsvConflict(selectedIdx.value);
		if (res) {
			selectedIdx.value.splice(0);
			modifyContainerShow.value = false;
			makeToast('시간이 변경되었습니다', 'info');
		}
	} catch (err) {
		console.error(err);
	}
}

function handleInclude() {
	selectedIdx.value.map(idx => {
		makeRsvFormStore.each[idx].include = true;
	});
	selectedIdx.value.splice(0);
	makeToast('에약할 목록에 추가했습니다.', 'info');
}

function handleExclude() {
	selectedIdx.value.map(idx => {
		makeRsvFormStore.each[idx].include = false;
	});
	selectedIdx.value.splice(0);
	makeToast('에약할 목록에서 제외했습니다.', 'info');
}
</script>

<style lang="scss" scoped>
.detailed-datetime-selector {
	// width: 100%;
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
}

@media (max-width: 768px) {
	.detailed-datetime-selector {
		.control-section {
			.modify-btn-container {
				justify-content: center;
			}
		}
	}
}
</style>

<style lang="scss">
.detailed-datetime-selector {
	.vue3-timepicker-wrapper--time-picker input[type='text'] {
		font-size: 0.9rem;
		margin: 4px;
	}
	.date-picker {
		font-size: 0.9rem;
	}
}
</style>
