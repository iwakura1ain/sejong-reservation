<template>
	<div id="check-attendence-gateway-view">
		<section-header>사용인증할 회의실 선택</section-header>
		<room-selector v-model="selectedRoomId" />
	</div>
</template>

<script setup>
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import RoomSelector from '@/components/RoomSelector.vue';
import { watch, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const selectedRoomId = ref(0);
watch(selectedRoomId, () => {
	router.push({
		name: 'CheckAttendence',
		params: {
			id: selectedRoomId.value,
		},
	});
});
</script>

<style lang="scss" scoped>
#check-attendence-gateway-view {
}
</style>
