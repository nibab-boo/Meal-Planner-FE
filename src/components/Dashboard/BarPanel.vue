<!-- A titled list of horizontal bars. items = [{ label: 'Seafood', value: 4 }, ...] -->
<template>
  <section class="panel">
    <h2>{{ title }}</h2>

    <p v-if="items.length === 0" class="empty">{{ emptyText }}</p>

    <ul v-else class="bars">
      <li v-for="item in items" :key="item.label">
        <div class="row">
          <span>{{ item.label }}</span>
          <strong>{{ item.value }}</strong>
        </div>
        <div class="track">
          <div class="fill" :style="{ width: (item.value / max) * 100 + '%' }"></div>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup>
    import { computed } from 'vue'

    const props = defineProps({
    title:     { type: String, required: true },
    items:     { type: Array,  required: true },
    emptyText: { type: String, default: 'Nothing to show yet.' },
    })

    // The biggest value gets a full-width bar; the others are a fraction of it
    const max = computed(() => Math.max(1, ...props.items.map(i => i.value)))
</script>

<style scoped>
.panel { background: white; border-radius: 8px; padding: 1.1rem 1.25rem; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07); }
h2 { font-size: 1.05rem; margin: 0 0 0.75rem; }
.bars { list-style: none; padding: 0; margin: 0; }
.bars li { margin-bottom: 0.7rem; }
.row { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.2rem; }
.track { background: #e3efe8; border-radius: 4px; height: 10px; }
.fill { background: #2c6a4d; height: 100%; border-radius: 4px; }
.empty { color: #9ca3af; font-style: italic; }
</style>