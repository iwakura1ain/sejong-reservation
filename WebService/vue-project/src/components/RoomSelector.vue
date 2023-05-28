<!-- room 정보를 담은 객체의 배열을 props로 받습니다.(roomData)
각각의 room을 RoomCard컴포넌트로 뿌립니다.

RoomCard의 '선택'버튼이 클릭되면 선택된 room의 id를 받습니다.
받은 id를 다시 위로 올려줍니다. -->

<template>
	<div class="room-selector">
		<room-card
			v-for="room in fetchedRoomStore.getAll()"
			:key="room.id"
			:contents="room"
			:selected="room.id === modelValue"
			@update-selected-room="updateSelectedRoom"
		></room-card>
	</div>
</template>

<script setup>
defineProps({
	modelValue: {
		required: true,
		type: Number,
		default: 1,
	},
});
const emits = defineEmits(['update:modelValue']);

import RoomCard from '@/components/atoms/RoomCard.vue';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';

function updateSelectedRoom(id) {
	emits('update:modelValue', id);
}
</script>

<style lang="scss" scoped>
.room-selector {
	width: 100%;
	display: flex;
	flex-wrap: wrap;

	.selected {
		border: 2px solid $sejong-red;
	}
}

@media (max-width: 768px) {
	.room-selector {
		justify-content: center;
	}
}
</style>
