<template>
	<filled-button class="plus-round-button">
		<template #icon>
			<img :src="plusimg" />
		</template>
	</filled-button>
</template>

<script setup>
import FilledButton from '@/components/atoms/FilledButton.vue';
import plusimg from '@/assets/images/icons/plus.png';
</script>

<style lang="scss" scoped>
.plus-round-button {
	width: 36px;
	height: 36px;
	border-radius: 50%;

	display: flex;
	justify-content: center;
	align-items: center;
	img {
		width: 18px;
		height: 18px;
	}
}
</style>
