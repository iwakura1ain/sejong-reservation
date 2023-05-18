<template>
	<div id="make-reservation-view">
		<section-header>예약하기</section-header>

		<template v-if="step < 4">
			<Transition appear>
				<article class="step step1-select-room">
					<section-header size="small">회의실 선택</section-header>
					<!-- <room-selector :rooms="step1Testdata" v-model="selectedRoomId" /> -->
					<room-selector />
					<RoomCalendar v-if="isRoomSelected" />
				</article>
			</Transition>

			<Transition appear>
				<article v-if="isRoomSelected" class="step step2-select-time">
					<section-header size="small">시간 선택</section-header>
					<meeting-datetime-selector
						:start-date-prop="$route.query.startDateProp"
						:selected-room="selectedRoom"
					/>
				</article>
			</Transition>

			<Transition appear>
				<article
					v-if="datetimeAvailability.length"
					class="step step3-write-members"
				>
					<section-header size="small">회의 정보 입력</section-header>
					<meeting-member-writer />

					<div class="step-btn-container">
						<filled-button class="step-btn" @click="confirm">
							검토하기
						</filled-button>
					</div>
				</article>
			</Transition>
		</template>

		<!-- form  -->
		<!-- confirm -->

		<template v-else>
			<Transition appear>
				<article class="step-4">
					<section-header size="small">내용 검토</section-header>
					<div class="confirm-notice">
						<p class="notice-1">입력하신 내용이 맞는지 검토해주세요.</p>
						<p class="notice-2">
							<span style="font-weight: bold">예약하기</span>
							버튼을 누르면 아래 내용으로 예약처리하고 참여자들에게 안내메일을
							발송합니다.
						</p>
					</div>

					<div class="confirm-contents">
						<div class="content">
							<p class="label">회의주제</p>
							<p class="value">
								{{ topic }}
							</p>
						</div>
						<div class="content">
							<p class="label">회의장소</p>
							<p class="value">
								{{ selectedRoom.buildingName }} {{ selectedRoom.roomName }}
							</p>
						</div>
						<div class="content">
							<p class="label">회의시간</p>
							<p class="value">{{ meetingTimeString }}</p>
						</div>
						<div class="content">
							<p class="label">회의일자</p>
							<div>
								<p
									v-for="(date, index) in meetingDates"
									:key="index"
									class="value"
								>
									{{ date.dateString }}
								</p>
							</div>
						</div>
						<div class="content">
							<p class="label">참여인원</p>
							<div>
								<p class="value">이원진 lee@wonj.in (예약자)</p>
								<p
									v-for="(member, index) in members"
									:key="index"
									class="value"
								>
									{{ member.name }} {{ member.email }}
								</p>
							</div>
						</div>
					</div>
					<div style="display: flex; width: 100%">
						<div class="step-btn-container">
							<filled-button class="step-btn" color="white" @click="cancel">
								수정하기
							</filled-button>
						</div>
						<div class="step-btn-container">
							<filled-button class="step-btn" @click="reserve">
								예약하기
							</filled-button>
						</div>
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
import RoomSelector from '@/layouts/MakeReservation/RoomSelector.vue';
import RoomCalendar from '@/components/RoomCalendar.vue';
import MeetingDatetimeSelector from '@/layouts/MakeReservation/MeetingDatetimeSelector.vue';
import MeetingMemberWriter from '@/layouts/MakeReservation/MeetingMemberWriter.vue';

import {
	selectedRoom,
	pickedTime,
	datetimeAvailability,
	topic,
	members,
} from '@/stores/reservation.js';

const meetingTimeString = computed(() => {
	const { start, end } = pickedTime.value;
	return `${start.HH}:${start.mm} ~ ${end.HH}:${end.mm}`;
});

const meetingDates = computed(() => {
	const arr = datetimeAvailability.value.filter(item => item.available);
	console.log(arr);
	return arr;
});

const step = ref(1);
const isRoomSelected = computed(() => {
	return Object.keys(selectedRoom.value).length > 0;
});

function confirm() {
	step.value = 4;
}

function cancel() {
	step.value = 3;
}

function reserve() {
	// stores/reservation 드래곤볼
	// --
}
</script>

<style lang="scss" scoped>
#make-reservation-view {
	margin-bottom: 10vh;
	.step {
		width: 100%;
	}
	.step-btn-container {
		width: 100%;
		margin-top: 64px;
		margin-bottom: 64px;
		text-align: center;
		.step-btn {
			text-align: center;
			width: 50%;
			min-width: 100px;
			padding-top: 24px;
			padding-bottom: 24px;
			font-size: 1.2rem;
		}
	}

	.step-4 {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.confirm-notice {
		margin-top: 24px;
		text-align: center;
		.notice-1 {
			font-size: 1.5rem;
			font-weight: bold;
			margin-bottom: 8px;
		}
		.notice-2 {
			font-size: 1.3rem;
		}
	}
	@media (max-width: 768px) {
		.confirm-notice {
			text-align: left;
			.notice-1 {
				font-size: 1.2rem;
			}
			.notice-2 {
				font-size: 1rem;
			}
		}
	}

	.confirm-contents {
		display: block;
		margin-top: 48px;
		margin-bottom: 24px;
		padding: 40px 96px 16px 96px;
		border: 1px solid $sejong-grey;
		border-radius: $box-radius;
		.content {
			display: flex;
			font-size: 1.1rem;
			margin-bottom: 24px;
			.label {
				font-weight: bold;
				margin-right: 8px;
				width: 67px;
			}
			.value {
				flex: 1;
				// word-wrap: break-all;
				word-break: break-all;
			}
			> div > p {
				margin-bottom: 8px;
			}
		}
	}
	@media (max-width: 768px) {
		.confirm-contents {
			display: block;
			width: 100%;
			max-width: 100%;
			padding-left: 4px;
			padding-right: 4px;
		}
	}

	.v-enter-active,
	.v-leave-active {
		transition: opacity 1s ease;
	}

	.v-enter-from,
	.v-leave-to {
		opacity: 0;
	}
}
</style>
