<template>
	<div
		class="check-box"
		:class="{ disabled: disabled, checked: checked }"
	></div>
</template>

<script setup>
defineProps({
	disabled: {
		required: false,
		type: Boolean,
		default: false,
	},
	checked: {
		required: false,
		type: Boolean,
		default: false,
	},
});
</script>

<style lang="scss" scoped>
.check-box {
	min-width: 24px;
	min-height: 24px;
	border: 1px solid $sejong-grey;
	border-radius: 6px;
	background-color: white;
	transition: all 0.2s;
	cursor: pointer;

	display: flex;
	justify-content: center;
	align-items: center;
	color: white;
}

// .hover {
// 	background-color: $sejong-red-40;
// }

.checked {
	background-color: $sejong-red;
	&:after {
		content: '✓';
	}
}

.disabled {
	background-color: $sejong-grey;
}
</style>
