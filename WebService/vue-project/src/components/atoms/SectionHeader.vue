<template>
	<div class="section-header" :class="{ big: size === 'big' }">
		<h2>
			<slot></slot>
		</h2>
		<!-- <div class="line"></div> -->
	</div>
</template>

<script setup>
defineProps({
	size: {
		required: false,
		type: String,
		default: 'big', // 'small', 'big'
	},
});
</script>

<style lang="scss" scoped>
.section-header {
	text-align: center;
	padding: 24px 0;
	margin-top: 18px;

	h2 {
		display: inline-block;
		font-size: 1.6rem;
		font-weight: 800;
		color: $sejong-red;

		padding-bottom: 12px;

		border-bottom: 4px solid $sejong-red;
	}
	// .line {
	// 	display: inline-block;
	// 	// width: 100%;
	// 	height: 4px;
	// 	background-color: $sejong-red;
	// }
}

.big {
	width: 100%;
	margin-bottom: 32px;
	h2 {
		display: block;
		font-size: 2rem;
	}
}
</style>
