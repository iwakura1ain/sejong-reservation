<template>
	<filled-button class="x-circle-button" :color="'white'">
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
.x-circle-button {
	width: 32px;
	height: 32px;
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
