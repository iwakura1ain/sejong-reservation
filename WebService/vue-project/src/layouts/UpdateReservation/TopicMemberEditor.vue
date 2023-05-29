<template>
	<div class="topic-member-editor">
		<div class="topic-container">
			<span style="margin-right: 8px">회의 주제</span>
			<text-input
				class="topic-input"
				v-model="updateRsvFormStore.common.toBeChanged.topic"
			/>
		</div>
		<div class="member-container">
			<div>
				<span>참여자</span>
				<span style="margin-left: 12px; font-weight: bold"
					>{{
						updateRsvFormStore.common.toBeChanged.members.length + 1
					}}명</span
				>
			</div>
			<div class="member-input-container" style="margin-top: 8px">
				<p style="margin: 16px 0">
					{{
						`${userInfoStore.get().name} ${userInfoStore.get().email} (예약자)`
					}}
				</p>

				<member-input-set
					v-for="(member, index) in updateRsvFormStore.common.toBeChanged
						.members"
					:key="index"
					:index="index"
					v-model:name="member.name"
					v-model:email="member.email"
					@remove-member="handleRemoveMember"
				/>
				<plus-round-button @click="addMember" />
			</div>
		</div>
	</div>
</template>

<script setup>
// import { watch } from 'vue';
import TextInput from '@/components/atoms/TextInput.vue';
import MemberInputSet from '@/components/MemberInputSet.vue';
import PlusRoundButton from '@/components/PlusRoundButton.vue';
import { userInfoStore } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import { updateRsvFormStore } from '@/stores/updateRsvForm.js';
import { loadingStore } from '@/stores/loading.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';

// 상태, computed
//

// 초기화
init();

// 일반함수 --------------------------------------------
async function init() {
	try {
		loadingStore.start();
		const accessToken = userTokenStore.getAccessToken();
		await userInfoStore.setFromBackend(accessToken);
	} catch (err) {
		console.error(err);
		makeToast('사용자 정보를 가져오는 중 문제가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}

// 이벤트 핸들러 ----------------------------------------
function addMember() {
	updateRsvFormStore.common.toBeChanged.members = [
		...updateRsvFormStore.common.toBeChanged.members,
		{ name: '', email: '' },
	];
}
function handleRemoveMember(index) {
	updateRsvFormStore.common.toBeChanged.members = [
		...updateRsvFormStore.common.toBeChanged.members.slice(0, index),
		...updateRsvFormStore.common.toBeChanged.members.slice(index + 1),
	];
}
</script>

<style lang="scss" scoped>
.topic-member-editor {
	width: 100%;
	display: flex;
	flex-direction: column;

	.topic-container {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		.topic-input {
			flex: 1;
			// width: 100%;
		}
	}
	.member-container {
		margin-top: 16px;
		width: 100%;
	}
	.member-input-container {
		width: 100%;
	}
}

@media (max-width: 768px) {
	.topic-member-editor {
		font-size: 0.9rem;
	}
}
</style>
