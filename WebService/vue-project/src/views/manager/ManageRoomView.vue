<template>
	<div id="manage-room-view">
		<manage-tool-header name="회의실 관리" />
		<div class="view-body">
			<div>
				<filled-button
					style="
						height: 48px;
						width: 200px;
						display: inline-flex;
						align-items: center;
						justify-content: center;
					"
					@click="makeRoom"
					>+ 새로운 회의실 생성</filled-button
				>
			</div>
			<div class="room-card-container" style="margin-top: 24px">
				<room-card
					v-for="room in fetchedRoomStore.data"
					:key="room.id"
					:contents="room"
					@delete="fetchRooms"
				/>
			</div>
		</div>
	</div>
</template>

<script setup>
import ManageToolHeader from '@/layouts/Manage/ManageToolHeader.vue';
import RoomCard from '@/layouts/Manage/RoomCardForManager.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import { adminService } from '@/assets/scripts/requests/request.js';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import { useRouter } from 'vue-router';

if (history.state.roomCreated) {
	makeToast('회의실이 생성되었습니다', 'info');
}
if (history.state.roomUpdated) {
	makeToast('회의실이 수정되었습니다', 'info');
}

//

const router = useRouter();
function makeRoom() {
	router.push({ name: 'MakeRoom' });
}
async function fetchRooms() {
	// 모든 회의실을 불러오는 함수
	try {
		const res = await adminService.getAllRooms();
		if (!res.status) {
			throw new Error(res.msg);
		}
		fetchedRoomStore.setAll(res.data);
		console.log('rooms are fetched', fetchedRoomStore.data);
	} catch (err) {
		const msg = err.message;
		console.error(err, msg);
		if (msg === 'Not logged in') {
			makeToast('로그인 정보가 없습니다', 'error');
		} else if (msg === 'Room not found') {
			makeToast('등록된 회의실이 없습니다', 'error');
		} else {
			makeToast('예기치 못한 오류입니다', 'error');
		}
	}
}
fetchRooms();
</script>

<style lang="scss" scoped>
.view-body {
	.room-card-container {
		display: flex;
		flex-wrap: wrap;
	}
}
</style>
