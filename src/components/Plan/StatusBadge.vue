<!-- A small coloured label: green for Active, grey for Archived. -->
<template>
  <span :class="['badge', badgeClass]">{{ status }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, required: true },
})

const badgeClass = computed(() =>
  props.status === 'Active' ? 'badge-active' : 'badge-archived'
)
</script>

<style scoped>
.badge { display: inline-block; padding: 0.1rem 0.6rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }
.badge-active { background: #e3efe8; color: #1f4f3a; }
.badge-archived { background: #ececec; color: #555; }
</style>