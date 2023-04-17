<template>
	<div id="app-header">
		<div id="logo-container">
			<img :src="sejongLogo" />
			<span>회의실 예약 시스템</span>
		</div>
		<div id="l-container">LEFT</div>
		<div id="r-container">RIGHT</div>
	</div>
</template>

<script setup>
import sejongLogo from '@/assets/images/logo_white.png';
</script>

<style lang="scss" scoped>
#app-header {
	display: flex;
	align-items: center;

	height: $header-height;
	padding: 0 24px;
	color: white;
	background-color: $sejong-red;

	// vertical align - center
	#logo-container,
	#l-container,
	#r-container {
		display: flex;
		align-items: center;
	}

	#logo-container {
		img {
			height: 48px;
			width: auto;
			margin-right: 12px;
		}
		span {
			font-size: 1.2rem;
		}
	}

	#l-container {
	}

	#r-container {
		margin-left: auto;
	}
}
</style>
