import { ref, computed } from 'vue';
import { USER_TYPE, DEPT_TYPE } from '@/assets/constants.js';

export const userStore = ref({
	token: {
		access: '',
		refresh: '',
	},
	info: {
		id: -1, // 학직번
		name: '',
		email: '',
		type: -1, // 1:관리자, 2:교수, 3:대학원생, 4:학부생
		dept: -1, // 1:컴공과, 2:기타학과
		noShow: -1, // 노쇼 카운트
	},

	init: function () {
		// userStore의 내용을 빈 값으로 만드는 메소드
		userStore.value.token = template.token;
		userStore.value.info = template.info;
	},
	set: function (data) {
		// userStore의 값을 채우는 메소드
		/*
      인수 "data"는 userService - login의 response data.
      형식은 아래와 같음
      {
        "status": true,
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjg0MDgxMTY1LCJqdGkiOiI4NDUxYjI0My04YjMwLTQxZjItYTdiNC1kZDhlNDk4YjAyYjAiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7ImlkIjoxNzAxMTUwNiwibmFtZSI6Ilx1YzU0OFx1Y2MzZFx1YzViODIiLCJ0eXBlIjoyLCJub19zaG93IjowfSwibmJmIjoxNjg0MDgxMTY1LCJleHAiOjE2ODQwODQ3NjV9.hq8DAYJDHG6MOoM_-7jFSdyuHV0tKrJshSe9xvnIAz4",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDA4MTE2NSwianRpIjoiZmEyMDk5MDgtYmU1MC00NjNlLTk4YTMtNTE5YmY0NDViMzkwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsiaWQiOjE3MDExNTA2LCJuYW1lIjoiXHVjNTQ4XHVjYzNkXHVjNWI4MiIsInR5cGUiOjIsIm5vX3Nob3ciOjB9LCJuYmYiOjE2ODQwODExNjUsImV4cCI6MTY4NjY3MzE2NX0.VnYGnQHdZx8tcSC8UaKgurNBf5rbJTrgWzuy9FLTW-4",
        "User": {
          "id": 17011506,
          "name": "안창언2",
          "dept": 0,
          "phone": null,
          "email": "",
          "type": 2,
          "no_show": 0
        }
      }
    */
		userStore.value.token.access = data.access_token;
		userStore.value.token.refresh = data.refresh_token;
		userStore.value.info.id = data.User.id;
		userStore.value.info.name = data.User.name;
		userStore.value.info.email = data.User.email;
		userStore.value.info.type = data.User.type;
		userStore.value.info.dept = data.User.dept;
		userStore.value.info.noShow = data.User.no_show;
	},
	getToken: function () {
		return userStore.value.token;
	},
	getInfo: function () {
		return userStore.value.info;
	},
});

export const userTypeStr = computed(() => {
	if (userStore.value.info.type === USER_TYPE.ADMIN) {
		return '관리자';
	} else if (userStore.value.info.type === USER_TYPE.PROFESSOR) {
		return '교수';
	} else if (userStore.value.info.type === USER_TYPE.GRAD_STUDENT) {
		return '대학원생';
	} else if (userStore.value.info.type === USER_TYPE.UNDER_GRAD_STUDENT) {
		return '학부생';
	} else {
		console.error('사용자 유형이 올바르지 않습니다.');
		return '올바르지 않은 사용자 유형';
	}
});

export const userDeptStr = computed(() => {
	if (userStore.value.info.dept === DEPT_TYPE.COMPUTER) {
		return '컴퓨터공학과';
	} else if (userStore.value.info.dept === DEPT_TYPE.OTHERS) {
		return '기타 학과';
	} else {
		console.error('학과 유형이 올바르지 않습니다.');
		return '올바르지 않은 학과 유형';
	}
});

const template = {
	token: {
		access: '',
		refresh: '',
	},
	info: {
		id: -1,
		name: '',
		email: '',
		type: -1,
		dept: -1,
		noShow: -1,
	},
};
