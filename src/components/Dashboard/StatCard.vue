<template>
  <div :class="['stat-card', highlight ? 'stat-card--highlight' : '']">
    <div class="value">{{ value }}</div>
    <div class="label">{{ label }}</div>
  </div>
</template>

<script setup>
defineProps({
  label:     { type: String,  required: true },
  value:     { type: Number,  required: true },
  highlight: { type: Boolean, default: false },
})
</script>

<style scoped>
.stat-card {
  background: white;
  border-radius: 8px;
  border-left: 5px solid #2c6a4d;
  padding: 0.9rem 1.1rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
}
.stat-card--highlight { border-left-color: #e2b13c; }
.value { font-size: 2rem; font-weight: 700; line-height: 1.1; }
.label { color: #6b7280; font-size: 0.85rem; margin-top: 0.15rem; }
</style>