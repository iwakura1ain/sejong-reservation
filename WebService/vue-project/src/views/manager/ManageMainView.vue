<template>
	<div id="manage-main-view">
		<manage-tool-header name="관리자 도구" />

		<section-header>통계 보고서</section-header>
		<div class="stat-range">
			<p style="font-weight: bold">통계 산출 기간</p>
			<p>{{ `${statDateRange.start} ~ ${statDateRange.end}` }}</p>
		</div>
		<div class="stat-report-container">
			<!-- 이용완료, 이용예정, 이용안함(노쇼)의 비율 파이차트 -->

			<div class="use-status-container">
				<section-header size="small">이용상태</section-header>
				<template v-if="useStatusChartData.length > 0">
					<Responsive class="w-full">
						<template #main="{ width }">
							<Chart
								direction="circular"
								:size="{ width: 400, height: 400 }"
								:data="useStatusChartData"
								:config="{ controlHover: false }"
								:margin="{
									left: 20,
									top: 20,
									right: 0,
									bottom: 20,
								}"
							>
								<template v-if="useStatusChartColors.length > 0" #layers>
									<Pie
										:dataKeys="['label', 'value']"
										:pie-style="{
											innerRadius: 80,
											padAngle: 0.05,
											colors: useStatusChartColors,
										}"
									/>
								</template>
								<template #widgets>
									<Tooltip
										:config="{
											label: { label: '상태' },
											value: { label: '건수' },
										}"
										hideLine
									/>
								</template>
							</Chart>
						</template>
					</Responsive>

					<div class="text-desc">
						<p class="item" v-for="(item, index) in useStatusData" :key="index">
							<span class="label">{{ item.label }}</span>
							<span class="value">{{ item.value }}건</span>
						</p>
					</div>
				</template>

				<template v-else>
					<empty-sign style="padding: 48px 0" />
				</template>
			</div>

			<!-- 회의실 전체 이용시간 대비 예약률 bar차트 -->
			<div class="utilization-container">
				<section-header size="small">회의실 이용률</section-header>
				<tempalte v-if="roomUtilizationChartData.length > 0">
					<Responsive class="w-full">
						<template #main="{ width }">
							<Chart
								direction="circular"
								:size="{ width: 400, height: 400 }"
								:data="roomUtilizationChartData"
								:config="{ controlHover: false }"
								:margin="{
									left: 20,
									top: 20,
									right: 0,
									bottom: 20,
								}"
							>
								<template v-if="roomUtilizationChartColors.length > 0" #layers>
									<Pie
										:dataKeys="['label', 'value']"
										:pie-style="{
											innerRadius: 80,
											padAngle: 0.05,
											colors: roomUtilizationChartColors,
										}"
									/>
								</template>

								<template #widgets>
									<Tooltip
										:config="{
											label: { label: '이용여부' },
											value: { label: '시간(분)' },
										}"
										hideLine
									/>
								</template>
							</Chart>
						</template>
					</Responsive>
					<div class="text-desc">
						<p
							class="item"
							v-for="(item, index) in roomUtilizationData"
							:key="index"
						>
							<span class="label">{{ item.label }}</span>
							<span class="value">{{
								`${parseInt(item.value / 60)}시간 ${item.value % 60}분`
							}}</span>
						</p>
					</div>
				</tempalte>

				<template v-else>
					<empty-sign style="padding: 48px 0" />
				</template>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';
import ManageToolHeader from '@/layouts/Manage/ManageToolHeader.vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import { userTokenStore } from '@/stores/userToken.js';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { loadingStore } from '@/stores/loading.js';
import { reservationService } from '@/assets/scripts/requests/request.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import getDateDifference from '@/assets/scripts/utils/getDateDifference.js';
import getDateStringInThreeDays from '@/assets/scripts/utils/getDateStringInThreeDays.js';
import EmptySign from '@/components/atoms/EmptySign.vue';
import { Chart, Responsive, Pie, Tooltip } from 'vue3-charts';

const statDateRange = ref({
	start: '',
	end: '',
});

// 이용상태 산출 / 차트 렌더링 로직 -------------------------------------
const useStatusData = ref([
	{ label: '전체', value: 0 },
	{ label: '⚪이용예정', value: 0 }, // roomUsed = 0
	{ label: '🟢이용완료', value: 0 }, // roomUsed = 1
	{ label: '🔴이용안함', value: 0 }, // roomUsed = -1
]);
const useStatusChartData = computed(() => {
	return useStatusData.value.filter(
		el => el.value !== 0 && el.label !== '전체',
	);
});

const useStatusChartColors = computed(() => {
	const colors = [];

	for (let el of useStatusChartData.value) {
		console.log(el);
		if (el.label === '⚪이용예정') colors.push('#DADADA');
		else if (el.label === '🟢이용완료') colors.push('#80B747');
		else if (el.label === '🔴이용안함') colors.push('#C3002F');
	}
	console.log(colors);
	return colors;
});

function buildUseStatusData(reservations) {
	const _useStatusData = {
		total: 0,
		complete: 0, // roomUsed = 1
		pending: 0, // roomUsed = 0
		noshow: 0, // roomUsed = -1
	};
	reservations.forEach(rsv => {
		if (rsv.roomUsed === 1) _useStatusData.complete++;
		else if (rsv.roomUsed === 0) _useStatusData.pending++;
		else if (rsv.roomUsed === -1) _useStatusData.noshow++;
	});
	_useStatusData.total =
		_useStatusData.complete + _useStatusData.pending + _useStatusData.noshow;

	// 반환
	const arr = [
		{ label: '전체', value: _useStatusData.total },
		{ label: '⚪이용예정', value: _useStatusData.pending }, // roomUsed = 0
		{ label: '🟢이용완료', value: _useStatusData.complete }, // roomUsed = 1
		{ label: '🔴이용안함', value: _useStatusData.noshow }, // roomUsed = -1
	];
	return arr;
}

// 회의실 이용률 산출 및 차트 렌더링 로직 -------------------------------------
const roomUtilizationData = ref([
	{ label: '운영시간', value: 0 },
	{ label: '🟢이용시간', value: 0 },
	{ label: '⚪유휴시간', value: 0 },
]);
const roomUtilizationChartData = computed(() => {
	return roomUtilizationData.value.filter(
		el => el.value !== 0 && el.label !== '운영시간',
	);
});
const roomUtilizationChartColors = computed(() => {
	const colors = [];

	for (let el of roomUtilizationChartData.value) {
		if (el.label === '🟢이용시간') colors.push('#80B747');
		else if (el.label === '⚪유휴시간') colors.push('#DADADA');
	}
	return colors;
});

function buildRoomUtilizationData(reservations, rooms) {
	const _roomUtilizationData = {
		totalMinutes: 0,
		usedMinutes: 0,
		unUsedMinutes: 0,
	};

	// total Minutes (이용률의 모수) 구하기
	// -- 하루당 이용가능 시간이 몇분이냐
	rooms.forEach(room => {
		const [openH, openM] = room.time.open.split(':');
		const openMins = parseInt(openH) * 60 + parseInt(openM);
		const [closeH, closeM] = room.time.close.split(':');
		const closeMins = parseInt(closeH) * 60 + parseInt(closeM);

		const availableMins = closeMins - openMins;
		_roomUtilizationData.totalMinutes += availableMins;
	});

	// -- 모수가 며칠이냐
	const firstReservationDate = new Date(
		`${reservations[0].meetingDatetime.date}T00:00`,
	);
	const tomorrow = new Date(`${getDateStringInThreeDays().tomorrow}T00:00`);
	const dayBetweenFirstReservationAndToday = getDateDifference(
		firstReservationDate,
		tomorrow,
	).dayDiff;
	_roomUtilizationData.totalMinutes *= dayBetweenFirstReservationAndToday;

	// usedMinutes 구하기 (예약된 회의실의 총 이용시간)
	// usedMinutes = 전체 예약의 예약시간(분) 합 - 노쇼한 예약의 예약시간(분) 합
	reservations.forEach(rsv => {
		if (rsv.roomUsed === -1) {
			return;
		}

		const [startH, startM] = rsv.meetingDatetime.startTime.split(':');
		const startMins = parseInt(startH) * 60 + parseInt(startM);
		const [endH, endM] = rsv.meetingDatetime.endTime.split(':');
		const endMins = parseInt(endH) * 60 + parseInt(endM);

		_roomUtilizationData.usedMinutes += endMins - startMins;
	});

	// unUsedMinutes 구하기 (예약되지 않은 회의실의 총 이용시간)
	_roomUtilizationData.unUsedMinutes =
		_roomUtilizationData.totalMinutes - _roomUtilizationData.usedMinutes;

	// 반환
	const arr = [
		{ label: '운영시간', value: _roomUtilizationData.totalMinutes },
		{ label: '🟢이용시간', value: _roomUtilizationData.usedMinutes },
		{ label: '⚪유휴시간', value: _roomUtilizationData.unUsedMinutes },
	];
	return arr;
}

// 초기화 로직 -------------------------------------
async function init() {
	try {
		loadingStore.start();

		// 전체 예약 정보 불러오기
		const accessToken = userTokenStore.getAccessToken();
		const rsvRes = await reservationService.get(
			{
				before: getDateStringInThreeDays().today,
			},
			accessToken,
		);
		if (!rsvRes.status) {
			console.error(rsvRes);
			throw new Error(rsvRes);
		}
		console.log(rsvRes);
		console.log(fetchedRoomStore.getAll());

		// 통게 산출기간 설정
		statDateRange.value.start = rsvRes.data[0].meetingDatetime.date;
		statDateRange.value.end = getDateStringInThreeDays().today;

		// 이용 상태 데이터 구성
		useStatusData.value = buildUseStatusData(rsvRes.data);
		console.log(useStatusData.value);

		// 회의실 이용률 데이터 구성
		roomUtilizationData.value = buildRoomUtilizationData(
			rsvRes.data,
			fetchedRoomStore.getAll(),
		);
		console.log(roomUtilizationData.value);
	} catch (err) {
		console.error(err);
		makeToast('통계자료를 불러오는 중 오류가 발생했습니다', 'error');
	} finally {
		loadingStore.stop();
	}
}
init();
</script>

<style lang="scss" scoped>
#manage-main-view {
	width: 100%;

	.stat-range {
		display: flex;
		flex-wrap: wrap;
		p {
			padding: 8px;
		}
	}
	.stat-report-container {
		width: 100%;
		display: flex;
		flex-wrap: wrap;
		.use-status-container,
		.utilization-container {
			display: flex;
			flex-direction: column;
			align-items: center;
			text-align: center;
			flex: 1;
			padding: 2rem;
			.text-desc {
				width: fit-content;
				text-align: left;
				.item {
					margin-bottom: 8px;
				}
				.label {
					font-weight: bold;
					margin-right: 4px;
				}
			}
		}
	}
}

@media (max-width: 768px) {
	.stat-range {
		flex-direction: column;
		align-items: center;
	}
	.stat-report-container {
		flex-direction: column;
	}
}
</style>

<style lang="scss">
.chart {
	text-align: center;
	max-width: 90vw;
	height: auto;
	> svg {
		max-width: 100%;
	}
	// text {
	color: white;
	// }
	.widgets .v-tooltip-content * {
		color: $sejong-grey !important;
	}
	.widgets .v-tooltip-content > div {
		border: 1px solid $sejong-grey !important;
		background-color: rgba(255, 255, 255, 0.8) !important;
	}
}
</style>
