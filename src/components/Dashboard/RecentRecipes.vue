<template>
  <section class="panel">
    <h2>Recent recipes</h2>

    <p v-if="recipes.length === 0" class="empty">No recipes yet. Add one on the Recipes page.</p>

    <ul v-else class="list">
      <li v-for="r in recipes" :key="r.id" class="item">
        <div>
          <!-- Later this becomes <RouterLink :to="`/recipes/${r.id}`"> once that route exists -->
          <strong>{{ r.title }}</strong>
          <span class="badge">{{ r.category }}</span>
        </div>
        <div class="details">
          <span>{{ r.prepTime }} min</span>
          <span>{{ r.calories }} kcal</span>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup>
defineProps({
  recipes: { type: Array, required: true },
})
</script>

<style scoped>
.panel { background: white; border-radius: 8px; padding: 1.1rem 1.25rem; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07); margin-bottom: 1.25rem; }
h2 { font-size: 1.05rem; margin: 0 0 0.75rem; }
.list { list-style: none; padding: 0; margin: 0; }
.item { display: flex; justify-content: space-between; gap: 1rem; padding: 0.6rem 0; border-bottom: 1px solid #f0f2f0; }
.item:last-child { border-bottom: none; }
.badge { margin-left: 0.5rem; padding: 0.1rem 0.6rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; background: #e3efe8; color: #1f4f3a; }
.details { display: flex; gap: 1rem; color: #6b7280; font-size: 0.85rem; white-space: nowrap; }
.empty { color: #9ca3af; font-style: italic; }
</style>