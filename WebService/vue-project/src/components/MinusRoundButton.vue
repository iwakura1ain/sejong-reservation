<template>
	<filled-button class="minus-round-button" :color="'white'">
		<template #icon>
			<img :src="minusimg" />
		</template>
	</filled-button>
</template>

<script setup>
import FilledButton from '@/components/atoms/FilledButton.vue';
import minusimg from '@/assets/images/icons/close.png';
</script>

<style lang="scss" scoped>
.minus-round-button {
	width: 28px;
	height: 28px;
	border-radius: 50%;

	display: flex;
	justify-content: center;
	align-items: center;
	img {
		width: 16px;
		height: 16px;
	}
}
</style>
