<!-- src/views/HomeView.vue -->
<template>
  <div class="page-overlay">
    <header class="topbar">
      <div class="left">
        <button class="menu-icon" aria-label="menu">☰</button>
        <div class="title">Code விவரிப்பு AI</div>
      </div>
      <div class="right">
        <div class="profile" title="Profile">👤</div>
      </div>
    </header>

    <main>
      <HomePrompt @analyze="handleAnalyze" />
    </main>

    <!-- footer moved inside CSS to stick to bottom by style.css -->
  </div>
</template>

<script>
import HomePrompt from "../components/HomePrompt.vue";
import { useReviewStore } from "../stores/useReviewStore";
import { useRouter } from "vue-router";

export default {
  name: "HomeView",
  components: { HomePrompt },
  setup() {
    const store = useReviewStore();
    const router = useRouter();

    async function handleAnalyze({ code, language }) {
      try {
        await store.postReview(code, language || null);
        // navigate to review page after successful store.save
        router.push({ name: "review" });
      } catch (err) {
        console.error("Analysis failed:", err);
        const msg = err?.response?.data?.detail || err?.message || "Network error";
        alert("Analysis failed. Server says: " + msg);
      }
    }

    return { handleAnalyze };
  },
};
</script>
