import { reactive, computed } from 'vue';
import { USER_TYPE, DEPT_TYPE } from '@/assets/constants.js';

export const userStore = reactive({
	data: {
		id: -1, // 학직번
		name: '',
		email: '',
		phone: '',
		type: -1, // 1:관리자, 2:교수, 3:대학원생, 4:학부생
		dept: -1, // 1:컴공과, 2:기타학과
		noShow: -1, // 노쇼 카운트
		accessToken: '',
		refreshToken: '',
	},

	init: function () {
		// userStore의 내용을 빈 값으로 만드는 메소드
		userStore.data = template;
	},
	set: function (_data) {
		userStore.data = _data;
	},
	getToken: function () {
		return {
			accessToken: userStore.data.accessToken,
			refreshToken: userStore.data.refreshToken,
		};
	},
	getInfo: function () {
		return {
			id: userStore.data.id,
			name: userStore.data.name,
			email: userStore.data.email,
			type: userStore.data.type,
			dept: userStore.data.dept,
			noShow: userStore.data.noShow,
		};
	},
});

export const userTypeStr = computed(() => {
	if (userStore.data.type === USER_TYPE.ADMIN) {
		return '관리자';
	} else if (userStore.data.type === USER_TYPE.PROFESSOR) {
		return '교수';
	} else if (userStore.data.type === USER_TYPE.GRAD_STUDENT) {
		return '대학원생';
	} else if (userStore.data.type === USER_TYPE.UNDER_GRAD_STUDENT) {
		return '학부생';
	} else {
		console.error('사용자 유형이 올바르지 않습니다.');
		return '올바르지 않은 사용자 유형';
	}
});

export const userDeptStr = computed(() => {
	if (userStore.data.dept === DEPT_TYPE.COMPUTER) {
		return '컴퓨터공학과';
	} else if (userStore.data.dept === DEPT_TYPE.OTHERS) {
		return '기타 학과';
	} else {
		console.error('학과 유형이 올바르지 않습니다.');
		return '올바르지 않은 학과 유형';
	}
});

const template = {
	id: -1, // 학직번
	name: '',
	email: '',
	type: -1, // 1:관리자, 2:교수, 3:대학원생, 4:학부생
	dept: -1, // 1:컴공과, 2:기타학과
	noShow: -1, // 노쇼 카운트
	accessToken: '',
	refreshToken: '',
};
