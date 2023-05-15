<template>
	<div id="not-found-view">
		<img :src="ximg" alt="x" />
		<p>
			<span style="font-weight: bold">NOT FOUND 404</span>
			<br /><br />
			<span>존재하지 않는 페이지입니다</span>
		</p>
		<router-link to="/main">
			<filled-button>메인화면으로 돌아가기</filled-button>
		</router-link>
	</div>
</template>

<script setup>
import FilledButton from '@/components/atoms/FilledButton.vue';
import ximg from '@/assets/images/icons/close.png';
</script>

<style lang="scss" scoped>
#not-found-view {
	display: flex;
	justify-content: center;
	align-items: center;

	img {
		width: 196px;
		height: 196px;
	}

	p {
		margin: 64px 0;
		font-size: 2rem;
		text-align: center;
	}
}
</style>
