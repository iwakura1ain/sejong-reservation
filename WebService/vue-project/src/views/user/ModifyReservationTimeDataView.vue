<template>
	<div id="modify-reservation-time-data-view">
		<section-header>일정 수정하기</section-header>
		<div>{{ reservationIds }}</div>
	</div>
</template>

<script setup>
import SectionHeader from '@/components/atoms/SectionHeader.vue';

const { reservationIds } = history.state;
</script>

<style lang="scss" scoped>
#modify-reservation-time-data-view {
}
</style>
