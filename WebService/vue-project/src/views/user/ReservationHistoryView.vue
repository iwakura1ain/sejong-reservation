<template>
	<div id="reservation-history-view">
		<section-header>내 예약 조회</section-header>
		<div>
			<div class="filter-container">
				<div class="field-row">
					<div class="field-set">
						<span class="field-label year">주제 검색</span>
						<text-input
							class="field-value"
							v-model="filter.topic"
							style="height: 32px"
						/>
					</div>
				</div>
				<div class="field-row">
					<div class="field-set">
						<span class="field-label year">회의실 건물</span>
						<vue-select
							class="field-value year"
							v-model="filter.room.address1"
							:options="selectOptions.room.address1"
							placeholder="회의실 건물"
							:disabled="selectOptions.room.address1.length === 0"
						/>
					</div>

					<div class="field-set">
						<span class="field-label month">회의실 이름</span>
						<vue-select
							class="field-value month"
							v-model="filter.room.name"
							:options="selectOptions.room.name"
							placeholder="회의실 이름"
							:disabled="selectOptions.room.name.length === 0"
						/>
					</div>
				</div>

				<div class="field-row">
					<div class="field-set">
						<span class="field-label date" style="margin: 0">일정 범위</span>
						<div class="field-value datepicker-container" style="display: flex">
							<div class="date-after" style="flex: 1; margin: 0 4px">
								<date-picker
									v-model="filter.date.after"
									:use-limit="false"
									style="
										width: 100%;
										font-size: 1rem;
										padding: 2px;
										height: 32px;
									"
								/>
							</div>
							<div
								class="date-before"
								style="flex: 1; display: flex; align-items: center"
							>
								<span style="padding-right: 4px">─</span>
								<div style="flex: 1">
									<date-picker
										v-model="filter.date.before"
										:use-limit="false"
										style="
											width: 100%;
											font-size: 1rem;
											padding: 2px;
											height: 32px;
										"
									/>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="field-row">
					<div class="field-set">
						<span class="field-label year">예약 유형</span>
						<vue-select
							class="field-value year"
							v-model="filter.type"
							:options="selectOptions.type"
							placeholder="표시할 예약 유형"
						/>
					</div>
				</div>

				<div style="display: flex; align-items: center; margin-top: 8px">
					<p>{{ reservationList.length }}건 조회됨</p>
					<div style="margin-left: auto">
						<!-- 달력 보기 지우기 버튼 -->
						<filled-button
							v-if="!isCalendarOpened"
							@click="handleToggleClaendar"
							style="margin-right: 8px"
							>달력보기</filled-button
						>
						<filled-button
							v-else
							color="white"
							@click="handleToggleClaendar"
							style="margin-right: 8px"
							>달력닫기</filled-button
						>

						<!-- 조회버튼 -->
						<filled-button @click="fetchReservationList" style="margin: 0"
							>조회하기</filled-button
						>
					</div>
				</div>
			</div>
			<div class="calendar-container">
				<multi-calendar
					v-if="isCalendarOpened"
					v-model:target-date="targetDate"
					:reservation-list="reservationList"
				/>
			</div>
			<div class="reservation-card-container">
				<reservation-card
					v-for="item in reservationList.slice().reverse()"
					:key="item.id"
					:rsv-data="item"
					:room-data="fetchedRoomStore.getById(item.roomId)"
					:user-name="userInfoStore.get().name"
					@click="goDetailPage(item.id, item.reservationType)"
				/>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import ReservationCard from '@/components/atoms/ReservationCard.vue';
import MultiCalendar from '@/components/MultiCalendar.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
import TextInput from '@/components/atoms/TextInput.vue';
import DatePicker from '@/components/wrappers/Vue3DatepickerWrapper.vue';
import { fetchedRoomStore } from '@/stores/fetchedRoom.js';
import { userInfoStore } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import { loadingStore } from '@/stores/loading.js';
import { reservationService } from '@/assets/scripts/requests/request.js';
import makeToast from '@/assets/scripts/utils/makeToast.js';
import VueSelect from '@/components/wrappers/VueNextSelectWrapper.vue';
import getFormattedStringFromDateObj from '@/assets/scripts/utils/getFormattedStringFromDateObj.js';
import getWeekNumber from '@/assets/scripts/utils/getWeekNumber.js';

// 달력 --------------------------------------------------
const isCalendarOpened = ref(false);

const nowDateObj = new Date();
const targetDate = ref({
	year: nowDateObj.getFullYear(),
	month: nowDateObj.getMonth() + 1,
	day: nowDateObj.getDate(),
	week: getWeekNumber(
		`${nowDateObj.getFullYear()}-${
			nowDateObj.getMonth() + 1
		}-${nowDateObj.getDate()}`,
	),
});

function handleToggleClaendar() {
	isCalendarOpened.value = !isCalendarOpened.value;
}

// 필터 form 유지 로직 ------------------------------------
const filter = ref({
	topic: '',
	room: {
		address1: '',
		name: '',
	},
	date: {
		after: new Date(),
		before: new Date(),
	},
	type: '전체',
});

const selectOptions = ref({
	room: {
		address1: [],
		name: [],
		idForName: [], // name배열의 각 원소에 대한 회의실id
	},
	type: [
		'전체',
		'단건예약',
		'정기예약' /*, '정기예약(풀어보기)', '정기예약(묶어보기)'*/,
	],
});
watch(
	() => filter.value.room.address1,
	() => {
		filter.value.name = '';
		selectOptions.value.room.name.splice(0);
		selectOptions.value.room.idForName.splice(0);
		fetchedRoomStore.getAll().forEach(room => {
			if (room.address1 === filter.value.room.address1) {
				selectOptions.value.room.name.push(room.name);
				selectOptions.value.room.idForName.push(room.id);
			}
		});
	},
);
watch(
	() => filter.value.date.after,
	() => {
		const date = filter.value.date.after;
		(targetDate.value.year = date.getFullYear()),
			(targetDate.value.month = date.getMonth() + 1),
			(targetDate.value.day = date.getDate()),
			(targetDate.value.week = getWeekNumber(
				`${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`,
			));
	},
);
watch(
	() => filter.value.date.before,
	() => {
		const date = filter.value.date.before;
		(targetDate.value.year = date.getFullYear()),
			(targetDate.value.month = date.getMonth() + 1),
			(targetDate.value.day = date.getDate()),
			(targetDate.value.week = getWeekNumber(
				`${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`,
			));
	},
);

// 예약 fetch 로직 ----------------------------------------
const reservationList = ref([]);

const fetchOptions = computed(() => {
	const optionObj = {
		after: getFormattedStringFromDateObj(filter.value.date.after, 'YYYY-MM-DD'),
		before: getFormattedStringFromDateObj(
			filter.value.date.before,
			'YYYY-MM-DD',
		),
		creator: userInfoStore.get().id,
	};

	// room
	const idx = selectOptions.value.room.name.findIndex(
		e => e === filter.value.room.name,
	);
	console.log(idx);
	if (idx != -1) {
		const selectedRoomId = selectOptions.value.room.idForName[idx];
		optionObj.room = selectedRoomId;
	}

	// reservationType
	if (filter.value.type === '단건예약') {
		optionObj.onlySingleType = true;
	}

	return optionObj;
});

async function fetchReservationList() {
	try {
		loadingStore.start();

		// 건물을 선택했지만 회의실 이름 선택을 안한경우 fetch안함
		const roomAdr1 = filter.value.room.address1;
		const roomName = filter.value.room.name;
		if (roomAdr1 && roomAdr1 !== '전체' && !roomName) {
			makeToast('회의실 이름이 선택되지 않았습니다', 'error');
			return;
		}

		// 통신
		const accessToken = userTokenStore.getAccessToken();
		const res = await reservationService.getMyFullData(
			fetchOptions.value,
			accessToken,
		);
		if (!res.status) {
			console.error(res);
			throw new Error(res);
		}

		const typeFiltered = filterByType(res.data);
		const nameFiltered = filterByName(typeFiltered);
		reservationList.value = nameFiltered;
	} catch (err) {
		const msg = err.msg;
		console.error(err, msg);
		if (msg === '') {
			makeToast('', 'error');
		} else if (msg === '') {
			makeToast('', 'error');
		} else {
			makeToast('알 수 없는 오류입니다', 'error');
		}
	} finally {
		loadingStore.stop();
	}
}

function filterByType(reservations) {
	if (filter.value.type === '단건예약') {
		return reservations.filter(rsv => rsv.reservationType === null);
	} else if (
		(filter.value.type === '정기예약') |
		(filter.value.type === '정기예약(풀어보기)') |
		(filter.value.type === '정기예약(묶어보기)')
	) {
		return reservations.filter(rsv => rsv.reservationType !== null);
	} else {
		// 'wjscp'
		return reservations;
	}
}

function filterByName(reservations) {
	return reservations.filter(rsv => rsv.topic.includes(filter.value.topic));
}

// 상세 페이지로 가기 ---------------------------------
function goDetailPage(id, reservationType) {
	console.log(id, reservationType);
	router.push({
		name: 'ReservationDetail',
		state: {
			id,
			reservationType,
		},
	});
}

// 초기화
const router = useRouter();

async function init() {
	// select 옵션 초기화
	selectOptions.value.room.address1 = [
		'전체',
		...new Set(fetchedRoomStore.getAll().map(room => room.address1)),
	];

	// 필터값 초기화
	const now = new Date();
	filter.value.date.after = new Date(now.setDate(now.getDate() - 7));
	filter.value.date.before = new Date(now.setMonth(now.getMonth() + 1));

	await fetchReservationList();
}
init();
</script>

<style lang="scss" scoped>
#reservation-history-view {
	width: 100%;
}
.filter-container {
	width: 100%;
	.field-row {
		display: flex;
		flex-wrap: wrap;
		width: 100%;

		.field-set {
			flex: 1;
			display: flex;
			align-items: center;
			justify-content: flex-end;
			margin: 8px;
			// width: 100%;
			.field-label {
				margin-right: 4px;
			}
			.field-value {
				flex: 1;
			}
			.datepicker-container {
				display: flex;
			}
		}
	}
	@media (max-width: 768px) {
		.field-row {
			flex-direction: column;
		}
		.field-set {
			width: 100%;
			margin: 8px 0;
		}
		.field-value {
			flex: 1;
		}

		.datepicker-container {
			flex-direction: column;
			.date-after {
				margin-right: 0;
			}
			.date-before {
				margin-top: 8px;
				margin-left: 4px;
			}

			.date-after,
			.date-before {
				max-width: 280px;
				min-width: 180px;
			}
		}
	}
}
.calendar-container {
}
.reservation-card-container {
	margin-top: 24px;
	display: flex;
	flex-direction: column;
	align-items: center;
}
</style>
