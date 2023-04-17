<template>
	<app-header> </app-header>
	<router-view class="app-router-view"></router-view>
	<app-footer> </app-footer>
</template>

<script setup>
import AppHeader from '@/layouts/AppHeader.vue';
import AppFooter from '@/layouts/AppFooter.vue';
</script>

<style lang="scss" scoped>
.app-router-view {
	min-height: $routerview-minheight;
}
</style>
