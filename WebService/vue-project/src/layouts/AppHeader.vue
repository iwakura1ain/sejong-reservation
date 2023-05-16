<template>
	<div id="app-header">
		<router-link :to="{ name: 'UserMain' }">
			<div class="logo-container">
				<img :src="sejongLogo" />
				<span>회의실 예약 시스템</span>
			</div>
		</router-link>

		<div class="l-container">
			<router-link :to="{ name: 'MakeQuickReservation' }">
				<text-button color="white">빠른예약</text-button>
			</router-link>

			<router-link :to="{ name: 'MakeReservation' }">
				<text-button color="white">예약하기</text-button>
			</router-link>
			<router-link :to="{ name: 'ReservationHistory' }">
				<text-button color="white">예약내역</text-button>
			</router-link>
		</div>

		<div v-if="isLogin" class="r-container">
			<router-link :to="{ name: 'UserMyPage' }">
				<text-button color="white">{{ userinfoString }}</text-button>
			</router-link>
			<div>
				<router-link :to="{ name: 'ManageMain' }">
					<filled-button color="white">관리</filled-button>
				</router-link>
				<filled-button color="red">로그아웃</filled-button>
			</div>
		</div>
		<div v-else class="r-container">로그인안함</div>
	</div>
</template>

<script setup>
import sejongLogo from '@/assets/images/logo_white.png';
import TextButton from '@/components/atoms/TextButton.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import { computed } from 'vue';

const props = defineProps({
	isLogin: {
		required: true,
		type: Boolean,
	},
	userInfo: {
		required: false,
		type: Object,
		default(rawProps) {
			return {};
		},
		validator(value) {
			return true;
		},
	},
});

console.log(props.userInfo);

const userinfoString = computed(() => {
	const { username, level, isAdmin, noShowCount, isBanned } = props.userInfo;
	return `(${username} | ${level})`;
});
</script>

<style lang="scss" scoped>
#app-header {
	display: flex;
	align-items: center;

	// height: $header-height;
	padding: 24px 24px;
	color: white;
	background-color: $sejong-red;

	.logo-container,
	.l-container,
	.r-container {
		display: flex;

		align-items: center;
	}

	.logo-container {
		cursor: pointer;

		img {
			height: 42px;
			width: auto;
			margin-right: 12px;
		}
		span {
			color: white;
			font-size: 1.2rem;
		}
	}

	.l-container {
		margin: 0 12px;
	}

	.r-container {
		margin-left: auto;
	}
}

@media (max-width: 850px) {
	#app-header {
		flex-direction: column;
		padding: 24px 12px;

		.l-container {
			margin: 8px 0px;
		}
		.r-container {
			margin-left: 0;
		}
	}
}

@media (max-width: 320px) {
	#app-header {
		.r-container {
			flex-direction: column;
		}
	}
}
</style>
