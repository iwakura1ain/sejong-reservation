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
