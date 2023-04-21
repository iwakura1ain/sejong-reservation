<template>
	<div id="user-main-view">
		<section-header>예정된 회의</section-header>
		<h1>M A I N</h1>
		<router-link to="/asdf">not found 표시</router-link>

		<br />
		<filled-button color="red">red</filled-button>
		<filled-button color="white">white</filled-button>
	</div>
</template>

<script setup>
import FilledButton from '@/components/atoms/FilledButton.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
</script>

<style lang="scss" scoped></style>
