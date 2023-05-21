<template>
	<Datepicker
		class="date-picker"
		style="
			width: 160px;
			text-align: center;
			font-size: 1rem;
			padding: 8px;
			border-radius: 0.5rem;
			border: 1px solid #51626f;
		"
		:style="{
			'--vdp-selected-bg-color': '#C3002F',
			'--vdp-hover-bg-color': '#C3002F',
		}"
		:locale="ko"
		v-model="localDateState"
	/>
</template>

<script setup>
import Datepicker from 'vue3-datepicker';
import { ko } from 'date-fns/locale';
import { toRefs, ref, watch } from 'vue';
import getTodayZeroHour from '@/assets/scripts/utils/getTodayZeroHour.js';

// define props, emits
const props = defineProps({
	modelValue: {
		required: false,
		type: Date,
		default: new Date(),
	},
});

const emits = defineEmits(['update:modelValue']);

// states
const localDateState = ref(getTodayZeroHour());

const refPropDate = toRefs(props).modelValue;
watch(refPropDate, () => {
	localDateState.value = refPropDate.value;
});

watch(localDateState, () => {
	emits('update:modelValue', localDateState.value);
});
</script>

<style lang="scss" scoped></style>
