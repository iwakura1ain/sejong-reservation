<template>
	<div class="manage-tool-header">
		<section-header style="margin-bottom: 0; margin-top: 0; padding-top: 0">
			{{ name }}
		</section-header>
		<div class="nav">
			<text-button @click="goManageReservation">예약 관리</text-button>
			<text-button @click="goManageUser">사용자 관리</text-button>
			<text-button @click="goManageRoom">회의실 관리</text-button>
		</div>
		<section-header style="margin-top: 0; padding-top: 8px"></section-header>
	</div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import TextButton from '@/components/atoms/TextButton.vue';

defineProps({
	name: {
		required: false,
		type: String,
		default: '',
	},
});
const router = useRouter();

function goManageReservation() {
	router.push({ name: 'ManageReservation' });
}

function goManageUser() {
	router.push({ name: 'ManageUser' });
}

function goManageRoom() {
	router.push({ name: 'ManageRoom' });
}
</script>

<style lang="scss" scoped>
.manage-tool-header {
	width: 100%;

	.nav {
		display: flex;
		justify-content: space-around;
	}
}
</style>
