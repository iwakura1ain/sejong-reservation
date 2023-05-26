<template>
	<Datepicker
		class="date-picker"
		style="
			width: 160px;
			text-align: center;
			/* font-size: 1rem; */
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
		:week-starts-on="0"
		:lower-limit="datepickerLimit.lower"
		:upper-limit="datepickerLimit.upper"
	/>
</template>

<script setup>
import Datepicker from 'vue3-datepicker';
import { ko } from 'date-fns/locale';
import { computed, ref, watch } from 'vue';

import { userInfoStore } from '@/stores/userInfo.js';

// define props, emits
const props = defineProps({
	modelValue: {
		required: false,
		type: Date,
		default: new Date(),
	},
});
const emits = defineEmits(['update:modelValue']);
const localDateState = ref(props.modelValue);
watch(localDateState, () => {
	emits('update:modelValue', localDateState.value);
});

// -------------------------------
// 사용자 유형에 따라 선택가능한 범위 지정
// 1 관리자, 2 교수 무제한
// 3 대학원생 지금으로부터 7일 뒤 자정까지 선택 가능
// 4 학부생 지금으로부터 2일 뒤 자정까지 선택 가능
const datepickerLimit = computed(() => {
	const userType = userInfoStore.get().type;

	const lower = new Date();
	lower.setHours(0, 0, 0, 0);
	const upper = new Date();
	upper.setHours(0, 0, 0, 0);

	if (userType === 1) {
		return {
			lower: lower,
			upper: null,
		};
	} else if (userType === 2) {
		return {
			lower: lower,
			upper: null,
		};
	} else if (userType === 3) {
		upper.setDate(upper.getDate() + 6);
		return {
			lower: lower,
			upper: upper,
		};
	} else if (userType === 4) {
		upper.setDate(upper.getDate() + 2);
		return {
			lower: lower,
			upper: upper,
		};
	} else {
		return null;
	}
});
</script>

<style lang="scss" scoped></style>
