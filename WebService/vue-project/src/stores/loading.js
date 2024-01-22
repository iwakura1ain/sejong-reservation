// loading중인지 아닌지를 저장하는 store입니다.
// App.vue의 loading-overay컴포넌트의 props로 들어갑니다.
// --true : 로딩중 = loading-overay 표시
// --false : 로딩중 아님 = loading-overay 숨김

import { reactive } from 'vue';

export const loadingStore = reactive({
	data: false,
	start: function () {
		this.data = true;
	},
	stop: function () {
		this.data = false;
	},
});
