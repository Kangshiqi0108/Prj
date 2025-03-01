import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';

// Define routes
const routes = [
  { path: '/', component: () => import('./components/Home.vue') },
  { path: '/about', component: () => import('./components/About.vue') }
];

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes
});

// Create and mount app
createApp(App).use(router).mount('#app');