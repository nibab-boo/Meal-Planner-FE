<template>
  <div class="dashboard">
    <h1>Dashboard</h1>

    <p v-if="loading" class="state">Loading dashboard...</p>
    <p v-else-if="error" class="state error">⚠ {{ error }}</p>

    <div v-else>
      <!-- Required: four summary cards -->
      <div class="stat-row">
        <StatCard label="Recipes"       :value="stats.totalRecipes" />
        <StatCard label="Plans"         :value="stats.totalPlans" />
        <StatCard label="Planned meals" :value="stats.totalEntries" />
        <StatCard label="Active plans"  :value="stats.activePlans" highlight />
      </div>

      <!-- Required: recent recipes -->
      <RecentRecipes :recipes="stats.recentRecipes" />

      <!-- Our two extra components -->
      <div class="panel-row">
        <BarPanel
          title="Most-used recipes"
          :items="mostUsedItems"
          empty-text="No recipe has been added to a plan yet."
        />
        <BarPanel
          title="Recipes by category"
          :items="categoryItems"
          empty-text="No recipes yet."
        />
      </div>
    </div>
  </div>
</template>

<!-- -------------------------------------------------------------------------- -->

<!-- JS -->
<script setup>
    import { ref, computed } from 'vue'
    import { API } from '../constants.js'
    import { useFetch } from '../composables/useFetch.js'

    // Components
    import StatCard from '../components/Dashboard/StatCard.vue'
    import RecentRecipes from '../components/Dashboard/RecentRecipes.vue'
    import BarPanel from '../components/Dashboard/BarPanel.vue'


    // ── LIVE DATA from GET /stats ───────────────────────────
    const { data: stats, loading, error } = useFetch(`${API}/stats`)

    // Reshape the data into the { label, value } list that BarPanel expects.
    // "?? []" = use an empty list while stats is still null (before it arrives)
    const mostUsedItems = computed(() =>
        (stats.value?.mostUsed ?? []).map(r => ({ label: r.title, value: r.count }))
    )
    const categoryItems = computed(() =>
        (stats.value?.categoryBreakdown ?? []).map(c => ({ label: c.category, value: c.count }))
    )


    // // ── PLACEHOLDER DATA ─────────────────────────────────────
    // // Same shape the API will return later, so only this block changes.
    // const stats = ref({
    // totalRecipes: 12,
    // totalPlans: 4,
    // totalEntries: 23,
    // activePlans: 3,
    // recentRecipes: [
    //     { id: 12, title: 'Apple Frangipan Tart',      category: 'Dessert',    prepTime: 60, calories: 390 },
    //     { id: 11, title: 'Overnight Oats',            category: 'Breakfast',  prepTime: 5,  calories: 340 },
    //     { id: 10, title: 'Grilled Salmon with Greens', category: 'Seafood',   prepTime: 20, calories: 430 },
    //     { id: 9,  title: 'Spicy Arrabiata Penne',     category: 'Vegetarian', prepTime: 25, calories: 520 },
    // ],
    // mostUsed: [
    //     { id: 10, title: 'Grilled Salmon with Greens', count: 5 },
    //     { id: 11, title: 'Overnight Oats',             count: 4 },
    //     { id: 9,  title: 'Spicy Arrabiata Penne',      count: 2 },
    // ],
    // categoryBreakdown: [
    //     { category: 'Seafood',    count: 4 },
    //     { category: 'Dessert',    count: 3 },
    //     { category: 'Breakfast',  count: 3 },
    //     { category: 'Vegetarian', count: 2 },
    // ],
    // })

    // // ── LOADING STATE ───────────────────────────────────────
    // const loading = ref(false)
    // const error   = ref(null)

    // // Reshape the data into the { label, value } list that BarPanel expects
    // const mostUsedItems = computed(() =>
    // stats.value.mostUsed.map(r => ({ label: r.title, value: r.count }))
    // )
    // const categoryItems = computed(() =>
    // stats.value.categoryBreakdown.map(c => ({ label: c.category, value: c.count }))
    // )
</script>



<!-- CSS -->
<style scoped>
.dashboard { max-width: 1000px; margin: 0 auto; padding: 1.75rem 1.25rem 3rem; }
h1 { font-size: 1.6rem; margin: 0 0 1.25rem; }
.stat-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; margin-bottom: 1.25rem; }
.panel-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem; }
.state { color: #9ca3af; }
.error { color: #dc2626; }
</style>