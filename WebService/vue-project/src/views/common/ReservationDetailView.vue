<template>
	<div id="reservation-detail-view">
		<section-header>예약 내역 상세</section-header>
		<div>{{ id }}번 예약내역</div>
	</div>
</template>

<script setup>
import SectionHeader from '@/components/atoms/SectionHeader.vue';

import { fetchedReservationStore } from '@/stores/fetchedReservation.js';
import { DEPT_TYPE, BASE_URL } from '@/assets/constants.js';

defineProps({
	id: {
		// router params : 백엔드 Reservation테이블의 id와 같은 값 (예약내역의 식별자)
		required: true,
		type: Number,
		default: -1,
	},
});
</script>

<style lang="scss" scoped>
#reservation-detail-view {
}
</style>
