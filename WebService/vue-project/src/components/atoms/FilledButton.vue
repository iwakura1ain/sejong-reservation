<template>
	<div class="filled-button" :class="color">
		<slot name="icon"></slot>
		<span>
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
			return ['red', 'white', 'disabled'].includes(value);
		},
	},
});
</script>

<style lang="scss" scoped>
.filled-button {
	display: inline-block;
	margin: $button-margin;
	padding: $button-padding;

	font-size: 1rem;
	border-radius: 0.5rem;
	cursor: pointer;

	transition: all 0.1s;
	word-break: keep-all;
	&:active {
		transform: scale(1.1);
	}
}

.red {
	background-color: $sejong-red;
	color: white;
	border: 1px solid white;
	&:hover {
		background-color: $almost-sejong-red;
	}
}

.white {
	background-color: white;
	color: $sejong-red;
	border: 1px solid $sejong-red;
	&:hover {
		background-color: $light-sejong-red;
	}
}

.disabled {
	border: 1px solid lightgrey;
	color: lightgrey;
	cursor: not-allowed;
	&:active {
		transform: none;
	}
}
</style>
