<!-- src/components/HomePrompt.vue -->
<template>
  <section class="home-outer">
    <h1 class="home-title">Let's Summarize.</h1>

    <div class="prompt-wrapper">
      <textarea
        v-model="code"
        :placeholder="placeholder"
        class="prompt-textarea"
        @keydown.enter.exact.prevent
      ></textarea>

      <!-- footer row inside prompt: left custom select, right submit arrow -->
      <div class="prompt-footer-row">
        <div class="left-controls">
          <CustomSelect v-model="language" :options="allOptions" />
        </div>

        <button
          class="submit-arrow"
          :disabled="loading"
          @click="onClickAnalyze"
          aria-label="Analyze"
        >
          <span class="arrow-symbol">➜</span>
          <span v-if="loading" class="spinner" aria-hidden="true"></span>
        </button>
      </div>
    </div>

    <footer class="page-footer">creviro.io  |  @arunchandran</footer>
  </section>
</template>

<script>
import { ref } from "vue";
import CustomSelect from "./CustomSelect.vue";

export default {
  name: "HomePrompt",
  components: { CustomSelect },
  emits: ["analyze"],
  setup(_, { emit }) {
    const code = ref("");
    const language = ref("auto");
    const loading = ref(false);

    const allOptions = ["auto","python","javascript","java","c++","c#","go","ruby","php","swift","kotlin"];

    const placeholder = "Provide your code here.";

    async function onClickAnalyze() {
      if (!code.value || !code.value.trim()) {
        alert("Please paste or type your code before analyzing.");
        return;
      }
      loading.value = true;
      try {
        await emit("analyze", { code: code.value, language: language.value === "auto" ? null : language.value });
      } catch (err) {
        console.error(err);
        alert("Analysis failed. Check console for details.");
      } finally {
        loading.value = false;
      }
    }

    return { code, language, allOptions, onClickAnalyze, placeholder, loading };
  },
};
</script>

<style scoped>
.home-outer { display:flex; flex-direction:column; align-items:center; padding-top:72px; gap:18px; }

.home-title {
  font-size:40px; font-weight:400; color:var(--title-color, #fff);
  text-align:center; margin: 6px 0 10px;
  text-shadow: 0 6px 18px rgba(0,0,0,0.55);
}

/* Prompt card */
.prompt-wrapper {
  width: 78%;
  max-width: 1120px;
  background: rgba(255,255,255,0.98);
  border-radius: 28px;
  padding: 30px 28px 60px 28px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.35);
  position: relative;
}

/* text area */
.prompt-textarea {
  width:100%;
  min-height: 260px;
  border: none;
  outline: none;
  resize: none;
  font-family: "Google Sans Flex", "Open Sans", Arial, sans-serif;
  font-size: 15px;
  color: #111;
  background: transparent;
}

/* footer row inside prompt */
.prompt-footer-row {
  position: absolute;
  left: 28px;
  right: 28px;
  bottom: 18px;
  display:flex;
  justify-content: space-between;
  align-items: center;
  pointer-events: none; /* allow children to control pointer */
}
.left-controls { pointer-events: auto; }

/* submit arrow (flat arrow button) */
.submit-arrow {
  pointer-events: auto;
  border: none;
  background: transparent;
  font-size: 26px;
  color: #222;
  cursor: pointer;
  padding: 10px 16px;
  border-radius: 8px;
  transition: transform .12s ease, color .12s ease;
}
.submit-arrow:hover { transform: translateY(-2px); color: #000; }
.submit-arrow:disabled { opacity: 0.5; cursor: not-allowed; }

/* small spinner (when loading) */
.spinner {
  display:inline-block;
  width:12px; height:12px; margin-left:8px;
  border-radius:50%;
  border:2px solid rgba(0,0,0,0.08);
  border-top-color: rgba(0,0,0,0.45);
  animation: spin .9s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* page footer */
.page-footer {
  margin-top: 18px;
  color: #e6e6e6;
  font-size:14px;
  text-align:center;
}

/* responsive */
@media (max-width: 900px){
  .prompt-wrapper { width:94%; padding: 18px; border-radius:18px; }
  .home-title { font-size:32px; }
}
</style>
