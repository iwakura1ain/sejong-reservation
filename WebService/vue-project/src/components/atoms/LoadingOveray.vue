<template>
	<Transition>
		<div v-if="loading" class="loading-overay">
			<img :src="sejongWhiteLogo" alt="세종대학교 교표" class="spin" />
		</div>
	</Transition>
</template>

<script setup>
import sejongWhiteLogo from '@/assets/images/logo_white.png';
defineProps({
	loading: {
		required: false,
		type: Boolean,
		default: false,
	},
});
</script>

<style lang="scss" scoped>
.loading-overay {
	display: flex;
	justify-content: center;
	align-items: center;
	width: 100vw;
	height: 100%;
	position: fixed;
	z-index: 999;
	top: 0;
	left: 0;
	background-color: $sejong-grey-60;

	img {
		width: 128px;
		height: 128px;
	}
	.spin {
		animation: spin 2s linear infinite;
		transform-origin: 50% 50%;
	}

	@keyframes spin {
		100% {
			transform: rotate(360deg);
		}
	}
}

.v-enter-active,
.v-leave-active {
	transition: opacity 0.4s ease;
}

.v-enter-from,
.v-leave-to {
	opacity: 0;
}
</style>
