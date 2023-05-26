<template>
	<input class="num-input" type="text" :value="modelValue" @input="update" />
</template>

<script setup>
const props = defineProps({
	modelValue: {
		require: false,
		type: [Number, null],
		default: -1,
	},
	noZero: {
		require: false,
		type: Boolean,
		default: false,
	},
	max: {
		require: false,
		type: [Number, null],
		default: null,
	},
});
const emits = defineEmits(['update:modelValue']);

function update(event) {
	//숫자만 입력받기 위한 문장
	const cur = event.target.value;
	event.target.value = cur.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');

	const replaced = event.target.value;
	if (props.noZero && (!replaced || replaced === '0')) {
		event.target.value = '1';
	}

	if (props.max) {
		if (parseInt(event.target.value) > props.max) {
			event.target.value = props.max;
		}
	}

	emits('update:modelValue', parseInt(event.target.value));
}
</script>

<style lang="scss" scoped>
.num-input {
	padding: 8px;
	font-size: 1rem;
	border-radius: 0.5rem;
	border: 1px solid grey;
}
</style>
