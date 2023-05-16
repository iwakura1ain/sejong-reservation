<template>
	<div class="meeting-member-writer">
		<div class="topic-container">
			<span style="margin-right: 8px">회의 주제</span>
			<text-input class="topic-input" v-model="topic" />
		</div>
		<div class="member-container">
			<div>
				<span>참여자</span>
				<span style="margin-left: 12px; font-weight: bold">총 2명</span>
			</div>
			<div class="member-input-container" style="margin-top: 8px">
				<!-- 예약자 (수정불가) -->
				<div></div>

				<!-- 나머지 멤버(추가제거 가능) -->
				<member-input-set
					:readonly="true"
					v-model:name="user.name"
					v-model:email="user.email"
				/>
				<member-input-set
					v-for="(member, index) in members"
					:key="index"
					:index="index"
					v-model:name="member.name"
					v-model:email="member.email"
					@remove-member="removeMember"
				/>
				<plus-round-button @click="addMember" />
			</div>
		</div>
	</div>
</template>

<script setup>
// import { ref } from 'vue';
import TextInput from '@/components/atoms/TextInput.vue';
import MemberInputSet from '@/components/MemberInputSet.vue';
import PlusRoundButton from '@/components/PlusRoundButton.vue';

import { topic, members } from '@/stores/reservation.js';

const user = {
	name: '이원진',
	email: 'lee@wonj.in',
};

function addMember() {
	members.value = [...members.value, { name: '', email: '' }];
	console.log(members.value);
}
function removeMember(index) {
	members.value = [
		...members.value.slice(0, index),
		...members.value.slice(index + 1),
	];
	console.log(members.value);
}
</script>

<style lang="scss" scoped>
.meeting-member-writer {
	display: flex;
	flex-direction: column;

	.topic-container {
		display: flex;
		align-items: center;
		.topic-input {
			flex: 1;
		}
	}
	.member-container {
		margin-top: 16px;
		// display: flex;
	}
}
</style>
