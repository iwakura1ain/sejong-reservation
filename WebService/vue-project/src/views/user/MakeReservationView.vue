<template>
	<div id="make-reservation-view">
		<section-header>예약하기</section-header>
		<div id="top-header"></div>
		<!-- STEP 1 : 회의실 선택 -->
		<template v-if="makeRsvFormStore.formState.step === 1">
			<Transition>
				<article class="step step1-select-room">
					<section-header size="small">회의실 선택</section-header>
					<room-selector v-model="makeRsvFormStore.common.roomId" />
				</article>
			</Transition>
		</template>

		<!-- 선택한 회의실의 예약현황을 보여주는 달력 : STEP 1에 표시됨 -->
		<template v-if="makeRsvFormStore.formState.step === 1 && isRoomSelected">
			<Transition>
				<div style="width: 100%">
					<div
						v-if="isRoomSelected"
						class="reserved-time-display-calendar-container"
					>
						<section-header size="small">회의실 예약현황</section-header>
						<RoomCalendar
							v-model:is-opened="isCalendarOpened"
							:fetch-trigger="makeRsvFormStore.common"
							:room-id="makeRsvFormStore.common.roomId"
						/>
					</div>
				</div>
			</Transition>
		</template>

		<div class="step" v-if="makeRsvFormStore.formState.step === 1">
			<div class="step-btn-container">
				<section-header></section-header>
				<filled-button
					v-if="isRoomSelected"
					class="next-step-btn"
					@click="handleGoNextStep"
				>
					{{ `공통 내용 결정하기 >` }}
				</filled-button>
				<filled-button v-else color="disabled">
					{{ `공통 내용 결정하기 >` }}
				</filled-button>
			</div>
		</div>

		<!--  -->
		<!--  -->
		<!-- 선택한 회의실의 예약현황을 보여주는 달력 : STEP 2~3에 표시됨 -->
		<!-- <div
			class="reserved-time-display-calendar-container"
			v-if="
				1 < makeRsvFormStore.formState.step &&
				makeRsvFormStore.formState.step < 4
			"
		>
			<RoomCalendar
				v-model:is-opened="isCalendarOpened"
				:fetch-trigger="makeRsvFormStore.common"
				:room-id="makeRsvFormStore.common.roomId"
			/>
		</div> -->

		<!-- STEP 2 : 회의 일정의 큰 틀 선택 -->
		<template v-if="makeRsvFormStore.formState.step === 2">
			<Transition>
				<article class="step step2-select-general-datetime">
					<div class="center-box">
						<section-header size="small">공통 내용 결정하기</section-header>
						<div class="reserved-time-display-calendar-container">
							<RoomCalendar
								v-model:is-opened="isCalendarOpened"
								:fetch-trigger="makeRsvFormStore.common"
								:room-id="makeRsvFormStore.common.roomId"
							/>
						</div>
						<general-datetime-selector />
					</div>
					<div class="step-btn-container">
						<section-header></section-header>
						<filled-button
							class="prev-step-btn"
							color="white"
							@click="handleGoPrevStep"
						>
							{{ `< 회의실 선택하기` }}
						</filled-button>
						<filled-button
							class="next-step-btn"
							@click="handleGoNextStep"
							v-if="makeRsvFormStore.isGeneralFormRequirementFulfilled.value"
						>
							{{ `세부 일정 선택하기 >` }}
						</filled-button>
						<filled-button v-else color="disabled">
							{{ `세부 일정 선택하기 >` }}
						</filled-button>
					</div>
				</article>
			</Transition>
		</template>

		<!-- STEP 3 : 세부 일정 선택 -- 예외처리(시간변경, 제외) -->
		<template v-if="makeRsvFormStore.formState.step === 3">
			<Transition appear>
				<article class="step step3-select-detailed-datetime">
					<div class="center-box">
						<section-header size="small">세부 일정 선택</section-header>
						<div class="reserved-time-display-calendar-container">
							<RoomCalendar
								v-model:is-opened="isCalendarOpened"
								:fetch-trigger="makeRsvFormStore.common"
								:room-id="makeRsvFormStore.common.roomId"
							/>
						</div>
						<detailed-datetime-selector />
					</div>
					<div class="step-btn-container">
						<section-header></section-header>
						<filled-button
							class="prev-step-btn"
							color="white"
							@click="handleGoPrevStep"
						>
							{{ `< 공통 내용 선택하기` }}
						</filled-button>
						<filled-button
							v-if="isConflictIncluded || isThereNoIncluded"
							class="next-step-btn"
							@click="handleGoNextStep"
						>
							{{ `주제/참여자 입력하기 >` }}
						</filled-button>
						<filled-button v-else color="disabled">
							{{ `주제/참여자 입력하기 >` }}
						</filled-button>
					</div>
				</article>
			</Transition>
		</template>

		<!-- STEP 4 : 회의 주제, 참여자 입력 -->
		<template v-if="makeRsvFormStore.formState.step === 4">
			<Transition appear>
				<article class="step step4-write-topic-members">
					<section-header size="small">주제/참여자 정보 입력</section-header>
					<topic-member-writer />

					<div class="step-btn-container">
						<section-header></section-header>
						<filled-button
							class="prev-step-btn"
							color="white"
							@click="handleGoPrevStep"
						>
							{{ `< 세부 일정 선택하기` }}
						</filled-button>
						<filled-button class="next-step-btn" @click="handleGoNextStep">
							{{ `최종 검토하기 >` }}
						</filled-button>
					</div>
				</article>
			</Transition>
		</template>

		<!-- form 끝  -->
		<!-- confirm 시작 -->

		<!-- STEP 5 : 최종 검토 및 예약 생성 -->
		<template v-if="makeRsvFormStore.formState.step === 5">
			<Transition appear>
				<article class="step step-5-comfirm">
					<div class="center-box">
						<section-header size="small">내용 검토</section-header>
						<form-confirmator />
					</div>
					<div class="step-btn-container">
						<section-header></section-header>
						<filled-button
							class="prev-step-btn"
							color="white"
							@click="handleGoPrevStep"
						>
							{{ `< 주제/참여자 입력하기` }}
						</filled-button>
					</div>
				</article>
			</Transition>
		</template>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';

import SectionHeader from '@/components/atoms/SectionHeader.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import RoomCalendar from '@/components/RoomCalendar.vue';

import RoomSelector from '@/components/RoomSelector.vue';
import GeneralDatetimeSelector from '@/layouts/MakeReservation/GeneralDatetimeSelector.vue';
import DetailedDatetimeSelector from '@/layouts/MakeReservation/DetailedDatetimeSelector.vue';
import TopicMemberWriter from '@/layouts/MakeReservation/TopicMemberWriter.vue';
import FormConfirmator from '@/layouts/MakeReservation/FormConfirmator.vue';

import { makeRsvFormStore } from '@/stores/makeRsvForm.js';
import validateDateTime from '@/assets/scripts/utils/validateDateTime.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
// 초기화 -------------------------------------
makeRsvFormStore.clear();

// 상태, computed -----------------------------
const isCalendarOpened = ref(false);

const isRoomSelected = computed(() => {
	return makeRsvFormStore.common.roomId > 0; // db의 회의실 id는 1부터 시작함.
});

const isConflictIncluded = computed(() => {
	let result = false;
	for (let rsv of makeRsvFormStore.each) {
		if (rsv.conflict && rsv.include) {
			return true;
		}
	}

	return result;
});

const isThereNoIncluded = computed(() => {
	for (let rsv of makeRsvFormStore.each) {
		if (rsv.include) {
			return true;
		}
	}

	return false;
});
// 일반함수 -----------------------------------

// 이벤트 핸들러 -------------------------------
function handleGoPrevStep() {
	makeRsvFormStore.formState.step -= 1;
	const el = document.querySelector('#top-header');
	el.scrollIntoView({
		behavior: 'smooth',
	});
}
function handleGoNextStep() {
	if (makeRsvFormStore.formState.step === 2) {
		const startDate = makeRsvFormStore.common.startDate;
		const defaultTime = makeRsvFormStore.defaultTime;
		const isValid = validateDateTime(startDate, defaultTime);
		if (!isValid) return;
	} else if (makeRsvFormStore.formState.step === 4) {
		const topic = makeRsvFormStore.common.topic;
		if (topic.length > 100) {
			makeToast(
				`회의 주제는 최대 100자 입니다.`,
				'error',
			);
			return;
		}

		const isValid = makeRsvFormStore.checkMeetingInfoFormValid();
		if (!isValid) {
			makeToast(
				'비어있는 항목이 있거나, 이메일의 형식이 올바르지 않습니다',
				'warning',
			);
			return;
		}
	}

	makeRsvFormStore.formState.step += 1;

	const el = document.querySelector('#top-header');
	el.scrollIntoView({
		behavior: 'smooth',
	});
}
</script>

<style lang="scss" scoped>
#make-reservation-view {
	margin-bottom: 10vh;
	.step {
		width: 100%;
	}
	.step-btn-container {
		text-align: center;
		.step-btn {
			// width: 80%;
		}
	}
	.center-box {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.reserved-time-display-calendar-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		margin-bottom: 48px;
	}
}
</style>
