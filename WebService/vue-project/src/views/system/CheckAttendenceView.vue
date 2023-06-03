<template>
	<div id="check-attendence-view">
		<form class="form-container" @submit.prevent="handleCode">
			<article class="logo-container">
				<img class="logoimg" :src="LogoImgRed" alt="sejong univ. logo" />
				<h1 class="logotext-ko">회의실 예약 시스템</h1>
				<h2 class="logotext-en">Meeting Room Reservation System</h2>
			</article>
			<div class="form-content">
				<p style="margin: 24px; font-size: 1.2rem; text-align: center">
					{{ meetingRoomStr }}
				</p>
				<div class="field-set">
					<span class="label">사용 인증코드 입력</span>
					<text-input v-model="code"></text-input>
				</div>
				<div class="btn">
					<filled-button
						class="btn attend"
						@click="handleCode"
						color="red"
						type="submit"
						>인증</filled-button
					>
				</div>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import LogoImgRed from '@/assets/images/logo_red.png';
import TextInput from '@/components/atoms/TextInput.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { loadingStore } from '@/stores/loading.js';
import { attendenceChecker } from '@/assets/scripts/requests/checkinRequest.js';

const route = useRoute();
const roomId = route.params.id;

const code = ref('');

const meetingRoomStr = computed(() => {
	console.log(roomId);
	if (fetchedRoomStore.getAll().length > 0 && parseInt(roomId)) {
		const { address1, address2, name } = fetchedRoomStore.getById(
			parseInt(roomId),
		);
		return `${address1} ${address2} ${name}`;
	} else {
		return '';
	}
});

async function handleCode() {
	try {
		loadingStore.start();
		if (!code.value) {
			makeToast('코드를 입력해 주세요.', 'warning');
			return;
		}
		if (code.value.length !== 8) {
			makeToast('코드는 8자 입니다.', 'warning');
			return;
		}

		const roomHash = localStorage.getItem('SEJONG_RESERVATION_ROOMHASH');
		if (!roomHash) {
			makeToast(
				'이 기기가 인증용 기기로 등록되지 않았습니다. 관리자에게 문의하세요.',
				'warning',
			);
		}

		const reqBody = {
			reservation_code: code.value,
			room_hash: roomHash,
		};

		const res = await attendenceChecker.checkin(roomId, reqBody);
		if (!res.status) {
			console.error(res);
			throw new Error(res.msg);
		}

		makeToast('회의실 사용 인증이 완료되었습니다.', 'success');
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);

		if (msg === 'invalid key:val pairs') {
			makeToast('입력한 내용의 형식이 올바르지 않습니다', 'error');
		} else if (msg === 'Invalid room ID') {
			makeToast('잘못된 회의실이 선택되었습니다', 'error');
		} else if (msg === 'no reservation for current time') {
			makeToast('현재 사용인증 가능한 예약이 없습니다', 'error');
		} else if (msg === 'reservation code wrong') {
			makeToast('예약 인증코드가 잘못되었습니다', 'error');
		} else {
			makeToast('알 수 없는 오류입니다', 'error');
		}
	} finally {
		loadingStore.stop();
	}
}
</script>

<!-- <script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import LogoImgRed from '@/assets/images/logo_red.png';
import TextInput from '@/components/atoms/TextInput.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import { userTokenStore } from '@/stores/userToken.js';
import { userInfoStore } from '@/stores/userInfo.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import { attendenceChecker } from '@/assets/scripts/requests/checkinRequest.js';

userInfoStore.clear();
userTokenStore.clear();

let code;
let id;
let router;
// let accessToken;

// init
function init() {
	try {
		code = ref('');
		router = useRouter();
		id = parseInt(router.currentRoute.value.params.id);
		// accessToken = userTokenStore.getAccessToken();
		if (!localStorage.getItem('room_hash')) {
			setRoomHash(id);
		}
		console.log(id);
	} catch (err) {
		console.log(err, err.message);
		makeToast('예상치 못한 오류가 발생했습니다', 'error');
	}
}

// // room_hash 세팅. 방마다 고유한 room_hash를 설정
// async function setRoomHash(id) {
// 	try {
// 		// room_hash를 가져온다
// 		const accessToken = userTokenStore.getAccessToken();
// 		const roomHash = await attendenceChecker.registerRoom(id, accessToken);

// 		console.log('roomhash : ', roomHash);
// 		localStorage.setItem('room_hash', roomHash);

// 		return roomHash;
// 	} catch (err) {
// 		console.log(err, err.message);
// 		makeToast('예상치 못한 오류가 발생했습니다', 'error');
// 	}
// }

// 입력받은 code를 reservationCode와 대조
async function handleCode() {
	try {
		// console.log("id: ",id, "id type: ", typeof(id));
		// validate inserted code
		if (!code.value) {
			makeToast('코드를 입력해 주세요.', 'warning');
		}
		if (code.value.length != 8) {
			makeToast('코드는 8자 입니다.', 'warning');
		}
		const req = {
			reservation_code: code.value,
			room_hash: localStorage.getItem('room_hash'),
		};
		// const room_id = id;
		// console.log("room_id:", room_id, "id type:",typeof(room_id));

		const validateCode = await attendenceChecker.checkin({
			id: id,
			reqBody: req,
		});

		console.log(validateCode);

		// console.log("validatecode:", validateCode.status);
		if (!validateCode.status) {
			if (validateCode.msg == 'no reservation for current time') {
				makeToast('현재 시간대와 맞지 않는 예약입니다.', 'error');
			}
			if (validateCode.msg == 'reservation code wrong') {
				makeToast('코드가 일치하지 않습니다.', 'error');
			}
		}
		if (validateCode.status) {
			// console.log("successssssssssssssssssss");
			makeToast('출석을 인증하였습니다.', 'success');
		}
	} catch (err) {
		console.log(err, err.message);
		makeToast('예상치 못한 오류가 발생했습니다', 'error');
	}
}

init();
</script> -->

<style lang="scss" scoped>
#check-attendence-view {
	background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 1)),
		url(@/assets/images/login_bg.jpg) center;
	background-size: cover;

	.logo-container {
		text-align: center;
		font-weight: bold;
		.logoimg {
			width: 196px;
			height: 196px;
		}
		.logotext-ko {
			color: $sejong-grey;
			font-size: 2rem;
			margin: 8px 0;
		}
		.logotext-en {
			color: $sejong-red;
			font-size: 1rem;
		}
	}

	.form-container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		background-color: white;
		padding: 24px;
		margin-top: 48px;
		border: 1px solid lightgrey;
		border-radius: $box-radius;

		.form-content {
			width: 100%;
		}

		.field-set {
			margin: 12px 0;
			text-align: center;
			.label {
				margin-bottom: 8px;
				display: block;
				font-weight: bold;
			}
		}
		.btn {
			text-align: center;
			width: 100%;
		}
	}
}

@media (max-width: 360px) {
	#check-attendence-view {
		.logo-container {
			transform: scale(0.6);
			.logotext-ko {
				font-size: 1.6rem;
			}
			.logotext-en {
				font-size: 0.85rem;
			}
		}

		.form-container {
			.field-set {
				display: flex;
				flex-direction: column;
				align-items: center;
				text-align: center;
				.label {
					margin-bottom: 4px;
				}
			}
			.form-content {
				width: 100%;
			}
			.btn {
				.attend {
					margin-top: 4px;
					transform: translateX(-4px);
				}
			}
		}
	}
}
</style>
