<template>
	<div class="radio-group">
		<filled-button
			v-for="(btn, index) in buttons"
			:key="index"
			class="radio-btn"
			:class="{
				'left-round': len >= 2 && index === 0,
				'right-round': len >= 2 && index === len - 1,
				'both-round': len === 1,
			}"
			:color="selectedValue === btn.value ? 'red' : 'white'"
			@click="updateSelect(index)"
		>
			{{ btn.text }}
		</filled-button>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';
import FilledButton from '@/components/atoms/FilledButton.vue';

// define props and events
const props = defineProps({
	modelValue: {
		required: false,
		type: [Number, String, null],
		default: null,
	},
	buttons: {
		required: false,
		type: Array,
		default() {
			return [
				{ text: 'button0', value: 0 },
				{ text: 'button1', value: 1 },
				{ text: 'button2', value: 2 },
			];
		},
	},
});
const emits = defineEmits(['update:modelValue']);

// states
const selectedValue = ref(props.buttons[0].value);
const len = computed(() => {
	return props.buttons.length;
});

// event handlers
function updateSelect(index) {
	selectedValue.value = props.buttons[index].value;
	emits('update:modelValue', props.buttons[index].value);
}
</script>

<style lang="scss" scoped>
.radio-group {
	.radio-btn {
		margin: 0;
		padding: 9px;
		border-left: 0;
		border-top: 1px solid $sejong-grey;
		border-bottom: 1px solid $sejong-grey;
		border-radius: 0;
	}
	.left-round {
		border-top-left-radius: $box-radius;
		border-bottom-left-radius: $box-radius;
		border-left: 1px solid $sejong-grey;
	}
	.right-round {
		border-top-right-radius: $box-radius;
		border-bottom-right-radius: $box-radius;
		border-right: 1px solid $sejong-grey;
	}
	.both-round {
		border-radius: $box-radius;
		border: 1px solid $sejong-grey;
	}
}
</style>
