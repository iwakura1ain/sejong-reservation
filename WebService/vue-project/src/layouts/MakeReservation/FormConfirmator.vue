<template>
	<div class="form-confirmator">
		<!-- 뭐하는건지 설명 -->
		<div class="confirm-notice">
			<p class="notice-1">입력하신 내용이 맞는지 검토해주세요.</p>
			<p class="notice-2">
				<span style="font-weight: bold">예약하기</span>
				버튼을 누르면 아래 내용으로 예약처리하고 참여자들에게 안내메일을
				발송합니다.
			</p>
		</div>

		<!-- 내용 확인 -->
		<div class="confirm-contents">
			<div class="content">
				<p class="label">주제</p>
				<p class="value">
					{{ makeRsvFormStore.common.topic }}
				</p>
			</div>
			<div class="content">
				<p class="label">장소</p>
				<p class="value">
					{{ meetingRoomStr }}
				</p>
			</div>
			<div class="content">
				<p class="label">일정</p>
				<div>
					<p
						v-for="(rsv, index) in makeRsvFormStore.each.filter(
							rsv => rsv.include && !rsv.conflict,
						)"
						:key="index"
						class="value"
					>
						{{
							`${getFormattedStringFromDateObj(
								rsv.date,
								'YYYY-MM-DD(ddd)',
							)} ${formatTimepickerObj(rsv.time)}`
						}}
					</p>
				</div>
			</div>
			<div class="content">
				<p class="label">참여자</p>
				<div>
					<p class="value" style="font-weight: bold">
						{{ makeRsvFormStore.common.members.length + 1 }}명
					</p>
					<p class="value">
						{{ `${userInfoStore.get().name} ${userInfoStore.get().email}` }}
						(예약자)
					</p>
					<p
						v-for="(member, index) in makeRsvFormStore.common.members"
						:key="index"
						class="value"
					>
						{{ `${member.name} ${member.email}` }}
					</p>
				</div>
			</div>
		</div>

		<section-header></section-header>
		<div class="submit-btn-container">
			<filled-button class="submit-btn" @click="handleSubmit">
				{{ `예약 생성하기` }}
			</filled-button>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { makeRsvFormStore } from '@/stores/makeRsvForm.js';
import { userInfoStore } from '@/stores/userInfo.js';
import { loadingStore } from '@/stores/loading.js';
import { userTokenStore } from '@/stores/userToken.js';
import { reservationService } from '@/assets/scripts/requests/request.js';
import getFormattedStringFromDateObj from '@/assets/scripts/utils/getFormattedStringFromDateObj.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import FilledButton from '@/components/atoms/FilledButton.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';

// 상태, computed ------------------------------------------
const meetingRoomStr = computed(() => {
	const roomId = makeRsvFormStore.common.roomId;
	const { address1, address2, name } = fetchedRoomStore.getById(roomId);
	return `${address1} ${address2} ${name}`;
});

const router = useRouter();

// 일반함수 ------------------------------------------------
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

async function validateRsvConflict() {
	// 입력 : [0,1,3] -->  makeRsvFormStore.each의 0번, 1번, 3번에 대해서 검증하라는 뜻.
	try {
		loadingStore.start();

		const reservations = makeRsvFormStore.each
			.filter(rsv => rsv.include && !rsv.conflict)
			.map(rsv => buildReqBodyElement(rsv));

		const req = { reservations };
		const accessToken = userTokenStore.getAccessToken();

		const res = await reservationService.create(req, accessToken);

		if (!res.status) {
			console.error(res);

			if (res.msg === 'Invalid reservation') {
				// 폼 검증을 통과하지 못함
				makeToast(`형식에 적합하지 않은 입력값이 있습니다`, 'error');
			} else if (res.msg === 'User cannot reserve that far into future') {
				makeToast(
					`현재 사용자유형으로 선택할 수 없는 너무 먼 예약입니다.`,
					'error',
				);
			} else {
				makeToast('알 수 없는 오류입니다', 'error');
				console.error(res);
			}
			throw new Error();
		}
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);
		makeToast('알 수 없는 오류입니다', 'error');
		throw new Error(err);
	} finally {
		loadingStore.stop();
	}
}
// 이벤트 핸들러 --------------------------------------------
async function handleSubmit() {
	try {
		await validateRsvConflict();
		router.push({ name: 'SuccessfullyReserved' });
	} catch (err) {
		makeToast('알 수 없는 오류입니다.', 'error');
	}
}
</script>

<style lang="scss" scoped>
.form-confirmator {
	display: flex;
	flex-direction: column;
	align-items: center;
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

	.confirm-contents {
		margin-top: 24px;
		.content {
			margin: 24px 0;
			.label {
				font-size: 1.2rem;
				font-weight: bold;
				margin: 4px 0;
			}
			.value {
				margin: 8px;
			}
		}
	}

	.submit-btn-container {
		text-align: center;
		.submit-btn {
			font-size: 2rem;
			padding: 48px;
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
	@media (max-width: 768px) {
	}
}
</style>
