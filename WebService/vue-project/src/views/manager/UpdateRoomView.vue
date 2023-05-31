<template>
	<div id="make-room-view">
		<section-header>회의실 수정</section-header>
		<div class="form-container">
			<div class="field-set">
				<span class="field-label">건물 이름</span>
				<text-input
					class="field-value text"
					placeholder="대양AI센터"
					v-model="formdata.address1"
				/>
			</div>
			<div class="field-set">
				<span class="field-label">중간 주소</span>
				<text-input
					class="field-value text"
					placeholder="8층"
					v-model="formdata.address2"
				/>
			</div>
			<div class="field-set">
				<span class="field-label">회의실 이름</span>
				<text-input
					class="field-value text"
					placeholder="835호"
					v-model="formdata.roomName"
				/>
			</div>
			<div class="field-set">
				<span class="field-label">운영 시작 시각</span>
				<vue3-timepicker-wrapper
					class="field-value timepicker"
					v-model="formdata.openTime"
					placeholder="시작하는 시각"
				/>
			</div>
			<div class="field-set">
				<span class="field-label">운영 종료 시각</span>
				<vue3-timepicker-wrapper
					class="field-value timepicker"
					v-model="formdata.closeTime"
					placeholder="끝나는 시각"
				/>
			</div>
			<div class="field-set">
				<span class="field-label">회의실 정원</span>
				<num-input
					class="field-value text"
					v-model="formdata.maxUsers"
					:no-zero="true"
					style="width: 64px"
				/>
			</div>
			<div class="field-set">
				<span class="field-label">사용가능 여부</span>
				<radio-group
					v-model="formdata.isUsable"
					class="field-value"
					:buttons="[
						{ text: '사용불가', value: 0 },
						{ text: '사용가능', value: 1 },
					]"
				/>
			</div>
			<div class="field-set">
				<span class="field-label">회의실 사진</span>
				<input type="file" @change="uploadFile" class="field-value" />
				<img
					v-if="formdata.previousImage && !formdata.image"
					:src="formdata.previousImage"
					alt="기존 사진"
					class="previous-img"
				/>
			</div>
		</div>

		<section-header></section-header>

		<div>
			<filled-button
				style="padding: 24px 120px; font-size: 1.2rem"
				@click="handleUpdate"
				>수정하기</filled-button
			>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import Vue3TimepickerWrapper from '@/components/wrappers/Vue3TimepickerWrapper.vue';
import RadioGroup from '@/components/RadioGroup.vue';
import NumInput from '@/components/atoms/NumInput.vue';
import TextInput from '@/components/atoms/TextInput.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import { adminService } from '@/assets/scripts/requests/request.js';
import { userTokenStore } from '@/stores/userToken.js';
import { loadingStore } from '@/stores/loading.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

const router = useRouter();

const formdata = ref({
	id: 0,
	roomName: '',
	address1: '',
	address2: '',
	openTime: { HH: '08', mm: '00' },
	closeTime: { HH: '22', mm: '00' },
	maxUsers: 1,
	isUsable: 1,
	image: null,
	previousImage: null,
});

if (history.state.roomData) {
	const roomdata = history.state.roomData;
	console.log(roomdata);
	formdata.value.id = roomdata.id;
	formdata.value.roomName = roomdata.name;
	formdata.value.address1 = roomdata.address1;
	formdata.value.address2 = roomdata.address2;
	formdata.value.isUsable = roomdata.isUsable;
	formdata.value.maxUsers = roomdata.maxUsers;

	const openTimeSplit = roomdata.time.open.split(':');
	const closeTimeSplit = roomdata.time.close.split(':');
	formdata.value.openTime.HH = openTimeSplit[0];
	formdata.value.openTime.mm = openTimeSplit[1];
	formdata.value.closeTime.HH = closeTimeSplit[0];
	formdata.value.closeTime.mm = closeTimeSplit[1];

	formdata.value.previousImage = roomdata.img;
}

function uploadFile(event) {
	formdata.value.image = event.target.files[0];
}

function validate() {
	const {
		roomName,
		address1,
		address2,
		openTime,
		closeTime,
		maxUsers,
		isUsable,
		image,
	} = formdata.value;

	if (!roomName || !address1 || !roomName || !maxUsers) {
		makeToast('비어있는 필수 항목이 있습니다', 'warning');
		return false;
	}

	const open = parseInt(openTime.HH) * 60 + parseInt(openTime.mm);
	const close = parseInt(closeTime.HH) * 60 + parseInt(closeTime.mm);
	if (open >= close) {
		makeToast('운영 종료시각은 시작시각 이후여야 합니다', 'warning');
		return false;
	}

	if (roomName.length > 40) {
		makeToast('회의실 이름은 최대 40자입니다', 'warning');
		return false;
	}

	if (address1.length > 80) {
		makeToast('건물 이름은 최대 80자입니다', 'warning');
		return false;
	}
	if (address2.length > 80) {
		makeToast('중간 주소는 최대 80자입니다', 'warning');
		return false;
	}

	return true;
}

async function handleUpdate() {
	try {
		loadingStore.start();
		if (!validate()) {
			return;
		}

		const req = {
			room_name: formdata.value.roomName,
			room_address1: formdata.value.address1,
			room_address2: formdata.value.address2,
			is_usable: formdata.value.isUsable,
			max_users: formdata.value.maxUsers,
			open_time: `${formdata.value.openTime.HH}:${formdata.value.openTime.mm}`,
			close_time: `${formdata.value.closeTime.HH}:${formdata.value.closeTime.mm}`,
		};

		const accessToken = userTokenStore.getAccessToken();
		const id = formdata.value.id;

		// 사진 제외정보 업데이트
		const res = await adminService.updateRoom(id, req, accessToken);
		if (!res.status) {
			console.error(res);
			throw new Error(res);
		}

		// 이미지 업로드
		if (formdata.value.image) {
			const _formdata = new FormData();
			_formdata.append('image', formdata.value.image);
			const imgRes = await adminService.uploadRoomImage(
				id,
				_formdata,
				accessToken,
			);
			if (!imgRes.status) {
				console.error(res);
				throw new Error(res);
			}
		}

		router.push({
			name: 'ManageRoom',
			state: {
				roomCreated: true,
			},
		});
		// makeToast('전송이 완료되었습니다', 'info');
	} catch (err) {
		console.error(err);
		makeToast('오류가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}
</script>

<style lang="scss" scoped>
#make-room-view {
	.form-container {
		.field-set {
			margin: 24px 0;
			display: flex;
			flex-direction: column;
			align-items: flex-start;
			// justify-content: flex-end;
			.field-label {
				margin-bottom: 4px;
			}
			.field-value {
				width: 320px;
			}
		}
	}
}

@media (max-width: 350px) {
	#make-room-view {
		.form-container {
			.field-set {
				.field-value {
					width: 240px;
				}
			}
		}
	}
}

.previous-img {
	width: 128px;
	height: 128px;
	border-radius: $box-radius;
	object-fit: cover;
	margin-top: 12px;
}
</style>
