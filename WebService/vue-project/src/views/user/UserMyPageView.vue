<template>
	<div id="user-my-page-view">
		<section-header>마이페이지</section-header>

		<div class="profile-container">
			<section-header size="small">내 정보</section-header>
			<p class="name">{{ userInfo.name }}</p>
			<p class="user-id">{{ userInfo.id }}</p>
			<p class="user-email">{{ userInfo.email }}</p>
			<div class="user-category">
				<p class="user-dept">{{ userDeptStr }}</p>
				<p class="user-type">{{ userTypeStr }}</p>
			</div>

			<router-link to="/mypage/profile/edit">
				<filled-button class="edit-profile-btn">정보수정</filled-button>
			</router-link>
		</div>

		<div class="reservation-history-container">
			<section-header size="small">내 예약 기록</section-header>
			<div class="filter-container"></div>
			<div class="mypage-calendar-wrap">
				<!-- <Calendar :interactionTarget="0" :year="" /> -->
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import SectionHeader from '@/components/atoms/SectionHeader.vue';
import FilledButton from '@/components/atoms/FilledButton.vue';
// import Calendar from '@/components/Calendar.vue';
import { userStore, userTypeStr, userDeptStr } from '@/stores/user.js';

const userInfo = userStore.value.getInfo();

// 내 예약 기록
const filter = ref({
	topicKeyword: '', // 회의 주제에 대해 검색할 내용
	room: {
		building: '', // 회의실 건물이름
		name: '', // 회의실 이름(호수)
	},
	meetingDate: {
		// 회의 날짜
		year: -1, // 년
		month: -1, // 월
		day: -1, // 일
	},
	reservationType: -1, // 단건/정기 예약 구분
});
</script>

<style lang="scss" scoped>
#user-my-page-view {
	.profile-container {
		margin-bottom: 24px;
		p {
			margin: 8px 0;
		}
		.name {
			font-size: 1.5rem;
			font-weight: bold;
		}
		.user-category {
			display: flex;
			p {
				margin-right: 8px;
				font-size: 1.4rem;
			}
			margin-bottom: 12px;
		}

		.edit-profile-btn {
			margin: 0;
		}
	}

	.reservatin-history-container {
	}
}
</style>
