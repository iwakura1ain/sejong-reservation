import { createRouter, createWebHistory } from 'vue-router';

import MainView from '@/views/MainView.vue';
import NotFoundView from '@/views/NotFoundView.vue';

const routes = [
	{
		path: '/:pathMatch(.*)*',
		name: 'NotFound',
		component: NotFoundView,
	},
	{
		path: '/',
		name: 'Main',
		component: MainView,
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
