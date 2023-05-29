<template>
	<div id="make-room-view">
		<section-header>회의실 {{ mode }}</section-header>
	</div>
</template>

<script setup>
import SectionHeader from '@/components/atoms/SectionHeader.vue';
defineProps({
	mode: {
		required: true,
		type: String, // "생성", "편집"
		default: '생성',
	},
});
</script>

<style lang="scss" scoped>
#make-room-view {
}
</style>
