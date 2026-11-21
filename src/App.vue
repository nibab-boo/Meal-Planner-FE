<template>
  <nav class="navbar">
    <span class="brand">🍽 Meal Planner</span>
    <RouterLink to="/">Dashboard</RouterLink>
    <RouterLink to="/recipes">Recipes</RouterLink>
    <RouterLink to="/plans">Plans</RouterLink>
  </nav>

  <RouterView />
</template>



<!-- CSS -->
<style scoped>
.navbar { display: flex; gap: 1.5rem; align-items: center; padding: 1rem 2rem; background: white; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
.brand { font-weight: 700; color: #16a34a; cursor:default }
.navbar a { color: #6b7280; text-decoration: none; font-size: 0.9rem; }
.navbar a.router-link-active { color: #16a34a; font-weight: 600; }
</style>