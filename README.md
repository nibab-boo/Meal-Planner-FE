# Frontend (app/)

The Vue 3 website for the Meal Planner. This file explains how the frontend is organised so any team member can find their way around.

## Commands

Run these inside the `app/` folder.

| Command | What it does |
|---|---|
| `npm install` | Installs everything listed in `package.json` (first time only) |
| `npm run dev` | Starts the website at http://localhost:5173 |
Don't try these 2 for now
| `npm run build` | Builds the site into a `dist/` folder |
| `npm run preview` | Serves the built site locally |

Versions: Vue ^3.5.44, Vue Router ^5.5.1, Vite ^8.3.6, @vitejs/plugin-vue ^6.0.10. Developed with Node v24.18.0.

## Folder map

```
src/
├── main.js            starts Vue, plugs in the router, loads style.css
├── App.vue            navigation bar + <RouterView />, no logic
├── style.css          global styles: body, buttons, slide-in drawers
├── constants.js       API address, DAYS, MEAL_TYPES (one place to change them)
├── router/index.js    the three routes
├── composables/       reusable logic (useFetch)
├── views/             pages: one file per route
└── components/        reusable pieces used inside the views. Componenets for each view is divided further by Folder.
```

| Where does it go? | Folder |
|---|---|
| A page with its own URL | `views/` |
| A reusable piece of the page | `components/` |
| Logic without HTML, shared by several files | `composables/` |
| A fixed list or value used in several files | `constants.js` |

## Pages (routes)

| URL | View | Purpose |
|---|---|---|
| `/` | `DashboardView.vue` | Summary cards, recent recipes, two extra panels |
| `/recipes` | `RecipesView.vue` | Recipe list, add and edit form, recipe details and plan usage |
| `/plans` | `PlansView.vue` | Plan list, add and edit form, weekly grid, entry form |

## Components

Data goes **down** as props. Events go **up** with `emit`. A component never changes the data itself; the view does.

| Component | Props | Emits | Used in |
|---|---|---|---|
| `StatCard` | `label`, `value`, `highlight` | none | Dashboard (4 cards) |
| `RecentRecipes` | `recipes` | none | Dashboard |
| `BarPanel` | `title`, `items`, `emptyText` | none | Dashboard (twice) |
| `RecipeForm` | `recipe` (`null` = adding) | `save`, `close` | Recipes, left drawer |
| `RecipeDetail` | `recipe`, `entries`, `plans`, `error` | `close`, `edit`, `add-entry`, `remove-entry` | Recipes, right drawer |
| `PlanForm` | `plan` (`null` = adding) | `save`, `close` | Plans, left drawer |
| `EntryForm` | `entry` (`null` = adding), `recipes`, `initialDay`, `initialMeal`, `error` | `save`, `close` | Plans, right drawer |
| `WeekGrid` | `entries` | `add`, `edit`, `remove` | Plans |
| `StatusBadge` | `status` | none | Plans |

## The slide-in drawers

The add and edit forms slide in over half of the screen. It is only CSS classes (in `style.css`), and Vue adds or removes the word `open`.

| Class | Effect |
|---|---|
| `.drawer` | A panel parked off-screen on the left |
| `.drawer.open` | Slides it into view (50% of the screen, at least 440px wide) |
| `.drawer.from-right` | Same panel, but from the right side |
| `.slide-page.pushed-left` / `.pushed-right` | Moves the page aside so the list stays visible |

In a view:

```vue
<div class="drawer" :class="{ open: showForm }">
  <RecipeForm :key="formKey" :recipe="editing" @save="saveRecipe" @close="closeForm" />
</div>
```

- Only one drawer is open at a time.
- A drawer stays open until Save, Cancel or Close is pressed.
- `formKey` goes up every time a form opens, so Vue builds a fresh form and clears old text.
- Editing works on a copy of the item, so nothing changes until Save.

## Conventions

- Every `.vue` file is ordered `<template>`, then `<script setup>`, then `<style scoped>`.
- Plain CSS only. Styles are scoped per component; only things shared by many files (buttons, drawers) are in `style.css`.
- Forms use `reactive`, and number inputs use `v-model.number`.
- Every `v-for` has a unique `:key`.
- Every fetch has a loading state and an error state (`v-if` / `v-else-if` / `v-else` in the template).
- The API address is set once, in `constants.js`.

## Data used by the views

| View | Fetches |
|---|---|
| Dashboard | `GET /stats` |
| Recipes | `GET /recipes`, `GET /plans`, `GET /entries`, TheMealDB (categories, meals, details) |
| Plans | `GET /plans`, `GET /recipes`, `GET /entries` |