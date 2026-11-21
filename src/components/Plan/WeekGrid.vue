<!-- The weekly grid: 7 days across, 4 meal slots down.
     It only DISPLAYS entries. Clicking a button sends an event up to PlansView,
     which changes the data. -->
<template>
  <div class="table-wrap">
    <table class="week">
      <thead>
        <tr>
          <th class="slot"></th>
          <th v-for="day in DAYS" :key="day">{{ day }}</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="meal in MEAL_TYPES" :key="meal">
          <th class="slot">{{ meal }}</th>

          <td v-for="day in DAYS" :key="day">
            <!-- Every recipe in this cell (a cell can hold several) -->
            <div v-for="e in cell(day, meal)" :key="e.id" class="chip">
              <strong>{{ e.recipeTitle }}</strong>
              <div class="servings">{{ e.servings }} serving{{ e.servings === 1 ? '' : 's' }}</div>
              <div class="chip-buttons">
                <button type="button" @click="emit('edit', e)">Edit</button>
                <button type="button" @click="emit('remove', e)">Remove</button>
              </div>
            </div>

            <!-- The + button: add a recipe to THIS cell -->
            <button
              type="button"
              class="cell-add"
              :aria-label="`Add a recipe on ${day} ${meal}`"
              @click="emit('add', day, meal)"
            >+</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { DAYS, MEAL_TYPES } from '../../constants.js'

const props = defineProps({
  entries: { type: Array, required: true },   // this plan's entries (with recipeTitle)
})
const emit = defineEmits(['add', 'edit', 'remove'])

// All entries sitting in one cell
function cell(day, meal) {
  return props.entries.filter(e => e.day === day && e.mealType === meal)
}
</script>

<style scoped>
.table-wrap { overflow-x: auto; }       /* the grid scrolls sideways on small screens */
.week { width: 100%; min-width: 760px; border-collapse: collapse; table-layout: fixed; }
th { font-size: 0.8rem; color: #6b7280; padding: 0.5rem 0.3rem; background: #f7f9f7; border: 1px solid #e5e7eb; }
th.slot { width: 78px; text-align: left; padding-left: 0.5rem; }
td { border: 1px solid #e5e7eb; padding: 0.35rem; vertical-align: top; height: 92px; }

.chip { background: #e3efe8; border-left: 3px solid #2c6a4d; border-radius: 4px; padding: 0.25rem 0.4rem; margin-bottom: 0.3rem; font-size: 0.78rem; }
.servings { color: #4b5563; }
.chip-buttons { display: flex; gap: 0.3rem; margin-top: 0.2rem; }
.chip-buttons button { font: inherit; font-size: 0.7rem; padding: 0 0.35rem; cursor: pointer; border: 1px solid #d1d5db; background: white; border-radius: 4px; }

.cell-add { font: inherit; width: 100%; background: none; border: 1px dashed #b8c4b8; color: #6b7280; border-radius: 4px; cursor: pointer; }
.cell-add:hover { background: #e3efe8; color: #1f4f3a; }
</style>