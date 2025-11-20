<!-- src/components/CustomSelect.vue -->
<template>
  <div class="custom-select" ref="root">
    <button
      class="cs-toggle"
      :aria-expanded="open ? 'true' : 'false'"
      @click="toggle"
      @keydown.enter.prevent="toggle"
      @blur="onBlur"
      type="button"
    >
      <span class="cs-label">{{ selectedLabel }}</span>
      <span class="cs-caret">▾</span>
    </button>

    <transition name="fade-slide">
      <ul v-if="open" class="cs-menu" role="listbox" :aria-activedescendant="activeId">
        <li
          v-for="(opt, idx) in options"
          :key="opt"
          class="cs-item"
          :class="{ 'is-active': opt === value }"
          role="option"
          @click="select(opt)"
        >
          {{ optLabel(opt) }}
        </li>
      </ul>
    </transition>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";

export default {
  name: "CustomSelect",
  props: {
    modelValue: { type: [String, null], default: "auto" },
    options: { type: Array, default: () => ["python", "javascript", "java", "c++", "c#", "go", "ruby", "php", "swift", "kotlin"] },
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const open = ref(false);
    const value = ref(props.modelValue || "auto");
    const root = ref(null);

    function toggle() { open.value = !open.value; }
    function close() { open.value = false; }
    function select(v) { value.value = v; emit("update:modelValue", v); close(); }
    function onBlur(e) {
      // small delay to allow click to register
      setTimeout(() => { close(); }, 120);
    }

    const selectedLabel = computed(() => {
      if (!value.value || value.value === "auto") return "Auto-detect";
      return value.value;
    });

    function optLabel(opt) {
      return opt === "auto" ? "Auto-detect" : opt;
    }

    // close on outside click
    onMounted(() => {
      document.addEventListener("click", (ev) => {
        if (!root.value) return;
        if (!root.value.contains(ev.target)) close();
      });
    });

    return { open, toggle, select, value, selectedLabel, root, optLabel };
  },
};
</script>

<style scoped>
.custom-select { position: relative; display:inline-block; }
.cs-toggle {
  display:flex; align-items:center; gap:10px; padding:10px 18px; border-radius:20px;
  background: white; color:#111; font-size:14px; box-shadow:0 10px 24px rgba(0,0,0,0.18);
  border:none; cursor:pointer;
}
.cs-caret { opacity:0.8; }
.cs-menu {
  position:absolute; left:0; bottom: calc(100% + 10px);
  background: white; min-width:160px; border-radius:8px; box-shadow:0 12px 40px rgba(0,0,0,0.18);
  list-style:none; margin:0; padding:6px 0; max-height:280px; overflow:auto; z-index:80;
}
.cs-item { padding:8px 14px; cursor:pointer; }
.cs-item:hover { background:#f2f2f2; }
.cs-item.is-active { background:#e6f0ff; font-weight:600; }
.fade-slide-enter-active, .fade-slide-leave-active { transition: all .18s ease; }
.fade-slide-enter-from { transform: translateY(8px); opacity: 0; }
.fade-slide-enter-to { transform: translateY(0); opacity:1; }
.fade-slide-leave-from { transform: translateY(0); opacity:1; }
.fade-slide-leave-to { transform: translateY(8px); opacity:0; }
</style>
