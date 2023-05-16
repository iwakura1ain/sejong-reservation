<template>
	<div class="member-input-set">
		<template v-if="readonly">
			<p class="name readonly">{{ name }}</p>
			<p class="email readonly">{{ email }}</p>
		</template>
		<template v-else>
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
			<minus-round-button @click="removeMember" />
		</template>
	</div>
</template>

<script setup>
import MinusRoundButton from '@/components/MinusRoundButton.vue';
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
	margin-bottom: 8px;
	.name {
		width: 64px;
	}
	.email {
		width: 512px;
		margin-left: 8px;
	}

	.readonly {
		border-radius: $box-radius;
		border: 1px solid $sejong-grey;
		background-color: lightgrey;
		color: $sejong-grey;
		padding: 8px;
	}
}

@media (max-width: 768px) {
	.member-input-set {
		.email {
			flex: 1;
		}
	}
}
</style>
