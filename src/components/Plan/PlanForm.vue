<!-- The form inside the LEFT drawer. Used for BOTH adding and editing a plan.
     plan = null   → "New plan" (empty form)
     plan = {...}  → "Edit plan" (form starts filled in) -->
<template>
  <form class="form" @submit.prevent="save">
    <div class="form-header">
      <h2>{{ plan ? 'Edit plan' : 'New plan' }}</h2>
      <button type="button" class="btn btn-small" @click="emit('close')">Close ✕</button>
    </div>

    <div class="fields">
      <div class="field wide">
        <label for="p-name">Plan name</label>
        <input id="p-name" v-model="form.name" required />
      </div>

      <div class="field">
        <label for="p-start">Start date (first day of the week)</label>
        <input id="p-start" type="date" v-model="form.startDate" required />
      </div>

      <div class="field">
        <label for="p-status">Status</label>
        <select id="p-status" v-model="form.status">
          <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>

      <div class="field wide">
        <label for="p-notes">Notes (goals or comments)</label>
        <textarea id="p-notes" v-model="form.notes"></textarea>
      </div>
    </div>
    <p v-if="error" class="error-text">⚠ {{ error }}</p>
    <div class="form-footer">
      <button class="btn btn-primary">Save plan</button>
      <button type="button" class="btn" @click="emit('close')">Cancel</button>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  plan: { type: Object, default: null },
  error: { type: String, default: '' },
})
const emit = defineEmits(['save', 'close'])

const statuses = ['Active', 'Archived']

// The Monday of this week, written like 2026-11-16 (the format <input type="date"> uses)
function thisMonday() {
  const d = new Date()
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7))
  const pad = n => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

// Editing? Make a COPY, so typing does not change the list until Save.
const form = reactive(
  props.plan
    ? JSON.parse(JSON.stringify(props.plan))
    : { name: '', startDate: thisMonday(), notes: '', status: 'Active' }
)

function save() {
  emit('save', { ...form, name: form.name.trim() })
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

label { font-size: 0.82rem; font-weight: 600; color: #6b7280; }
input, select, textarea {
  font: inherit; padding: 0.45rem 0.6rem; width: 100%; box-sizing: border-box;
  border: 1px solid #d1d5db; border-radius: 6px; background: white;
}
textarea { min-height: 110px; resize: vertical; }

.form-footer {
  position: sticky; bottom: 0;
  background: white; border-top: 1px solid #e5e7eb;
  display: flex; gap: 0.5rem; padding: 0.9rem 0; margin-top: 1.2rem;
}
.error-text { color: #dc2626; margin: 0.5rem 0 0; }
</style>