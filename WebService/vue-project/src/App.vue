<template>
	<app-header :isLogin="true" :user-info="userinfo"> </app-header>
	<Transition appear>
		<router-view class="app-router-view"></router-view>
	</Transition>
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

	display: flex;
	flex-direction: column;
	align-items: center;

	width: 100%;

	padding: $routerview-padding;
}
@media (max-width: 768px) {
	.app-router-view {
		padding: $routerview-mobile-padding;
	}
}
</style>

<style lang="scss">
.v-enter-active,
.v-leave-active {
	transition: opacity 1s ease;
}

.v-enter-from,
.v-leave-to {
	opacity: 0;
}
</style>
