<!-- The form inside the RIGHT drawer: put ONE recipe into ONE cell of the grid.
     entry = null   → ADD: choose a recipe, day, meal and servings
     entry = {...}  → EDIT: the recipe stays the same, change day, meal or servings -->
<template>
  <form class="form" @submit.prevent="save">
    <div class="form-header">
      <h2>{{ entry ? 'Edit entry' : 'Add a recipe' }}</h2>
      <button type="button" class="btn btn-small" @click="emit('close')">Close ✕</button>
    </div>

    <div class="fields">
      <!-- EDIT: the recipe is fixed and only shown -->
      <div v-if="entry" class="field wide">
        <div class="label">Recipe</div>
        <p class="recipe-name">{{ entry.recipeTitle }}</p>
      </div>

      <!-- ADD: the recipe is CHOSEN from the existing recipes, never typed -->
      <div v-else class="field wide">
        <label for="e-recipe">Recipe</label>
        <p v-if="recipes.length === 0" class="empty">No recipes yet. Add some on the Recipes page first.</p>
        <select v-else id="e-recipe" v-model.number="form.recipeId" required>
          <option value="" disabled>Select a recipe</option>
          <option v-for="r in recipes" :key="r.id" :value="r.id">{{ r.title }}</option>
        </select>
      </div>

      <div class="field">
        <label for="e-day">Day</label>
        <select id="e-day" v-model="form.day">
          <option v-for="d in DAYS" :key="d" :value="d">{{ d }}</option>
        </select>
      </div>

      <div class="field">
        <label for="e-meal">Meal</label>
        <select id="e-meal" v-model="form.mealType">
          <option v-for="m in MEAL_TYPES" :key="m" :value="m">{{ m }}</option>
        </select>
      </div>

      <div class="field">
        <label for="e-serv">Servings</label>
        <input id="e-serv" type="number" min="1" v-model.number="form.servings" required />
      </div>
    </div>

    <p v-if="error" class="error-text">⚠ {{ error }}</p>

    <div class="form-footer">
      <button class="btn btn-primary" :disabled="!entry && recipes.length === 0">Save</button>
      <button type="button" class="btn" @click="emit('close')">Cancel</button>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { DAYS, MEAL_TYPES } from '../../constants.js'

const props = defineProps({
  entry:       { type: Object, default: null },        // null = adding
  recipes:     { type: Array,  required: true },       // all recipes, for the dropdown
  initialDay:  { type: String, default: 'Monday' },    // the cell that was clicked
  initialMeal: { type: String, default: 'Breakfast' },
  error:       { type: String, default: '' },          // e.g. "already in this slot"
})
const emit = defineEmits(['save', 'close'])

// Editing starts with the entry's values. Adding starts with the clicked cell.
const form = reactive({
  recipeId: props.entry ? props.entry.recipeId : '',
  day:      props.entry ? props.entry.day      : props.initialDay,
  mealType: props.entry ? props.entry.mealType : props.initialMeal,
  servings: props.entry ? props.entry.servings : 1,
})

function save() {
  emit('save', { ...form })
}
</script>

<style scoped>
.form { padding: 0 1.5rem; }

.form-header {
  position: sticky; top: 0;
  background: white; z-index: 1;
  display: flex; justify-content: space-between; align-items: center;
  padding: 1rem 0; border-bottom: 1px solid #e5e7eb; margin-bottom: 1rem;
}
h2 { font-size: 1.2rem; margin: 0; }

.fields { display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; }
.field { display: flex; flex-direction: column; gap: 0.25rem; }
.wide { grid-column: 1 / -1; }

label, .label { font-size: 0.82rem; font-weight: 600; color: #6b7280; }
input, select {
  font: inherit; padding: 0.45rem 0.6rem; width: 100%; box-sizing: border-box;
  border: 1px solid #d1d5db; border-radius: 6px; background: white;
}
.recipe-name { margin: 0; font-weight: 700; }
.empty { color: #9ca3af; font-style: italic; margin: 0; }
.error-text { color: #b3261e; font-size: 0.88rem; margin: 0.9rem 0 0; }

.form-footer {
  position: sticky; bottom: 0;
  background: white; border-top: 1px solid #e5e7eb;
  display: flex; gap: 0.5rem; padding: 0.9rem 0; margin-top: 1.2rem;
}
</style>