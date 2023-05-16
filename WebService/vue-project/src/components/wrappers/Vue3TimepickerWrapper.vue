<template>
	<vue-timepicker
		class="vue3-timepicker-wrapper--time-picker"
		v-model="localPickedTime"
		:hour-label="'시'"
		:minute-label="'분'"
		:placeholder="placeholder"
		close-on-complete
		hide-clear-button
		@change="updateTime"
	></vue-timepicker>
</template>

<script setup>
import { toRefs, ref, watch } from 'vue';
import VueTimepicker from 'vue3-timepicker';
import 'vue3-timepicker/dist/VueTimepicker.css';

// define props, emits
const props = defineProps({
	placeholder: {
		required: false,
		type: String,
		default: '시간 선택',
	},
	modelValue: {
		required: false,
		type: Object,
		default() {
			return {
				HH: '',
				mm: '',
			};
		},
	},
});

const emits = defineEmits(['update:modelValue']);

// states
const localPickedTime = ref({
	HH: '',
	mm: '',
});

const refPickedTime = toRefs(props).modelValue;
watch(refPickedTime, () => {
	// console.log('wathced', refPickedTime.value);
	localPickedTime.value.HH = refPickedTime.value.HH;
	localPickedTime.value.mm = refPickedTime.value.mm;
});
// event handelrs
function updateTime() {
	// console.log(`[Vue3TimepickerWrapper] pickedTime = ${localPickedTime.value}`);
	emits('update:modelValue', localPickedTime.value);
}
</script>

<style lang="scss">
.vue3-timepicker-wrapper--time-picker {
	input[type='text'] {
		border: 1px solid $sejong-grey;
		border-radius: $box-radius;
		text-align: center;
		font-size: 1rem;
	}
	.dropdown > .select-list > .hours > .active {
		background-color: $sejong-red !important;
	}
	.dropdown > .select-list > .minutes > .active {
		background-color: $sejong-red !important;
	}
}
</style>
