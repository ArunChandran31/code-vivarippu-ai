// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ReviewView from "../views/ReviewView.vue";
import AdminCost from "../pages/AdminCost/AdminCost.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/review", name: "review", component: ReviewView },
  { path: "/admin/cost", name: "admin-cost", component: AdminCost },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
