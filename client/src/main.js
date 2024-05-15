import { createApp } from "vue";
import App from "./App.vue";
import Vue from "vue";
import { RouterLink } from "vue-router";
import Auth from "./components/Auth.vue";

// createApp(App).mount("#app");

Vue.use(RouterLink);

const routes = [
  { path: "/auth", component: Auth },
  // Define other routes as needed
];

const router = new RouterLink({
  mode: "history",
  routes,
});

new Vue({
  router,
}).$mount("#app");
