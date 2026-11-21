<!-- The RIGHT drawer: everything about ONE recipe.
     - plan usage (which plans use it, on which day, meal and servings)
     - add the recipe to a plan
     - remove the recipe from a plan
     It does not change any data itself. It sends events up to RecipesView. -->
<template>
  <div class="detail">
    <div class="detail-header">
      <h2>{{ recipe.title }}</h2>
      <div class="header-buttons">
        <button type="button" class="btn btn-small" @click="emit('edit')">Edit recipe</button>
        <button type="button" class="btn btn-small" @click="emit('close')">Close ✕</button>
      </div>
    </div>

    <!-- Quick facts -->
    <div class="facts">
      <span class="badge">{{ recipe.category }}</span>
      <span v-if="recipe.area">{{ recipe.area }} cuisine</span>
      <span>{{ recipe.prepTime }} min</span>
      <span>{{ recipe.calories }} kcal</span>
      <span>Serves {{ recipe.servings }}</span>
    </div>
    <p v-if="recipe.description" class="description">{{ recipe.description }}</p>

    <!-- 1. PLAN USAGE + REMOVE -->
    <section class="section">
      <h3>Used in these plans</h3>

      <p v-if="entries.length === 0" class="empty">This recipe is not in any plan yet.</p>

      <table v-else>
        <thead>
          <tr>
            <th>Plan</th>
            <th>Day</th>
            <th>Meal</th>
            <th class="num">Servings</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in entries" :key="e.id">
            <td>{{ e.planName }}</td>
            <td>{{ e.day }}</td>
            <td>{{ e.mealType }}</td>
            <td class="num">{{ e.servings }}</td>
            <td class="right">
              <button type="button" class="btn btn-small btn-danger" @click="emit('remove-entry', e)">Remove</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- 2. ADD TO A PLAN -->
    <section class="section">
      <h3>Add to a plan</h3>

      <p v-if="plans.length === 0" class="empty">No plans yet. Create a plan on the Plans page first.</p>

      <form v-else class="add-form" @submit.prevent="add">
        <div class="field wide">
          <label for="d-plan">Plan</label>
          <!-- the plan is CHOSEN from the existing plans, never typed -->
          <select id="d-plan" v-model.number="addForm.planId" required>
            <option value="" disabled>Select a plan</option>
            <option v-for="p in plans" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>

        <div class="field">
          <label for="d-day">Day</label>
          <select id="d-day" v-model="addForm.day">
            <option v-for="d in DAYS" :key="d" :value="d">{{ d }}</option>
          </select>
        </div>

        <div class="field">
          <label for="d-meal">Meal</label>
          <select id="d-meal" v-model="addForm.mealType">
            <option v-for="m in MEAL_TYPES" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>

        <div class="field">
          <label for="d-serv">Servings</label>
          <input id="d-serv" type="number" min="1" v-model.number="addForm.servings" required />
        </div>

        <div class="field button-field">
          <button class="btn btn-primary">Add to plan</button>
        </div>
      </form>

      <p v-if="error" class="error-text">⚠ {{ error }}</p>
    </section>

    <!-- 3. THE REST OF THE RECIPE -->
    <section class="section">
      <h3>Ingredients</h3>
      <p v-if="recipe.ingredients.length === 0" class="empty">No ingredients saved.</p>
      <ul v-else class="ingredients">
        <li v-for="(ing, index) in recipe.ingredients" :key="index">{{ ing.measure }} {{ ing.name }}</li>
      </ul>
    </section>

    <section class="section">
      <h3>Instructions</h3>
      <p class="instructions">{{ recipe.instructions || 'No instructions saved.' }}</p>
      <img v-if="recipe.imageUrl" :src="recipe.imageUrl" :alt="recipe.title" class="photo" />
    </section>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { DAYS, MEAL_TYPES } from '../../constants.js'

defineProps({
  recipe:  { type: Object, required: true },
  entries: { type: Array,  required: true },   // this recipe's plan entries (with planName)
  plans:   { type: Array,  required: true },   // all plans, for the dropdown
  error:   { type: String, default: '' },      // message to show, e.g. "already in this slot"
})
const emit = defineEmits(['close', 'edit', 'add-entry', 'remove-entry'])

// The little "add to plan" form
const addForm = reactive({ planId: '', day: 'Monday', mealType: 'Breakfast', servings: 1 })

function add() {
  emit('add-entry', { ...addForm })
}
</script>

<style scoped>
.detail { padding: 0 1.5rem 2rem; }

.detail-header {
  position: sticky; top: 0;            /* stays visible while the drawer scrolls */
  background: white; z-index: 1;
  display: flex; justify-content: space-between; align-items: center; gap: 1rem;
  padding: 1rem 0; border-bottom: 1px solid #e5e7eb; margin-bottom: 0.9rem;
}
h2 { font-size: 1.2rem; margin: 0; }
.header-buttons { display: flex; gap: 0.4rem; white-space: nowrap; }

.facts { display: flex; flex-wrap: wrap; gap: 0.4rem 1rem; align-items: center; color: #4b5563; font-size: 0.9rem; }
.badge { padding: 0.1rem 0.6rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; background: #e3efe8; color: #1f4f3a; }
.description { color: #4b5563; margin: 0.6rem 0 0; }

.section { margin-top: 1.5rem; }
h3 { font-size: 0.98rem; margin: 0 0 0.6rem; }

table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
th, td { text-align: left; padding: 0.5rem 0.4rem; border-bottom: 1px solid #f0f2f0; }
th { font-size: 0.78rem; color: #6b7280; }
.num { text-align: right; }
.right { text-align: right; }

.add-form { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.field { display: flex; flex-direction: column; gap: 0.25rem; }
.wide { grid-column: 1 / -1; }
.button-field { justify-content: flex-end; }
label { font-size: 0.82rem; font-weight: 600; color: #6b7280; }
input, select {
  font: inherit; padding: 0.45rem 0.6rem; width: 100%; box-sizing: border-box;
  border: 1px solid #d1d5db; border-radius: 6px; background: white;
}

.error-text { color: #b3261e; font-size: 0.88rem; margin: 0.6rem 0 0; }
.empty { color: #9ca3af; font-style: italic; margin: 0; }

.ingredients { margin: 0; padding-left: 1.2rem; columns: 2; }
.instructions { white-space: pre-line; margin: 0 0 0.9rem; }
.photo { max-width: 100%; border-radius: 8px; display: block; }
</style>