import axios from 'axios';
import { createApp } from 'vue';
import App from './App.vue';
import router from '@/router.js';

// import './assets/global.scss';

async function init() {
	try {
		const jsonipRes = await axios.get('https://jsonip.com');
		const serviceIP = jsonipRes.data.ip;
		localStorage.setItem('SEJONG_RESERVATION_SERVICE_IP', serviceIP);

		const app = createApp(App);
		app.use(router);
		app.mount('#app');
	} catch (err) {}
}

init();
