<template>
	<div id="successfully-reserved-view">
		<section-header>예약완료</section-header>
		<main>
			<div class="circle">
				<img :src="checkImg" alt="check" />
			</div>
			<p>예약이 완료되었습니다</p>

			<router-link to="/reservation/history">
				<filled-button>내역 확인하기</filled-button>
			</router-link>
		</main>
	</div>
</template>

<script setup>
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import checkImg from '@/assets/images/icons/tick_white.png';
import FilledButton from '@/components/atoms/FilledButton.vue';
</script>

<style lang="scss" scoped>
#successfully-reserved-view {
	main {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		.circle {
			width: 224px;
			height: 224px;
			border-radius: 50%;
			background-color: green;
			display: flex;
			justify-content: center;
			align-items: center;

			img {
				width: 192px;
				height: 192px;
			}
		}

		p {
			margin: 64px 0 24px 0;
			font-size: 1.5rem;
		}
	}
}
</style>
