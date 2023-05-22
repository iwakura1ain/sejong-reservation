<template>
	<div id="modify-reservation-common-data-view">
		<section-header>기본 정보 수정하기</section-header>
		<div>{{ reservationIds }}</div>
		<hr />
		<div>{{ reservationType === null ? 'null' : reservationType }}</div>
	</div>
</template>

<script setup>
import SectionHeader from '@/components/atoms/SectionHeader.vue';

const { reservationIds, reservationType } = history.state;
</script>

<style lang="scss" scoped>
#modify-reservation-common-data-view {
}
</style>
