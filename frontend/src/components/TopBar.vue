<!-- frontend/src/components/TopBar.vue -->
<template>
  <header class="topbar">
    <div class="topbar-inner px-6">
      <div class="left flex items-center gap-3">
        <button aria-label="menu" class="menu-button">
          <!-- menu icon -->
          <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none">
            <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>

        <div class="title">Code விவரிப்பு AI</div>
      </div>

      <div class="right">
        <button aria-label="profile" class="profile">
          <svg class="w-5 h-5 text-white/90" viewBox="0 0 24 24" fill="none">
            <path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8z" stroke="currentColor" stroke-width="1.4"/>
            <path d="M4 20c0-3.314 3.582-6 8-6s8 2.686 8 6" stroke="currentColor" stroke-width="1.2"/>
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: "TopBar"
}
</script>

<style scoped>
.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 72px;
  z-index: 80;
  display: flex;
  align-items: center;
  background: transparent;
}

/* inner container stretches full width but keeps padding */
.topbar-inner {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-height: 72px;
}

/* left side */
.left { display: flex; align-items: center; gap: 14px; }

/* menu button */
.menu-button {
  background: transparent;
  border: none;
  padding: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* title on the left - make it larger and left-aligned */
.title {
  color: #fff;
  font-size: 22px;
  font-weight: 400;
  letter-spacing: 0.2px;
  font-family: "Google Sans Flex", sans-serif;
}

/* profile on right */
.right { display: flex; align-items: center; gap: 8px; }
.profile {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.35);
  display:flex; align-items:center; justify-content:center;
  background: transparent;
}
</style>
