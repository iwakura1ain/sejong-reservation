<template>
	<div class="view-header">
		<h2>
			<slot></slot>
		</h2>
		<div class="line"></div>
	</div>
</template>

<script setup></script>

<style lang="scss" scoped>
.view-header {
	text-align: center;
	padding: 24px 0;

	h2 {
		font-size: 2rem;
		font-weight: 800;
		color: $sejong-red;
	}
	.line {
		display: inline-block;
		width: 80%;
		height: 4px;
		background-color: $sejong-red;
	}
}
</style>
