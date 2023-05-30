import { reactive, computed } from 'vue';
import { USER_TYPE, DEPT_TYPE } from '@/assets/constants.js';
import { userService } from '@/assets/scripts/requests/request.js';

export const userInfoStore = reactive({
	data: {
		id: -1, // 학직번
		name: '',
		email: '',
		phone: '',
		type: -1, // 1:관리자, 2:교수, 3:대학원생, 4:학부생
		dept: -1, // 1:컴공과, 2:기타학과
		noShow: -1, // 노쇼 카운트
	},

	clear: function () {
		// userInfoStore 내용을 빈 값으로 만드는 메소드
		// this.data = { ...template };
		this.data.id = template.id;
		this.data.name = template.name;
		this.data.email = template.email;
		this.data.phone = template.phone;
		this.data.type = template.type;
		this.data.dept = template.id;
		this.data.noShow = template.noShow;
	},
	set: function (_data) {
		this.data.id = _data.id;
		this.data.name = _data.name;
		this.data.email = _data.email;
		this.data.phone = _data.phone;
		this.data.type = _data.type;
		this.data.dept = _data.dept;
		this.data.noShow = _data.noShow;
	},
	setFromBackend: async function (accessToken) {
		try {
			const res = await userService.getAuthInfo(accessToken);
			if (!res.status) {
				throw new Error(res);
			}
			this.set(res.data);
		} catch (err) {
			console.error(err, err.message);
			throw new Error(err);
		}
	},
	get: function () {
		return userInfoStore.data;
		// return {
		// 	id: userInfoStore.data.id,
		// 	name: userInfoStore.data.name,
		// 	email: userInfoStore.data.email,
		// 	phone: userInfoStore.data.phone,
		// 	type: userInfoStore.data.type,
		// 	dept: userInfoStore.data.dept,
		// 	noShow: userInfoStore.data.noShow,
		// };
	},
});

export const userTypeStr = computed(() => {
	if (userInfoStore.data.type === USER_TYPE.ADMIN) {
		return '관리자';
	} else if (userInfoStore.data.type === USER_TYPE.PROFESSOR) {
		return '교수';
	} else if (userInfoStore.data.type === USER_TYPE.GRAD_STUDENT) {
		return '대학원생';
	} else if (userInfoStore.data.type === USER_TYPE.UNDER_GRAD_STUDENT) {
		return '학부생';
	} else {
		//console.error('사용자 유형이 올바르지 않습니다.');
		return '올바르지 않은 사용자 유형';
	}
});

export const userDeptStr = computed(() => {
	if (userInfoStore.data.dept === DEPT_TYPE.COMPUTER) {
		return '컴퓨터공학과';
	} else if (userInfoStore.data.dept === DEPT_TYPE.OTHERS) {
		return '기타 학과';
	} else {
		//console.error('학과 유형이 올바르지 않습니다.');
		return '올바르지 않은 학과 유형';
	}
});

export const userIsLogin = computed(() => {
	return userInfoStore.data.id !== -1;
});

const template = {
	id: -1, // 학직번
	name: '',
	email: '',
	phone: '',
	type: -1, // 1:관리자, 2:교수, 3:대학원생, 4:학부생
	dept: -1, // 1:컴공과, 2:기타학과
	noShow: -1, // 노쇼 카운트
};
