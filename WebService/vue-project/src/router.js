// View 목록 문서
// https://www.notion.so/sogeumguideopbap/Web-Service-193dca19bff94c64a5673b7a0f116fbe?pvs=4#55d729ed74cd460b89a4090fa9bf6eb5

import { createRouter, createWebHistory } from 'vue-router';
import { userInfoStore } from '@/stores/userInfo.js';
import { userTokenStore } from '@/stores/userToken.js';
import { userService } from '@/assets/scripts/requests/request.js';

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
const notRequireLogin = ['Login', 'Register', 'Landing'];
const RequireAdmin = [
	'ManageMain',
	'ManageReservation',
	'ManageUser',
	'ManageRoom',
	'MakeRoom',
];
router.beforeEach(async (to, from, next) => {
	// 로그인이 필요하지 않은 페이지들은 그냥 갈길 갑시다.
	// console.log('1', to.name, from.name);
	if (notRequireLogin.includes(to.name)) {
		next();
		return;
	}

	// 로그인이 필요한 페이지들.
	try {
		const { accessToken, refreshToken } = userTokenStore.get();

		// 액세스토큰, 리프레시토큰 둘 중 하나라도 저장된 것 없으면 로그인으로 갑시다
		if (!userTokenStore.exist()) {
			next({ name: 'Login' });
			return;
		}

		// 만약 관리자여야 진입가능한 곳인데 일반사용자가 들어갔으면 로그인으로 갑시다
		const resAuth = await userService.getAuthInfo(accessToken);
		if (!resAuth.status) {
			throw new Error(resAuth);
		}
		if (RequireAdmin.includes(to.name) && resAuth.data.type !== 1) {
			await userService.logout(accessToken);
			throw new Error(
				`ADMIN권한을 요구하는 페이지이지만 사용자가 ADMIN이 아닙니다(권한유형코드:${resAuth.data.type})`,
			);
		}

		if (from.name === undefined) {
			next();
			return;
		}

		// 두 토큰이 저장돼있다면 refresh Auth를 합시다
		// const res = await userService.refreshAuth(refreshToken);
		// if (!res.status) {
		// 	throw new Error();
		// }

		// 새로운 액세스 토큰을 저장하고 올바른 토큰인지 검사합시다
		// userTokenStore.setAccessToken(res.data);
		// console.log('3', to.name, res.data);

		// 모든 시련을 이겨냈다면 이제 가려던 길을 갑시다
		next();
	} catch (err) {
		userInfoStore.clear();
		userTokenStore.clear();
		next({ name: 'Login', state: { failToAuth: true } });
	}
});

export default router;
