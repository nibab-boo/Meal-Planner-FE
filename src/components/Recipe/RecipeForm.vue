<!-- The form inside the LEFT drawer. Used for BOTH adding and editing.
     recipe = null   → "New recipe" (empty form)
     recipe = {...}  → "Edit recipe" (form starts filled in)

     It also has the TheMealDB parts:
       - category dropdown filled from TheMealDB
       - import helper: category → meals in that category → form pre-fills -->
<template>
  <form class="form" @submit.prevent="save">
    <div class="form-header">
      <h2>{{ recipe ? 'Edit recipe' : 'New recipe' }}</h2>
      <button type="button" class="btn btn-small" @click="emit('close')">Close ✕</button>
    </div>

    <!-- ── IMPORT HELPER ─────────────────────────────── -->
    <div class="import-box">
      <strong>Import from TheMealDB (optional)</strong>

      <p v-if="categoriesLoading" class="hint">Loading categories...</p>
      <div v-else-if="categoriesError" class="error-row">
        <span>⚠ Could not load categories: {{ categoriesError }}</span>
        <button type="button" class="btn btn-small" @click="loadCategories">Retry</button>
      </div>

      <div v-else class="import-fields">
        <div class="field">
          <label for="imp-category">1. Category</label>
          <select id="imp-category" v-model="importCategory">
            <option value="">Select a category</option>
            <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>

        <div class="field">
          <label for="imp-meal">2. Meal</label>
          <select id="imp-meal" v-model="importMealId" :disabled="importCategory === '' || mealsLoading">
            <option value="">{{ mealsLoading ? 'Loading meals...' : 'Select a meal' }}</option>
            <option v-for="m in meals" :key="m.idMeal" :value="m.idMeal">{{ m.strMeal }}</option>
          </select>
        </div>
      </div>

      <p v-if="mealsError" class="error-text">⚠ {{ mealsError }}</p>
      <p v-if="importLoading" class="hint">Loading recipe details...</p>
      <p v-if="importError" class="error-text">⚠ {{ importError }}</p>
      <p v-if="importDone" class="hint">Form filled in. Add prep time, calories and servings, and change anything you like.</p>
    </div>

    <!-- ── THE RECIPE FIELDS ─────────────────────────── -->
    <div class="fields">
      <div class="field wide">
        <label for="r-title">Title</label>
        <input id="r-title" v-model="form.title" required />
      </div>

      <div class="field wide">
        <label for="r-desc">Description</label>
        <input id="r-desc" v-model="form.description" />
      </div>

      <div class="field">
        <label for="r-category">Category</label>
        <select id="r-category" v-model="form.category" required>
          <option value="" disabled>{{ categoriesLoading ? 'Loading...' : 'Select a category' }}</option>
          <!-- keeps the saved category visible even before the list has loaded -->
          <option v-if="form.category && !categories.includes(form.category)" :value="form.category">{{ form.category }}</option>
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>

      <div class="field">
        <label for="r-area">Area (cuisine)</label>
        <input id="r-area" v-model="form.area" />
      </div>

      <div class="field">
        <label for="r-prep">Prep time (minutes)</label>
        <input id="r-prep" type="number" min="0" v-model.number="form.prepTime" required />
      </div>

      <div class="field">
        <label for="r-cal">Calories per serving</label>
        <input id="r-cal" type="number" min="0" v-model.number="form.calories" required />
      </div>

      <div class="field">
        <label for="r-serv">Default servings</label>
        <input id="r-serv" type="number" min="1" v-model.number="form.servings" required />
      </div>

      <div class="field">
        <label for="r-img">Image URL (optional)</label>
        <input id="r-img" v-model="form.imageUrl" />
      </div>

      <!-- Ingredients: a list the user can add to and remove from -->
      <div class="field wide">
        <div class="label">Ingredients</div>
        <div v-for="(ing, index) in form.ingredients" :key="index" class="ingredient-row">
          <input v-model="ing.name" placeholder="Name (e.g. Flour)" />
          <input v-model="ing.measure" placeholder="Measure (e.g. 2 cups)" />
          <button type="button" class="btn btn-small btn-danger" @click="removeIngredient(index)">Remove</button>
        </div>
        <div>
          <button type="button" class="btn btn-small" @click="addIngredient">+ Add ingredient</button>
        </div>
      </div>

      <div class="field wide">
        <label for="r-instr">Instructions</label>
        <textarea id="r-instr" v-model="form.instructions"></textarea>
      </div>
    </div>
        <p v-if="error" class="error-text">⚠ {{ error }}</p>
    <div class="form-footer">
      <button class="btn btn-primary">Save recipe</button>
      <button type="button" class="btn" @click="emit('close')">Cancel</button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'

const props = defineProps({
  recipe: { type: Object, default: null },
  error: {type: String,default: ''},
})
const emit = defineEmits(['save', 'close'])

// ── THE RECIPE BEING ADDED / EDITED ──────────────────────
function emptyRecipe() {
  return {
    title: '', description: '', category: '', area: '',
    prepTime: 30, calories: 500, servings: 2,
    ingredients: [{ name: '', measure: '' }],
    instructions: '', imageUrl: '',
  }
}

// Editing? Make a COPY, so typing in the form does not change the list
// behind it until the user presses Save.
const form = reactive(props.recipe ? JSON.parse(JSON.stringify(props.recipe)) : emptyRecipe())

function addIngredient() {
  form.ingredients.push({ name: '', measure: '' })
}

function removeIngredient(index) {
  form.ingredients.splice(index, 1)
}

function save() {
  // Ignore ingredient rows the user left empty
  const cleanIngredients = form.ingredients.filter(i => i.name.trim() !== '')
  emit('save', { ...form, ingredients: cleanIngredients })
}

// ── THEMEALDB ────────────────────────────────────────────
// Three calls, one after another:
//   1. categories  (when the form opens)
//   2. meals in the chosen category  (when a category is picked)
//   3. full details of the chosen meal  (when a meal is picked) → fills the form
const MEALDB = 'https://www.themealdb.com/api/json/v1/1'

// Call 1: categories. Fills BOTH category dropdowns.
const categories        = ref([])
const categoriesLoading = ref(true)
const categoriesError   = ref(null)

async function loadCategories() {
  categoriesLoading.value = true
  categoriesError.value = null
  try {
    const res = await fetch(`${MEALDB}/categories.php`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()

    
    categories.value = (data.categories ?? []).map(c => c.strCategory)
  } catch (e) {
    categoriesError.value = e.message
  } finally {
    categoriesLoading.value = false
  }
}
onMounted(loadCategories)

// Call 2: meals in a category. Runs whenever importCategory changes.
const importCategory = ref('')
const meals          = ref([])
const mealsLoading   = ref(false)
const mealsError     = ref(null)
const importMealId   = ref('')

watch(importCategory, async (category) => {
  meals.value = []              // clear the old list
  importMealId.value = ''
  mealsError.value = null
  if (category === '') return   // user went back to "Select a category"

  mealsLoading.value = true
  try {
    const res = await fetch(`${MEALDB}/filter.php?c=${category}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    meals.value = data.meals ?? []              // TheMealDB sends null when nothing matches
    if (meals.value.length === 0) mealsError.value = 'No meals found in this category.'
  } catch (e) {
    mealsError.value = e.message
  } finally {
    mealsLoading.value = false
  }
})

// Call 3: full details of one meal. Runs whenever importMealId changes.
const importLoading = ref(false)
const importError   = ref(null)
const importDone    = ref(false)

watch(importMealId, async (id) => {
  importError.value = null
  importDone.value = false
  if (id === '') return

  importLoading.value = true
  try {
    const res = await fetch(`${MEALDB}/lookup.php?i=${id}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()

    
    const meal = data.meals ? data.meals[0] : null   // "meals" is a list with ONE item
    if (!meal) throw new Error('Meal not found')

    // TheMealDB sends ingredients as 20 numbered fields, many of them empty.
    // Turn them into one clean list and skip the blanks.
    const ingredients = []
    for (let i = 1; i <= 20; i++) {
      const name    = (meal[`strIngredient${i}`] || '').trim()
      const measure = (meal[`strMeasure${i}`] || '').trim()
      if (name !== '') ingredients.push({ name, measure })
    }

    // Pre-fill the form. TheMealDB has no prepTime, calories or servings,
    // so those keep their values and the user fills them in.
    form.title        = meal.strMeal
    form.category     = meal.strCategory
    form.area         = meal.strArea
    form.instructions = meal.strInstructions
    form.imageUrl     = meal.strMealThumb
    form.ingredients  = ingredients.length > 0 ? ingredients : [{ name: '', measure: '' }]
    importDone.value = true
  } catch (e) {
    importError.value = e.message
  } finally {
    importLoading.value = false
  }
})
</script>

<style scoped>
.form { padding: 0 1.5rem; }

.form-header {
  position: sticky; top: 0;            /* stays visible while the form scrolls */
  background: white; z-index: 1;
  display: flex; justify-content: space-between; align-items: center;
  padding: 1rem 0; border-bottom: 1px solid #e5e7eb; margin-bottom: 1rem;
}
h2 { font-size: 1.2rem; margin: 0; }

.import-box { background: #e3efe8; border-radius: 8px; padding: 0.9rem 1rem; margin-bottom: 1.1rem; }
.import-fields { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 0.6rem; }
.hint { color: #4b5563; font-size: 0.85rem; margin: 0.5rem 0 0; }
.error-text { color: #b3261e; font-size: 0.85rem; margin: 0.5rem 0 0; }
.error-row { display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; color: #b3261e; font-size: 0.85rem; margin-top: 0.5rem; }

.fields { display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; }
.field { display: flex; flex-direction: column; gap: 0.25rem; }
.wide { grid-column: 1 / -1; }          /* spans both columns */

label, .label { font-size: 0.82rem; font-weight: 600; color: #6b7280; }
input, select, textarea {
  font: inherit; padding: 0.45rem 0.6rem; width: 100%; box-sizing: border-box;
  border: 1px solid #d1d5db; border-radius: 6px; background: white;
}
textarea { min-height: 110px; resize: vertical; }

.ingredient-row { display: grid; grid-template-columns: 2fr 1fr auto; gap: 0.5rem; margin-bottom: 0.4rem; }

.form-footer {
  position: sticky; bottom: 0;         /* Save button always reachable */
  background: white; border-top: 1px solid #e5e7eb;
  display: flex; gap: 0.5rem; padding: 0.9rem 0; margin-top: 1.2rem;
}
</style>