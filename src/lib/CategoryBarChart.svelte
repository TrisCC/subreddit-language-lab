<script lang="ts">
  import { onMount } from "svelte";
  import BarChart from "./BarChart.svelte";

  export let categories: Record<string, Record<string, number>>;
  export let categoryNames: string[] = [
    "Nouns",
    "Verbs",
    "Adjectives",
    "Adverbs",
  ];

  let selectedCategory = categoryNames[0];

  function getTopWords(cat: string) {
    const categoryData = categories[cat.toLowerCase()];
    if (!categoryData) return [];
    return Object.entries(categoryData)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15);
  }

  $: if (categories) {
    selectedCategory = categoryNames[0];
  }
</script>

<div class="mb-4 inline-flex border border-slate-950 rounded-md">
  {#each categoryNames as cat}
    <button
      class="px-4 py-2 border font-semibold transition-colors focus:outline-none {selectedCategory ===
      cat
        ? 'bg-slate-800 text-white border-slate-800'
        : 'bg-white text-slate-800 border-slate-800 hover:bg-slate-100'}"
      on:click={() => (selectedCategory = cat)}
    >
      {cat}
    </button>
  {/each}
</div>

{#key selectedCategory}
  <BarChart data={getTopWords(selectedCategory)} />
{/key}
