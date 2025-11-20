<template>
  <div class="p-6">
    <h2 class="text-2xl font-semibold mb-4">Admin — Usage & Cost</h2>

    <div v-if="loading" class="p-4">Loading usage...</div>

    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">

      <div class="p-4 rounded-xl shadow bg-white">
        <h3 class="font-bold text-lg mb-2">Total Reviews</h3>
        <p class="text-3xl">{{ usage.total_reviews }}</p>
      </div>

      <div class="p-4 rounded-xl shadow bg-white">
        <h3 class="font-bold text-lg mb-2">Total Tokens Used</h3>
        <p class="text-3xl">{{ usage.total_tokens }}</p>
      </div>

      <div class="p-4 rounded-xl shadow bg-white">
        <h3 class="font-bold text-lg mb-2">Approx Cost (₹)</h3>
        <p class="text-3xl">{{ usage.cost_inr.toFixed(2) }}</p>
      </div>

    </div>

    <div class="mt-8" v-if="usage">
      <h3 class="font-bold text-xl mb-2">Last Updated</h3>
      <p>{{ usage.last_updated }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const loading = ref(true);
const usage = ref({
  total_reviews: 0,
  total_tokens: 0,
  cost_inr: 0,
  last_updated: "—"
});

onMounted(async () => {
  try {
    const res = await fetch("http://localhost:5000/api/usage");
    const data = await res.json();
    usage.value = data;
  } catch (err) {
    console.error("Failed to fetch usage:", err);
  } finally {
    loading.value = false;
  }
});
</script>
