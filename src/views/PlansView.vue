<template>
  <div>
    <!-- LEFT DRAWER: add / edit a plan -->
    <div class="drawer" :class="{ open: showPlanForm }">
      <PlanForm :key="planFormKey" :plan="editingPlan" @save="savePlan" @close="closePlanForm" />
    </div>

    <!-- RIGHT DRAWER: add / edit one recipe in one cell of the grid -->
    <div class="drawer from-right" :class="{ open: showEntryForm }">
      <EntryForm
        :key="entryFormKey"
        :entry="editingEntry"
        :recipes="recipes"
        :initial-day="entryCell.day"
        :initial-meal="entryCell.meal"
        :error="entryError"
        @save="saveEntry"
        @close="closeEntryForm"
      />
    </div>

    <!-- THE PAGE: moves aside while a drawer is open -->
    <div class="slide-page" :class="{ 'pushed-left': showPlanForm, 'pushed-right': showEntryForm }">
      <div class="plans">
        <div class="header">
          <h1>Plans</h1>
          <button class="btn btn-primary" @click="openAddPlan">+ Add plan</button>
        </div>

        <p v-if="loading" class="state">Loading plans...</p>
        <p v-else-if="error" class="state error">⚠ {{ error }}</p>

        <div v-else>
          <!-- 1. THE LIST OF PLANS -->
          <section class="panel">
            <p v-if="plans.length === 0" class="empty">No plans yet. Click "Add plan" to create your first one.</p>

            <template v-else>
              <p class="hint">Click a plan name to open its weekly grid.</p>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Start date</th>
                      <th>Status</th>
                      <th class="num">Meals planned</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="p in plans" :key="p.id" :class="{ selected: p.id === selectedPlanId }">
                      <td><button class="title-link" @click="openGrid(p)">{{ p.name }}</button></td>
                      <td>{{ p.startDate }}</td>
                      <td><StatusBadge :status="p.status" /></td>
                      <td class="num">{{ mealCount(p.id) }}</td>
                      <td class="actions">
                        <button class="btn btn-small" @click="openEditPlan(p)">Edit</button>
                        <button class="btn btn-small btn-danger" @click="deletePlan(p)">Delete</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </template>
          </section>

          <!-- 2. THE WEEKLY GRID of the selected plan (same page, no navigation) -->
          <section v-if="selectedPlan" class="panel">
            <div class="grid-header">
              <div>
                <h2>{{ selectedPlan.name }}</h2>
                <p class="meta">
                  Week starting {{ selectedPlan.startDate }}
                  <StatusBadge :status="selectedPlan.status" />
                </p>
                <p v-if="selectedPlan.notes" class="notes">{{ selectedPlan.notes }}</p>
              </div>
              <button class="btn btn-small" @click="closeGrid">Close grid ✕</button>
            </div>

            <WeekGrid
              :entries="selectedEntries"
              @add="openAddEntry"
              @edit="openEditEntry"
              @remove="removeEntry"
            />
          </section>
        </div>
      </div>
    </div>
  </div>
</template>




<!-- Javascript -->

<script setup>
    import { ref, computed } from 'vue'
    
    // Components
    import PlanForm from '../components/Plan/PlanForm.vue'
    import EntryForm from '../components/Plan/EntryForm.vue'
    import WeekGrid from '../components/Plan/WeekGrid.vue'
    import StatusBadge from '../components/Plan/StatusBadge.vue'

    // ── PLACEHOLDER DATA (later: fetched from the API) ───────
    const plans = ref([
    { id: 1, name: 'Client A – Week 47', startDate: '2026-11-16', notes: 'Higher protein, lower sugar.', status: 'Active' },
    { id: 2, name: 'Client B – Week 47', startDate: '2026-11-16', notes: 'Vegetarian.', status: 'Active' },
    { id: 3, name: 'Client A – Week 46', startDate: '2026-11-09', notes: 'Completed.', status: 'Archived' },
    ])

    // The recipes (later: GET /recipes). Used for the recipe dropdown.
    const recipes = ref([
    { id: 1, title: 'Spicy Arrabiata Penne' },
    { id: 2, title: 'Grilled Salmon with Greens' },
    { id: 3, title: 'Overnight Oats' },
    ])

    // The entries: one recipe, in one plan, on one day, in one meal slot (later: GET /entries)
    const entries = ref([
    { id: 1, planId: 1, recipeId: 3, day: 'Monday',   mealType: 'Breakfast', servings: 1 },
    { id: 2, planId: 1, recipeId: 2, day: 'Monday',   mealType: 'Dinner',    servings: 2 },
    { id: 3, planId: 1, recipeId: 2, day: 'Thursday', mealType: 'Dinner',    servings: 2 },
    { id: 4, planId: 2, recipeId: 1, day: 'Tuesday',  mealType: 'Lunch',     servings: 2 },
    { id: 5, planId: 3, recipeId: 3, day: 'Monday',   mealType: 'Breakfast', servings: 1 },
    { id: 6, planId: 2, recipeId: 3, day: 'Tuesday',  mealType: 'Breakfast', servings: 1 },
    ])

    const loading = ref(false)
    const error   = ref(null)

    // How many meals a plan has
    function mealCount(planId) {
    return entries.value.filter(e => e.planId === planId).length
    }

    // ── LEFT DRAWER: the plan form ───────────────────────────
    const showPlanForm = ref(false)
    const editingPlan  = ref(null)   // the plan being edited, or null when adding
    const planFormKey  = ref(0)      // a new key = a brand-new form (clears old text)

    function openAddPlan() {
    editingPlan.value = null
    planFormKey.value++
    showEntryForm.value = false    // only one drawer at a time
    showPlanForm.value = true
    }

    function openEditPlan(plan) {
    editingPlan.value = plan
    planFormKey.value++
    showEntryForm.value = false
    showPlanForm.value = true
    }

    // Only hide the drawer. Keep "editingPlan" so the title doesn't flip while sliding out.
    function closePlanForm() {
    showPlanForm.value = false
    }

    function nextPlanId() {
    return Math.max(0, ...plans.value.map(p => p.id)) + 1
    }

    function savePlan(data) {
    if (editingPlan.value) {
        // EDIT: replace the plan that has the same id
        plans.value = plans.value.map(p =>
        p.id === editingPlan.value.id ? { ...p, ...data } : p
        )
    } else {
        // ADD: give it a new id
        plans.value.push({ ...data, id: nextPlanId() })
    }
    closePlanForm()
    }

    function deletePlan(plan) {
    const count = mealCount(plan.id)
    const warning = count > 0 ? ` Its ${count} planned meal(s) will be removed too.` : ''
    if (!confirm(`Delete "${plan.name}"?${warning}`)) return

    plans.value = plans.value.filter(p => p.id !== plan.id)
    // CASCADE: entries of a deleted plan are removed too
    entries.value = entries.value.filter(e => e.planId !== plan.id)

    if (selectedPlanId.value === plan.id) closeGrid()
    if (editingPlan.value && editingPlan.value.id === plan.id) closePlanForm()
    }

    // ── THE WEEKLY GRID: which plan is open ──────────────────
    const selectedPlanId = ref(null)

    const selectedPlan = computed(() =>
    plans.value.find(p => p.id === selectedPlanId.value) || null
    )

    // This plan's entries, each with its recipe's title added for display
    const selectedEntries = computed(() =>
    entries.value
        .filter(e => e.planId === selectedPlanId.value)
        .map(e => ({ ...e, recipeTitle: recipeTitle(e.recipeId) }))
    )

    function recipeTitle(recipeId) {
    const recipe = recipes.value.find(r => r.id === recipeId)
    return recipe ? recipe.title : '(deleted recipe)'
    }

    function openGrid(plan) {
    selectedPlanId.value = plan.id
    showEntryForm.value = false    // an open entry form belongs to the previous plan
    }

    function closeGrid() {
    selectedPlanId.value = null
    showEntryForm.value = false
    }

    // ── RIGHT DRAWER: the entry form ─────────────────────────
    const showEntryForm = ref(false)
    const editingEntry  = ref(null)                                 // null when adding
    const entryCell     = ref({ day: 'Monday', meal: 'Breakfast' }) // the cell that was clicked
    const entryFormKey  = ref(0)
    const entryError    = ref('')                                   // message under the form

    // The "+" in a cell was clicked
    function openAddEntry(day, meal) {
        editingEntry.value = null
        entryCell.value = { day, meal }
        entryError.value = ''
        entryFormKey.value++
        showPlanForm.value = false     // only one drawer at a time
        showEntryForm.value = true
    }

    // "Edit" on an entry in the grid was clicked
    function openEditEntry(entry) {
        editingEntry.value = entry
        entryError.value = ''
        entryFormKey.value++
        showPlanForm.value = false
        showEntryForm.value = true
    }

    function closeEntryForm() {
        showEntryForm.value = false
    }

    function nextEntryId() {
        return Math.max(0, ...entries.value.map(e => e.id)) + 1
    }

    // Is this recipe already in this plan on this day and meal slot?
    // ignoreId lets an entry be edited without clashing with ITSELF.
    function isDuplicate(recipeId, day, mealType, ignoreId) {
        return entries.value.some(e =>
            e.id !== ignoreId &&
            e.planId === selectedPlanId.value &&
            e.recipeId === recipeId &&
            e.day === day &&
            e.mealType === mealType
        )
    }

    function saveEntry(data) {
        const isEditing = editingEntry.value !== null
        const recipeId  = isEditing ? editingEntry.value.recipeId : data.recipeId
        const ignoreId  = isEditing ? editingEntry.value.id : null

        // (Later the SERVER checks this and sends back a 409 error message.)
        if (isDuplicate(recipeId, data.day, data.mealType, ignoreId)) {
            entryError.value = `That recipe is already in this plan on ${data.day} ${data.mealType}.`
            return
        }
        entryError.value = ''

        if (isEditing) {
            // EDIT: only day, meal and servings can change. The entry keeps its id.
            entries.value = entries.value.map(e =>
            e.id === editingEntry.value.id
                ? { ...e, day: data.day, mealType: data.mealType, servings: data.servings }
                : e
            )
        } else {
            // ADD: a new entry that links this plan to the chosen recipe
            entries.value.push({
            id: nextEntryId(),
            planId: selectedPlanId.value,
            recipeId: data.recipeId,
            day: data.day,
            mealType: data.mealType,
            servings: data.servings,
            })
        }
        closeEntryForm()
    }

    function removeEntry(entry) {
        if (!confirm(`Remove "${entry.recipeTitle}" from ${entry.day} ${entry.mealType}?`)) return
        entries.value = entries.value.filter(e => e.id !== entry.id)
    }
</script>







<!-- CSS -->

<style scoped>
    .plans { max-width: 1200px; margin: 0 auto; padding: 1.75rem 1.25rem 3rem; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
    h1 { font-size: 1.6rem; margin: 0; }
    h2 { font-size: 1.2rem; margin: 0 0 0.25rem; }

    .panel { background: white; border-radius: 8px; padding: 1rem 1.25rem; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07); margin-bottom: 1.25rem; }
    .table-wrap { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: 0.65rem 0.7rem; border-bottom: 1px solid #f0f2f0; }
    th { font-size: 0.82rem; color: #6b7280; }
    .num { text-align: right; }
    .actions { display: flex; gap: 0.4rem; justify-content: flex-end; white-space: nowrap; }
    tr.selected { background: #f1f7f3; }

    .title-link {
    background: none; border: none; padding: 0; font: inherit; font-weight: 700;
    color: #1f4f3a; cursor: pointer; text-align: left;
    }
    .title-link:hover { text-decoration: underline; }

    .grid-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 0.9rem; }
    .meta { color: #6b7280; font-size: 0.88rem; margin: 0; }
    .notes { margin: 0.4rem 0 0; font-size: 0.9rem; }

    .hint { color: #6b7280; font-size: 0.85rem; margin: 0 0 0.5rem; }
    .state { color: #9ca3af; }
    .error { color: #dc2626; }
    .empty { color: #9ca3af; font-style: italic; }
</style>