<template>
	<app-header :isLogin="true" :user-info="userinfo"> </app-header>
	<router-view class="app-router-view"></router-view>
	<app-footer> </app-footer>
</template>

<script setup>
import AppHeader from '@/layouts/AppHeader.vue';
import AppFooter from '@/layouts/AppFooter.vue';
import { ref } from 'vue';

// test data
const userinfo = ref({
	username: '이원진',
	email: '',
	level: '학부생',
	isAdmin: false,
	noShowCount: 0,
	isBanned: false,
});
</script>

<style lang="scss" scoped>
.app-router-view {
	min-height: $routerview-minheight;
}
</style>
