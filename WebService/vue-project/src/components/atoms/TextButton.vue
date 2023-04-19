<template>
	<div class="text-button" :class="color">
		<span class="text-area">
			<slot></slot>
		</span>
	</div>
</template>

<script setup>
/* const props = */ defineProps({
	color: {
		required: false,
		type: String,
		default: 'red',
		validator(value) {
			return ['red', 'white'].includes(value);
		},
	},
});
</script>

<style lang="scss" scoped>
.text-button {
	display: inline-block;
	margin: $button-margin;
	padding: $button-padding;

	font-size: 1rem;
	border-radius: 0.5rem;
	cursor: pointer;

	transition: all 0.1s;

	&:active {
		transform: scale(1.1);
	}
}

.red {
	color: $sejong-red;
	&:hover {
		background-color: $sejong-red-30;
	}
	// &:active {
	// 	background-color: $sejong-red-50;
	// }
}

.white {
	color: white;
	&:hover {
		background-color: $white-30;
	}
	// &:active {
	// 	background-color: $white-50;
	// }
}
</style>
