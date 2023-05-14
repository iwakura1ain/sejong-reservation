<template>
	<div id="user-main-view">
		<section-header>예정된 회의</section-header>
		<h1>M A I N</h1>
		<router-link to="/asdf">not found 표시</router-link>

		<br />
		<filled-button color="red">red</filled-button>
		<filled-button color="white">white</filled-button>
		<br /><br />
		<div class="reservation-card-container">
			<reservation-card :reservation="data[0]"></reservation-card>
			<reservation-card :reservation="data[1]"></reservation-card>
			<reservation-card :reservation="data[2]"></reservation-card>
		</div>
	</div>
</template>

<script setup>
import FilledButton from '@/components/atoms/FilledButton.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import ReservationCard from '@/components/atoms/ReservationCard.vue';
import { ref } from 'vue';

const subdata = {
	creatorID: -1,
	creatorName: '이원진',
	members: ['장호진', '안창언', '한수현', '교수님', '캡스톤'],
	reservationRoomID: -1,
	reservationRoomBuilding: '대양AI센터',
	reservationRoomName: '대충 몇호',
	isRegular: false,
};

const data = ref([
	{
		reservationDate: '2023-04-22',
		reservationTimeslot: [50, 51, 52],
		reservationTopic: '테스트 _ 1',
		...subdata,
	},
	{
		reservationDate: '2023-04-23',
		reservationTimeslot: [120, 121, 122, 123, 124, 125, 126, 127, 128],
		reservationTopic: '테스트 _ 2',
		...subdata,
	},
	{
		reservationDate: '2023-05-01',
		reservationTimeslot: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
		reservationTopic: '테스트 _ 3',
		...subdata,
	},
]);
</script>

<style lang="scss" scoped>
#user-main-view {
	display: flex;
	flex-direction: column;
	align-items: center;

	padding: $routerview-padding;

	.reservation-card-container {
		display: flex;
		justify-content: center;
		flex-wrap: wrap;
	}
}
</style>
