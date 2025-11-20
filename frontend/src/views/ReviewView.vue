<!-- src/views/ReviewView.vue -->
<template>
  <div class="page-overlay">
    <header class="topbar">
      <div class="left">
        <button class="menu-icon" @click="$router.push('/')" aria-label="back">←</button>
        <div class="title">Review</div>
      </div>
      <div class="right"><div class="profile">👤</div></div>
    </header>

    <section class="review-wrapper">
      <div v-if="lastReview && lastReview.ai">
        <h3>Static Analysis</h3>
        <pre class="report-pre">{{ pretty(lastReview.static) }}</pre>

        <h3>AI Response</h3>
        <pre class="report-pre">{{ pretty(lastReview.ai) }}</pre>

        <h3>Usage</h3>
        <pre class="report-pre">{{ pretty(lastReview.usage) }}</pre>
      </div>
      <div v-else>
        <p>No review found. Run an analysis from the Home page.</p>
      </div>
    </section>

    <footer class="footer-text">creviro.io  |  @arunchandran</footer>
  </div>
</template>

<script>
import { useReviewStore } from "../stores/useReviewStore";
import { computed } from "vue";

export default {
  name: "ReviewView",
  setup() {
    const store = useReviewStore();
    const lastReview = computed(() => store.lastReview.value || null);

    function pretty(obj) {
      try { return JSON.stringify(obj, null, 2); } catch { return String(obj); }
    }
    return { lastReview, pretty };
  },
};
</script>

<style scoped>
.report-pre { white-space: pre-wrap; font-family: ui-monospace, "Roboto Mono", monospace; background:#f7f7f7; padding:12px; border-radius:8px; color:#111; }
</style>
