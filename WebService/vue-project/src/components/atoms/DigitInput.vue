<template>
	<input class="digit-input" type="text" :value="modelValue" @input="update" />
</template>

<script setup>
defineProps({
	modelValue: {
		require: false,
		type: [String, null],
		default: '',
	},
});
const emits = defineEmits(['update:modelValue']);

function update(event) {
	event.target.value = event.target.value.replace(/\D/g, '');
	emits('update:modelValue', event.target.value);
}
</script>

<style lang="scss" scoped>
.digit-input {
	padding: 8px;
	font-size: 1rem;
	border-radius: 0.5rem;
	border: 1px solid grey;
}
</style>
