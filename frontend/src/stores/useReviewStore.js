// src/stores/useReviewStore.js
import axios from "axios";
import { ref } from "vue";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const lastReview = ref(null);
const loading = ref(false);

async function postReview(code, language = null) {
  loading.value = true;
  try {
    const payload = { code, language };
    const res = await axios.post(`${API_BASE}/api/review`, payload, {
      headers: { "Content-Type": "application/json" },
    });
    // backend returns { static, ai, usage } - store whole doc
    lastReview.value = res.data;
    return res.data;
  } catch (err) {
    // bubble up error
    throw err;
  } finally {
    loading.value = false;
  }
}

function getLastReview() {
  return lastReview;
}

function isLoading() {
  return loading;
}

export function useReviewStore() {
  return {
    postReview,
    lastReview,
    getLastReview,
    loading,
    isLoading,
  };
}
