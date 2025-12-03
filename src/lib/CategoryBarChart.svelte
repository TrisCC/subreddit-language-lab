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
    return Object.entries(categories[cat.toLowerCase()])
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15);
  }
</script>

<div class="mb-4 flex gap-2">
  {#each categoryNames as cat}
    <button
      class="px-4 py-2 rounded-md border font-semibold transition-colors focus:outline-none {selectedCategory ===
      cat
        ? 'bg-blue-500 text-white border-blue-500'
        : 'bg-white text-blue-500 border-blue-500 hover:bg-blue-100'}"
      on:click={() => (selectedCategory = cat)}
    >
      {cat}
    </button>
  {/each}
</div>

{#key selectedCategory}
  <BarChart data={getTopWords(selectedCategory)} />
{/key}
