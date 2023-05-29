<template>
	<div class="vue-next-select-wrapper">
		<vue-select
			v-model="localModelValue"
			:options="options"
			:placeholder="placeholder"
			close-on-select
			openDirection="bottom"
			:min="1"
			:disabled="disabled"
		></vue-select>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import VueSelect from 'vue-next-select';
import 'vue-next-select/dist/index.min.css';

const props = defineProps({
	modelValue: {
		required: false,
	},
	options: {
		required: false,
		type: Array,
		default() {
			return [];
		},
	},
	placeholder: {
		required: false,
		type: String,
		default: '선택',
	},
	disabled: {
		required: false,
		type: Boolean,
		default: false,
	},
});

const emits = defineEmits(['update:modelValue']);

const localModelValue = computed({
	get() {
		return props.modelValue;
	},
	set(newValue) {
		emits('update:modelValue', newValue);
	},
});
</script>

<style lang="scss" scoped>
.vue-next-select-wrapper {
	width: 120px;
	cursor: pointer;
}
</style>

<style lang="scss">
.vue-select {
	width: 100%;
	height: 32px;
	border-radius: $box-radius;
	border-color: grey;
}
.vue-input input {
	height: 24px;
	font-size: 1rem;
	padding-left: 4px;
}

.vue-select-header {
	cursor: pointer;
}

.vue-dropdown-item.highlighted {
	background-color: $sejong-grey;
	color: white;
}

.vue-dropdown-item.selected {
	background-color: $sejong-red;
	color: white;
}
.vue-dropdown-item.selected.highlighted {
	background-color: $sejong-red;
	color: white;
	cursor: pointer;
}
</style>
