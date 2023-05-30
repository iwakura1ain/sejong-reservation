<template>
	<div class="empty-sign">
		<img
			:src="emptyImg"
			alt="보여줄 데이터가 하나도 없음을 표현하는 사람의 사진"
		/>
		<p>표시할 결과가 없습니다</p>
	</div>
</template>

<script setup>
import emptyImg from '@/assets/images/empty.png';
</script>

<style lang="scss" scoped>
.empty-sign {
	text-align: center;
	img {
		width: 256px;
		height: 256px;
	}
	p {
		font-size: 1.5rem;
	}
}
</style>
