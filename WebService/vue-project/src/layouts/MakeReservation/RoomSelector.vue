<!-- room 정보를 담은 객체의 배열을 props로 받습니다.(roomData)
각각의 room을 RoomCard컴포넌트로 뿌립니다.

RoomCard의 '선택'버튼이 클릭되면 선택된 room의 id를 받습니다.
받은 id를 다시 위로 올려줍니다. -->

<template>
	<div class="room-selector">
		<room-card
			v-for="room in rooms"
			:key="room.id"
			:contents="room"
			:selected="room.id === selectedRoom.id"
			@update-selected-room="updateSelectedRoom"
		></room-card>
	</div>
</template>

<script setup>
import RoomCard from '@/components/atoms/RoomCard.vue';
import RoomImgTest_1 from '@/assets/images/test/roomimg_1.jpg';
import RoomImgTest_2 from '@/assets/images/test/roomimg_2.jpg';
import { selectedRoom } from '@/stores/reservation.js';

// define props, events
// defineProps({
// 	modelValue: {
// 		required: false,
// 		type: [Number, String, null],
// 		default: null,
// 	},
// 	rooms: {
// 		required: true,
// 		type: Array,
// 	},
// });
// const emit = defineEmits(['update:modelValue']);

// state
// const selectedRoomId = ref(-1);

const rooms = [
	{
		id: 0,
		roomImg: RoomImgTest_1,
		buildingName: '대양AI센터',
		roomName: '835호',
		maxUser: 8,
		openingHour: ['09:00', '18:00'],
	},
	{
		id: 1,
		roomImg: RoomImgTest_2,
		buildingName: '대양AI센터',
		roomName: '836호',
		maxUser: 4,
		openingHour: ['09:00', '18:00'],
	},
];

// event handlers
// function updateSelectedRoomId(id) {
// 	console.log('[RoomSelector] 방 선택 : ', id);
// 	selectedRoomId.value = id;
// 	// emit('update:modelValue', id);
// }
function updateSelectedRoom(id) {
	console.log('[RoomSelector] 방 선택 : ', id);
	selectedRoom.value = rooms[id];
	// emit('update:modelValue', id);
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
