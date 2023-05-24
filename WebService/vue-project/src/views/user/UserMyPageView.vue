<template>
	<div id="user-my-page-view">
		<section-header>마이페이지</section-header>

		<!-- 내 정보 -->
		<div class="profile-container">
			<section-header size="small">내 정보</section-header>
			<p class="name">{{ userInfo.name }}</p>
			<p class="user-id">{{ userInfo.id }}</p>
			<p class="user-email">{{ userInfo.email }}</p>
			<p class="user-phone">{{ userInfo.phone }}</p>
			<div class="user-category">
				<p class="user-dept">{{ userDeptStr }}</p>
				<p class="user-type">{{ userTypeStr }}</p>
			</div>

			<div style="text-align: center">
				<router-link to="/mypage/profile/edit">
					<filled-button class="edit-profile-btn">정보수정</filled-button>
				</router-link>
			</div>
		</div>

		<!-- 내 예약내역 요약 -->
		<div class="reservation-history-container">
			<section-header size="small">내 예약</section-header>
			<div style="text-align: center">
				<div style="margin-bottom: 24px">
					<p>
						<span>{{ '총 예약 : ' }}</span>
						{{ rsvStat.total }}건
					</p>
					<p>
						<span>{{ '사용 완료 : ' }}</span>
						{{ rsvStat.used }}건
					</p>
					<p>
						<span>{{ '미사용(노쇼) : ' }}</span>
						{{ rsvStat.noshow }}건
					</p>
					<p>
						<span>{{ '사용 예정 : ' }}</span>
						{{ rsvStat.notyet }}건
					</p>
				</div>

				<router-link to="/reservation/history">
					<filled-button class="go-history-btn">
						상세내역 바로가기
					</filled-button>
				</router-link>
			</div>
		</div>

		<!-- 탈퇴하기 -->
		<div class="user-delete-container">
			<section-header size="small">회원 탈퇴하기</section-header>
			<div style="text-align: center">
				<p>아래 버튼을 누르시면 회의실 예약 서비스에서 계정을 제거합니다.</p>
				<p style="color: red; font-weight: bold">
					⚠탈퇴한 뒤에 계정을 복구할 수 없습니다
				</p>

				<div v-if="!userDeleteEnabled">
					<filled-button @click="toggleUserDeleteEnabled">
						탈퇴하기
					</filled-button>
				</div>
				<div v-else>
					<filled-button color="white" @click="toggleUserDeleteEnabled">
						취소하기
					</filled-button>
					<p
						style="
							margin-top: 24px;
							color: red;
							font-weight: bold;
							font-size: 2rem;
						"
					>
						⚠탈퇴한 뒤에 계정을 복구할 수 없습니다
					</p>
					<p style="margin-top: 24px">
						탈퇴를 원하시면 아래 내용을 입력해주세요
					</p>

					<!-- 탈퇴를 위해 입력해야하는 내용 -->
					<div class="field-set">
						<p class="label">현재 비밀번호</p>
						<text-input
							class="content"
							type="password"
							v-model="deleteFormdata.pw"
						></text-input>
					</div>
					<div class="field-set">
						<p class="label">확인 문장</p>
						<p>아래 문장을 동일하게 입력해주세요</p>
						<p style="font-weight: bold; margin: 12px 0">
							{{ deleteConfirmString }}
						</p>
						<text-input
							class="content"
							v-model="deleteFormdata.confirmStr"
							:placeholder="deleteConfirmString"
						></text-input>
					</div>

					<filled-button @click="handleDeleteUser">탈퇴하기</filled-button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextInput from '@/components/atoms/TextInput.vue';
import { userTokenStore } from '@/stores/userToken.js';
import { userInfoStore, userDeptStr, userTypeStr } from '@/stores/userInfo.js';
import {
	reservationService,
	userService,
} from '@/assets/scripts/requests/request.js';
import { loadingStore } from '@/stores/loading.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

// 상태, computed -----------------------------------
const userInfo = ref({});
const rsvStat = ref({
	total: 0,
	used: 0,
	noshow: 0,
	notyet: 0,
});

const userDeleteEnabled = ref(false);
const deleteFormdata = ref({
	pw: '',
	confirmStr: '',
});
const deleteConfirmString = computed(() => {
	return `${userDeptStr.value}의 ${userInfo.value.name}님은 회원탈퇴를 진행하고 있습니다`;
});

// 초기화 ---------------------------------------
init();
const router = useRouter();
if (history.state.userPorfileUpdated) {
	makeToast('사용자 정보가 수정되었습니다', 'info');
}

// 일반함수 ----------------------------------------
// 주어진 시각(endTime)이 현재시각을 지났으면 true, 지나기 전이면 false반환.
function endTimeIsOvered({ date, endTime }) {
	const nowDate = new Date();
	const endTimeDate = new Date(`${date}T${endTime}:00`);
	return endTimeDate < nowDate;
}

async function getMyReservationStat() {
	try {
		const res = await reservationService.get({ creator: userInfo.value.id });
		if (!res.status) {
			if (res.msg) throw new Error(res.msg);
			else throw new Error(res);
		}
		const reservationList = res.data ? res.data : [];

		// 완료
		const beforeNow = reservationList.filter(rsv =>
			endTimeIsOvered(rsv.meetingDatetime),
		);
		const fromNow = reservationList.filter(
			rsv => !endTimeIsOvered(rsv.meetingDatetime),
		);

		return {
			total: reservationList.length,
			used: reservationList.reduce(
				(cnt, item) => cnt + (item.roomUsed === 1),
				0,
			),
			noshow: beforeNow.reduce((cnt, item) => cnt + (item.roomUsed === 1), 0),
			notyet: fromNow.reduce((cnt, item) => cnt + (item.roomUsed === 0), 0),
		};

		// ------------------------------
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);
		makeToast('예기치 못한 오류가 발생했습니다.', 'error');
	} finally {
		loadingStore.stop();
	}
}

async function init() {
	try {
		const accessToken = userTokenStore.getAccessToken();
		await userInfoStore.setFromBackend(accessToken);
		userInfo.value = userInfoStore.get();
		rsvStat.value = await getMyReservationStat();
	} catch (err) {
		const msg = err.msg;
		console.error(err, msg);
		if (msg === 'Token has expired') {
			makeToast('로그인이 만료되었습니다', 'error');
		} else {
			makeToast('예기치 못한 오류가 발생했습니다', 'error');
		}
	}
}

// 이벤트핸들러 -----------------
function toggleUserDeleteEnabled() {
	userDeleteEnabled.value = !userDeleteEnabled.value;
}

async function handleDeleteUser() {
	try {
		if (!deleteFormdata.value.pw || !deleteFormdata.value.confirmStr) {
			makeToast('비어있는 항목이 있습니다', 'warning');
		}
		if (deleteFormdata.value.confirmStr !== deleteConfirmString.value) {
			makeToast('확인 문장이 일치하지 않습니다', 'warning');
		}

		// 비밀번호가 맞는지 검증
		const checkPwRes = await userService.login({
			id: userInfo.value.id,
			password: deleteFormdata.value.pw,
		});
		if (!checkPwRes.status) {
			if (checkPwRes.msg === 'Wrong Password') {
				makeToast('비밀번호가 틀렸습니다', 'error');
				return;
			} else {
				throw new Error(checkPwRes.msg);
			}
		}

		// 삭제
		const at = userTokenStore.getAccessToken();
		const deleteRes = await userService.delete(userInfo.value.id, at);
		if (!deleteRes.status) {
			throw new Error(deleteRes);
		}
		userTokenStore.clear();
		userInfoStore.clear();
		router.push({ name: 'Login', state: { userDeleted: true } });
	} catch (err) {
		console.log(err, err.message);
		makeToast('예상치 못한 오류가 발생했습니다', 'error');
	}
}
</script>

<style lang="scss" scoped>
#user-my-page-view {
	.profile-container {
		margin-bottom: 24px;
		p {
			margin: 8px 0;
		}
		.name {
			font-size: 1.5rem;
			font-weight: bold;
		}
		.user-category {
			display: flex;
			p {
				margin-right: 8px;
				font-size: 1.4rem;
			}
			margin-bottom: 12px;
		}

		.edit-profile-btn {
			margin: 0;
		}
	}

	.reservatin-history-container {
	}
	.user-delete-container {
		.field-set {
			display: flex;
			flex-direction: column;
			align-items: flex-start;

			margin: 24px 0;
			.label {
				font-weight: bold;
				padding: 4px 0;
				font-size: 1.2rem;
				margin-bottom: 4px;
			}
			.content {
				width: 100%;
			}
		}
	}
}
</style>
