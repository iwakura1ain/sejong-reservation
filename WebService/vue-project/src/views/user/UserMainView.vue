<template>
	<div id="user-main-view">
		<section-header>예정된 회의</section-header>
		<div class="reservation-card-container">
			<reservation-card :reservation="data[0]"></reservation-card>
			<reservation-card :reservation="data[1]"></reservation-card>
			<reservation-card :reservation="data[2]"></reservation-card>
		</div>

		<section-header>모든 예약 내역</section-header>
		<month-calendar />
	</div>
</template>

<script setup>
import { ref } from 'vue';

import FilledButton from '@/components/atoms/FilledButton.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import ReservationCard from '@/components/atoms/ReservationCard.vue';
import MonthCalendar from '@/components/MonthCalendar.vue';

const subdata = {
	creatorID: -1,
	creatorName: '이원진',
	members: ['장호진', '안창언', '한수현', '이원진', '장호진'],
	reservationRoomID: -1,
	reservationRoomBuilding: '대양AI센터',
	reservationRoomName: '835호',
	isRegular: false,
};

const data = ref([
	{
		reservationDate: '2023-05-10',
		reservationTimeslot: [50, 51, 52],
		reservationTopic: '테스트 _ 1',
		...subdata,
	},
	{
		reservationDate: '2023-05-11',
		reservationTimeslot: [120, 121, 122, 123, 124, 125, 126, 127, 128],
		reservationTopic: '테스트 _ 2',
		...subdata,
	},
	{
		reservationDate: '2023-05-12',
		reservationTimeslot: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
		reservationTopic: '테스트 _ 3',
		...subdata,
	},
]);

const qrcodeTempImg =
	'https://www.investopedia.com/thmb/hJrIBjjMBGfx0oa_bHAgZ9AWyn0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/qr-code-bc94057f452f4806af70fd34540f72ad.png';
</script>

<style lang="scss" scoped>
#user-main-view {
	.reservation-card-container {
		display: flex;
		justify-content: center;
		flex-wrap: wrap;
	}
}
</style>
