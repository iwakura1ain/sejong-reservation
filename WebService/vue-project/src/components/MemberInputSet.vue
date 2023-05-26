<template>
	<div class="member-input-set">
		<x-circle-button class="btn" @click="removeMember" />
		<div>
			<text-input
				class="name"
				:value="name"
				@input="updateName"
				placeholder="이름"
			/>
			<text-input
				class="email"
				:value="email"
				@input="updateEmail"
				placeholder="이메일"
			/>
		</div>
	</div>
</template>

<script setup>
import XCircleButton from '@/components/XCircleButton.vue';
import TextInput from '@/components/atoms/TextInput.vue';
const props = defineProps({
	name: {
		// v-model value
		required: true,
		type: String,
		default: '',
	},
	email: {
		// v-model value
		required: true,
		type: String,
		default: '',
	},
	index: {
		required: false,
		type: Number,
		default: -1,
	},
	readonly: {
		required: false,
		type: Boolean,
		default: false,
	},
});
const emits = defineEmits(['update:name', 'update:email', 'remove-member']);

function updateName(event) {
	emits('update:name', event.target.value);
}
function updateEmail(event) {
	emits('update:email', event.target.value);
}

function removeMember() {
	emits('remove-member', props.index);
}
</script>

<style lang="scss" scoped>
.member-input-set {
	display: flex;
	align-items: center;
	margin-bottom: 8px;
	width: 100%;
	// flex-wrap: wrap;

	.btn {
		width: 32px;
		height: 32px;
	}
	> div {
		display: flex;

		.name,
		.email {
			margin: 2px 0;
		}

		.name {
			margin-left: 8px;
		}
		.email {
			margin-left: 8px;
			width: 50vw;
		}
	}

	// .readonly {
	// 	border-radius: $box-radius;
	// 	border: 1px solid $sejong-grey;
	// 	background-color: lightgrey;
	// 	color: $sejong-grey;
	// 	padding: 8px;
	// }
}

@media (max-width: 546px) {
	.member-input-set {
		> div {
			flex-direction: column;
			align-items: stretch;
			.email {
				width: auto;
			}
		}
	}
}
</style>
