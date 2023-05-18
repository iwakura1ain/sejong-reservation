import { createRouter, createWebHistory } from 'vue-router';

// 뷰 불러오기 ------------------------------------
// 공통 뷰
import NotFoundView from '@/views/common/NotFoundView.vue';
import LandingView from '@/views/common/LandingView.vue';
import LoginView from '@/views/common/LoginView.vue';
import RegisterView from '@/views/common/RegisterView.vue';

// 사용자 뷰
import UserMainView from '@/views/user/UserMainView.vue';
import MakeQuickReservationView from '@/views/user/MakeQuickReservationView.vue';
import MakeReservationView from '@/views/user/MakeReservationView.vue';
import ReservationHistoryView from '@/views/user/ReservationHistoryView.vue';
import UserMyPageView from '@/views/user/UserMyPageView.vue';
import UserEditProfileView from '@/views/user/UserEditProfileView.vue';
import SuccessfullyReservedView from '@/views/user/SuccessfullyReservedView.vue';

// 관리기능 뷰
import ManageMainView from '@/views/manager/ManageMainView.vue';
import ManageReservationView from '@/views/manager/ManageReservationView.vue';
import ManageRoomView from '@/views/manager/ManageRoomView.vue';
import ManageUserView from '@/views/manager/ManageUserView.vue';

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
		props: true, // "UserMainView" passes "startDateProp"
	},
	{
		path: '/reservation/done',
		name: 'SuccessfullyReserved',
		component: SuccessfullyReservedView,
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
];

// 라우터 객체 생성
const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
