// View 목록 문서
// https://www.notion.so/sogeumguideopbap/Web-Service-193dca19bff94c64a5673b7a0f116fbe?pvs=4#55d729ed74cd460b89a4090fa9bf6eb5

import { createRouter, createWebHistory } from 'vue-router';
// import { userStore } from '@/stores/user.js';
// import { userService } from '@/assets/scripts/requests/request.js';

// 뷰 불러오기 ------------------------------------
// 공통 뷰
import NotFoundView from '@/views/common/NotFoundView.vue';
import LandingView from '@/views/common/LandingView.vue';
import LoginView from '@/views/common/LoginView.vue';
import RegisterView from '@/views/common/RegisterView.vue';
import ReservationDetailView from '@/views/common/ReservationDetailView.vue';

// 사용자 뷰
import UserMainView from '@/views/user/UserMainView.vue';
import MakeQuickReservationView from '@/views/user/MakeQuickReservationView.vue';
import MakeReservationView from '@/views/user/MakeReservationView.vue';
import ModifyReservationCommonDataView from '@/views/user/ModifyReservationCommonDataView.vue';
import ModifyReservationTimeDataView from '@/views/user/ModifyReservationTimeDataView.vue';
import AllReservationCalendarView from '@/views/user/AllReservationCalendarView.vue';
import ReservationHistoryView from '@/views/user/ReservationHistoryView.vue';
import UserMyPageView from '@/views/user/UserMyPageView.vue';
import UserEditProfileView from '@/views/user/UserEditProfileView.vue';
import SuccessfullyReservedView from '@/views/user/SuccessfullyReservedView.vue';

// 관리기능 뷰
import ManageMainView from '@/views/manager/ManageMainView.vue';
import ManageReservationView from '@/views/manager/ManageReservationView.vue';
import ManageUserView from '@/views/manager/ManageUserView.vue';
import ManageRoomView from '@/views/manager/ManageRoomView.vue';
import MakeRoomView from '@/views/manager/MakeRoomView.vue';

// 시스템 뷰 (일반사용자도 관리자도 아닌, 특별한 사용자 "system"만 접속가능)
import CheckNoShowView from '@/views/system/CheckNoShowView.vue';

// 라우터 설정 ------------------------------------
const routes = [
	// 공통 뷰
	{
		path: '/:pathMatch(.*)*',
		name: 'NotFound',
		component: NotFoundView,
	},
	{
		path: '/',
		name: 'Landing',
		component: LandingView,
	},
	{
		path: '/login',
		name: 'Login',
		component: LoginView,
	},
	{
		path: '/register',
		name: 'Register',
		component: RegisterView,
	},
	{
		path: '/reservation/detail',
		name: 'ReservationDetail',
		component: ReservationDetailView,
		// state(id, reservationType) : 백엔드 Reservation테이블의 id값과 동일(예약 식별자)
	},

	// 사용자 뷰
	{
		path: '/main',
		name: 'UserMain',
		component: UserMainView,
	},
	{
		path: '/reservation/make/quick',
		name: 'MakeQuickReservation',
		component: MakeQuickReservationView,
	},
	{
		path: '/reservation/make',
		name: 'MakeReservation',
		component: MakeReservationView,
		props: true, // "startDateProp" query
	},
	{
		path: '/reservation/done',
		name: 'SuccessfullyReserved',
		component: SuccessfullyReservedView,
	},
	{
		path: '/reservation/modify/common',
		name: 'ModifyReservationCommonData',
		component: ModifyReservationCommonDataView,
		// state push됨
	},
	{
		path: '/reservation/modify/time',
		name: 'ModifyReservationTimeData',
		component: ModifyReservationTimeDataView,
		// state push됨
	},
	{
		path: '/reservation/all',
		name: 'AllReservationCalendar',
		component: AllReservationCalendarView,
	},
	{
		path: '/reservation/history',
		name: 'ReservationHistory',
		component: ReservationHistoryView,
	},
	{
		path: '/mypage',
		name: 'UserMyPage',
		component: UserMyPageView,
	},
	{
		path: '/mypage/profile/edit',
		name: 'UserEditProfile',
		component: UserEditProfileView,
	},

	// 관리기능 뷰
	{
		path: '/manage/main',
		name: 'ManageMain',
		component: ManageMainView,
	},
	{
		path: '/manage/reservation',
		name: 'ManageReservation',
		component: ManageReservationView,
	},
	{
		path: '/manage/user',
		name: 'ManageUser',
		component: ManageUserView,
	},
	{
		path: '/manage/room',
		name: 'ManageRoom',
		component: ManageRoomView,
	},
	{
		path: '/manage/room/make',
		name: 'MakeRoom',
		component: MakeRoomView,
	},

	// system사용자용 뷰
	// ** system사용자 = 일반사용자도 관리자도 아닌, 특별한 사용자
	{
		path: '/system/check/noshow',
		name: 'CheckNoShow',
		component: CheckNoShowView,
	},
];

// 라우터 객체 생성
const router = createRouter({
	history: createWebHistory(),
	routes,
	scrollBehavior(/*to, from, savedPosition*/) {
		return { top: 0 };
	},
});

// 네이게이션 가드 설정
// const needlogin = [];
// router.beforeEach(async (to, from, next) => {

// });

export default router;
