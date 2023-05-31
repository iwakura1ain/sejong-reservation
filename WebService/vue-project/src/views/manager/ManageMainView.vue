<template>
	<div id="manage-main-view">
		<manage-tool-header name="관리자 도구" />

		<!-- <section-header>통계 보고서</section-header>
		<div class="stat-report-container"></div> -->
	</div>
</template>

<script setup>
import ManageToolHeader from '@/layouts/Manage/ManageToolHeader.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
</script>

<style lang="scss" scoped>
#manage-main-view {
	width: 100%;
}
</style>
