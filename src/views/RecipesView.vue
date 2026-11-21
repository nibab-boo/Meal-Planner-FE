<template>
  <div>
    <!-- LEFT DRAWER: add / edit form -->
    <div class="drawer" :class="{ open: showForm }">
      <RecipeForm :key="formKey" :recipe="editing" @save="saveRecipe" @close="closeForm" />
    </div>

    <!-- RIGHT DRAWER: one recipe's details, plan usage, add to plan, remove from plan -->
    <div class="drawer from-right" :class="{ open: showDetail }">
      <RecipeDetail
        v-if="selectedRecipe"
        :key="selectedId"
        :recipe="selectedRecipe"
        :entries="selectedEntries"
        :plans="plans"
        :error="entryError"
        @close="closeDetail"
        @edit="openEdit(selectedRecipe)"
        @add-entry="addEntry"
        @remove-entry="removeEntry"
      />
    </div>

    <!-- THE PAGE: moves aside while a drawer is open -->
    <div class="slide-page" :class="{ 'pushed-left': showForm, 'pushed-right': showDetail }">
      <div class="recipes">
        <div class="header">
          <h1>Recipes</h1>
          <button class="btn btn-primary" @click="openAdd">+ Add recipe</button>
        </div>

        <p v-if="loading" class="state">Loading recipes...</p>
        <p v-else-if="error" class="state error">⚠ {{ error }}</p>

        <section v-else class="panel">
          <p v-if="recipes.length === 0" class="empty">No recipes yet. Click "Add recipe" to create your first one.</p>

          <div v-else class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Category</th>
                  <th>Area</th>
                  <th class="num">Prep (min)</th>
                  <th class="num">Calories</th>
                  <th class="num">Plans</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="r in recipes" :key="r.id" :class="{ selected: showDetail && r.id === selectedId }">
                  <td>
                    <!-- Click the title to open the details drawer -->
                    <button class="title-link" @click="openDetail(r)">{{ r.title }}</button>
                  </td>
                  <td>{{ r.category }}</td>
                  <td>{{ r.area }}</td>
                  <td class="num">{{ r.prepTime }}</td>
                  <td class="num">{{ r.calories }}</td>
                  <td class="num">{{ planCount(r.id) }}</td>
                  <td class="actions">
                    <button class="btn btn-small" @click="openEdit(r)">Edit</button>
                    <button class="btn btn-small btn-danger" @click="deleteRecipe(r)">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>    
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
    import { ref, computed } from 'vue'
    import RecipeForm from '../components/Recipe/RecipeForm.vue'
    import RecipeDetail from '../components/Recipe/RecipeDetail.vue'

    // ── PLACEHOLDER DATA (later: fetched from the API) ───────
    const recipes = ref([
    {
        id: 1, title: 'Spicy Arrabiata Penne', description: 'Quick tomato and chilli pasta.',
        category: 'Vegetarian', area: 'Italian', prepTime: 25, calories: 520, servings: 2,
        ingredients: [{ name: 'Penne rigate', measure: '1 pound' }, { name: 'Garlic', measure: '3 cloves' }],
        instructions: 'Boil the pasta. Fry garlic and chilli, add tomatoes, toss together.', imageUrl: '',
    },
    {
        id: 2, title: 'Grilled Salmon with Greens', description: 'High-protein dinner.',
        category: 'Seafood', area: 'British', prepTime: 20, calories: 430, servings: 2,
        ingredients: [{ name: 'Salmon fillets', measure: '2' }, { name: 'Spinach', measure: '200g' }],
        instructions: 'Grill the salmon 4 minutes per side. Wilt the spinach.', imageUrl: '',
    },
    {
        id: 3, title: 'Overnight Oats', description: 'Make-ahead breakfast.',
        category: 'Breakfast', area: 'American', prepTime: 5, calories: 340, servings: 1,
        ingredients: [{ name: 'Rolled oats', measure: '1/2 cup' }, { name: 'Milk', measure: '1/2 cup' }],
        instructions: 'Mix in a jar and chill overnight.', imageUrl: '',
    },
    ])

    // The plans (later: GET /plans). Used for the "Add to a plan" dropdown.
    const plans = ref([
    { id: 1, name: 'Client A – Week 47' },
    { id: 2, name: 'Client B – Week 47' },
    { id: 3, name: 'Client A – Week 46' },
    ])

    // The entries = the link between recipes and plans (later: GET /entries).
    // One entry = one recipe, in one plan, on one day, in one meal slot.
    const entries = ref([
    { id: 1, planId: 1, recipeId: 3, day: 'Monday',    mealType: 'Breakfast', servings: 1 },
    { id: 2, planId: 1, recipeId: 2, day: 'Monday',    mealType: 'Dinner',    servings: 2 },
    { id: 3, planId: 1, recipeId: 2, day: 'Thursday',  mealType: 'Dinner',    servings: 2 },
    { id: 4, planId: 2, recipeId: 1, day: 'Tuesday',   mealType: 'Lunch',     servings: 2 },
    { id: 5, planId: 3, recipeId: 3, day: 'Monday',    mealType: 'Breakfast', servings: 1 },
    { id: 6, planId: 2, recipeId: 3, day: 'Tuesday',   mealType: 'Breakfast', servings: 1 },
    ])

    const loading = ref(false)
    const error   = ref(null)

    // ── LEFT DRAWER: the add / edit form ─────────────────────
    const showForm = ref(false)   // is the form drawer open?
    const editing  = ref(null)    // the recipe being edited, or null when adding
    const formKey  = ref(0)       // a new key = a brand-new form (clears old text)

    function openAdd() {
    editing.value = null
    formKey.value++
    showDetail.value = false    // only one drawer at a time
    showForm.value = true
    }

    function openEdit(recipe) {
    editing.value = recipe
    formKey.value++
    showDetail.value = false
    showForm.value = true
    }

    // We only hide the drawer. We do NOT reset "editing" here, otherwise the
    // title would flip to "New recipe" while the drawer is still sliding out.
    function closeForm() {
    showForm.value = false
    }

    // ── RIGHT DRAWER: the details ────────────────────────────
    const showDetail = ref(false)   // is the details drawer open?
    const selectedId = ref(null)    // which recipe is shown
    const entryError = ref('')      // message shown under the "Add to a plan" form

    const selectedRecipe = computed(() =>
    recipes.value.find(r => r.id === selectedId.value) || null
    )

    // This recipe's entries, each with its plan's name added for display
    const selectedEntries = computed(() =>
    entries.value
        .filter(e => e.recipeId === selectedId.value)
        .map(e => ({ ...e, planName: planName(e.planId) }))
    )

    function openDetail(recipe) {
    selectedId.value = recipe.id
    entryError.value = ''
    showForm.value = false      // only one drawer at a time
    showDetail.value = true
    }

    function closeDetail() {
    showDetail.value = false
    }

    function planName(planId) {
    const plan = plans.value.find(p => p.id === planId)
    return plan ? plan.name : '(deleted plan)'
    }

    // How many DIFFERENT plans use this recipe.
    // A Set keeps each plan only once, even if the recipe is in it twice.
    function planCount(recipeId) {
    const planIds = entries.value.filter(e => e.recipeId === recipeId).map(e => e.planId)
    return new Set(planIds).size
    }

    // ── ADD / REMOVE A RECIPE FROM A PLAN ────────────────────
    function nextEntryId() {
    return Math.max(0, ...entries.value.map(e => e.id)) + 1
    }

    function addEntry(data) {
    // Same recipe + plan + day + meal slot twice is not allowed.
    // (Later the SERVER checks this and sends back a 409 error message.)
    const duplicate = entries.value.some(e =>
        e.recipeId === selectedId.value &&
        e.planId === data.planId &&
        e.day === data.day &&
        e.mealType === data.mealType
    )
    if (duplicate) {
        entryError.value = `This recipe is already in that plan on ${data.day} ${data.mealType}.`
        return
    }

    entryError.value = ''
    entries.value.push({ ...data, id: nextEntryId(), recipeId: selectedId.value })
    }

    function removeEntry(entry) {
    if (!confirm(`Remove from "${entry.planName}" (${entry.day} ${entry.mealType})?`)) return
    entries.value = entries.value.filter(e => e.id !== entry.id)
    }

    // ── ADD / EDIT / DELETE A RECIPE ─────────────────────────
    function nextId() {
    return Math.max(0, ...recipes.value.map(r => r.id)) + 1
    }

    function saveRecipe(data) {
    if (editing.value) {
        // EDIT: replace the recipe that has the same id
        recipes.value = recipes.value.map(r =>
        r.id === editing.value.id ? { ...r, ...data } : r
        )
    } else {
        // ADD: give it a new id and put it in the list
        recipes.value.push({ ...data, id: nextId() })
    }
    closeForm()
    }

    function deleteRecipe(recipe) {
        const count = planCount(recipe.id)
        const warning = count > 0 ? ` It will also be removed from ${count} plan(s).` : ''
        if (!confirm(`Delete "${recipe.title}"?${warning}`)) return

        recipes.value = recipes.value.filter(r => r.id !== recipe.id)
        // CASCADE: a recipe that no longer exists can't stay in any plan
        entries.value = entries.value.filter(e => e.recipeId !== recipe.id)

        if (selectedId.value === recipe.id) {
            closeDetail()
            selectedId.value = null
        }
        if (editing.value && editing.value.id === recipe.id) closeForm()
    }
</script>

<style scoped>
    .recipes { max-width: 1000px; margin: 0 auto; padding: 1.75rem 1.25rem 3rem; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
    h1 { font-size: 1.6rem; margin: 0; }

    .panel { background: white; border-radius: 8px; padding: 1rem 1.25rem; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07); }
    .table-wrap { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: 0.65rem 0.7rem; border-bottom: 1px solid #f0f2f0; }
    th { font-size: 0.82rem; color: #6b7280; }
    .num { text-align: right; }
    .actions { display: flex; gap: 0.4rem; justify-content: flex-end; white-space: nowrap; }
    tr.selected { background: #f1f7f3; }

    /* A button that looks like a link */
    .title-link {
    background: none; border: none; padding: 0; font: inherit; font-weight: 700;
    color: #1f4f3a; cursor: pointer; text-align: left;
    }
    .title-link:hover { text-decoration: underline; }

    .state { color: #9ca3af; }
    .error { color: #dc2626; }
    .empty { color: #9ca3af; font-style: italic; }
</style>