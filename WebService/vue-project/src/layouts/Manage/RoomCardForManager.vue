<template>
	<div class="room-card">
		<div class="info-container">
			<img class="room-img" :src="contents.img" alt="회의실 사진" />
			<div>
				<span class="room-address">{{
					`${contents.address1} ${contents.address2}`
				}}</span>
				<!-- <span class="room-address2">{{ contents.address2 }}</span> -->
				<span class="room-name">{{ contents.name }}</span>
				<div class="max-user">
					<img class="icon" :src="groupIcon" alt="최대 수용인원" />
					<span class="value">{{ contents.maxUsers }}명</span>
				</div>
				<div class="opening-hour">
					<img class="icon" :src="clockIcon" alt="개방시간" />
					<span class="value">
						{{ contents.time.open }}
						─ {{ contents.time.close }}
					</span>
				</div>
				<!-- <div>
					<p v-if="contents.isUsable === 1">✅사용가능</p>
					<p v-else>❌사용불가</p>
				</div> -->
			</div>
		</div>
		<div
			v-if="!confirmDelete"
			class="btns"
			style="display: flex; margin-top: 12px"
		>
			<filled-button
				class="select-room-btn"
				color="white"
				style="flex: 1; text-align: center"
				@click="registerRoom"
			>
				기기등록
			</filled-button>
			<filled-button
				class="select-room-btn"
				color="white"
				style="flex: 1; text-align: center"
				@click="updateRoom"
			>
				수정
			</filled-button>
			<filled-button
				class="select-room-btn"
				style="flex: 1; text-align: center"
				@click="toggleConfirmDelete"
			>
				삭제
			</filled-button>
		</div>
		<div
			v-if="confirmDelete"
			style="
				display: flex;
				flex-direction: column;
				align-items: center;
				justify-content: center;
				margin-top: 12px;
			"
		>
			<p style="color: red; font-weight: bold; word-break: break-all">
				회의실을 삭제합니다.
			</p>
			<p style="color: red; font-weight: bold; word-break: break-all">
				되돌릴 수 없습니다.
			</p>
			<p style="color: red; font-weight: bold; word-break: break-all">
				이미 생성된 예약들에
			</p>
			<p style="color: red; font-weight: bold; word-break: break-all">
				영향을 줄 수 있습니다
			</p>
			<div>
				<text-button @click="toggleConfirmDelete">취소</text-button>
				<filled-button @click="handleDelete">삭제</filled-button>
			</div>
		</div>
	</div>
</template>

<script setup>
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextButton from '@/components/atoms/TextButton.vue';
import groupIcon from '@/assets/images/icons/group.png';
import clockIcon from '@/assets/images/icons/time.png';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { userTokenStore } from '@/stores/userToken.js';
import { loadingStore } from '@/stores/loading.js';
import { adminService } from '@/assets/scripts/requests/request.js';
import { attendenceChecker } from '@/assets/scripts/requests/checkinRequest.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

const props = defineProps({
	contents: {
		required: false,
		type: [Object, null],
	},
});
const emits = defineEmits(['delete']);
const router = useRouter();
const confirmDelete = ref(false);
function toggleConfirmDelete() {
	confirmDelete.value = !confirmDelete.value;
}
async function handleDelete() {
	try {
		loadingStore.start();
		const id = props.contents.id;
		const accessToken = userTokenStore.getAccessToken();
		const res = await adminService.deleteRoom(id, accessToken);
		if (!res.status) {
			console.error(res);
			throw new Error(res);
		}
		console.log(res);
		makeToast('삭제되었습니다', 'info');
		emits('delete');
	} catch (err) {
		console.error(err);
		makeToast('오류가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}

function updateRoom() {
	router.push({
		name: 'UpdateRoom',
		state: {
			roomData: JSON.parse(JSON.stringify(props.contents)),
		},
	});
}

// room_hash 세팅. 방마다 고유한 room_hash를 설정
async function setRoomHash(id) {
	try {
		// room_hash를 가져온다
		const accessToken = userTokenStore.getAccessToken();
		const roomHash = await attendenceChecker.registerRoom(id, accessToken);

		console.log('roomhash : ', roomHash);
		localStorage.setItem('room_hash', roomHash);

		return roomHash;
	} catch (err) {
		console.log(err, err.message);
		makeToast('예상치 못한 오류가 발생했습니다', 'error');
	}
}
async function registerRoom() {
	try {
		loadingStore.start();
		// const accessToken = userTokenStore.getAccessToken();
		const roomId = props.contents.id;
		// const res = await attendenceChecker.registerRoom(roomId, accessToken);

		// if (!res.status) {
		// 	console.error(res);
		// 	throw new Error(res);
		// }
		// console.log(res);
		makeToast(
			`이 기기가 ${roomId}번 방(${props.contents.name})의 이용인증용 기기로 등록되었습니다`,
			'info',
		);
	} catch (err) {
		console.error(err);
		makeToast('오류가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}
</script>

<style lang="scss" scoped>
.room-card {
	margin: 12px;
	padding: 24px;

	background-color: white;
	border-radius: $box-radius;

	box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
	-webkit-box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);
	-moz-box-shadow: 0px 4px 10px 4px rgba(0, 0, 0, 0.25);

	.info-container {
		display: flex;
		align-items: center;
		.room-img {
			width: 192px;
			height: 192px;
			border-radius: $box-radius;
			object-fit: cover;
		}

		> div {
			display: flex;
			flex-direction: column;
			justify-content: center;
			padding-left: 12px;

			.icon {
				vertical-align: middle;
				display: inline-block;
				height: 24px;
				width: auto;
				margin-right: 8px;
			}

			.room-address {
				display: block;
				font-weight: bold;
			}
			.room-name {
				display: block;
				font-size: 1.6rem;
				padding: 12px 0;
			}
			.opening-hour {
				margin: 8px 0;
			}

			.max-user,
			.opening-hour {
				display: flex;
				align-items: center;
			}

			.select-room-btn {
				text-align: center;
				margin: 0;
				margin-top: 8px;
			}
		}
	}
}

.room-card.selected {
	border: 2px solid $sejong-red;
	.info-container {
		filter: opacity(50%);
	}
}

@media (max-width: 768px) {
	.room-card {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		margin: 12px 0;
		// margin: 8px;
		padding: 12px;
		border: 2px solid white;
		.info-container {
			flex-direction: column;
			align-items: center;
			.room-img {
				width: 120px;
				height: 80px;
				margin-bottom: 24px;
			}
			> div {
				padding: 0;
			}
		}
	}
}
</style>
