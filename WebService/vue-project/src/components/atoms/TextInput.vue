<template>
	<input class="text-input" type="text" :value="modelValue" @input="update" />
</template>

<script setup>
defineProps({
	modelValue: {
		require: false,
		type: String,
		default: '',
	},
});
const emits = defineEmits(['update:modelValue']);

function update(event) {
	emits('update:modelValue', event.target.value);
}
</script>

<style lang="scss" scoped>
.text-input {
	padding: 8px;
	font-size: 1rem;
	border-radius: 0.5rem;
	border: 1px solid grey;
}
</style>
