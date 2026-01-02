<script lang="ts">
  import BarChart from "./BarChart.svelte";
  export let bigrams: Record<string, number>;
  export let trigrams: Record<string, number>;

  let selected = "Bigrams";

  function getTop(type: string) {
    const source = type === "Bigrams" ? bigrams : trigrams;
    if (!source) return [];
    return Object.entries(source)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);
  }

  $: if (bigrams || trigrams) {
    selected = "Bigrams";
  }
</script>

<div class="mb-4 inline-flex border border-slate-950 rounded-md">
  <button
    class="px-4 py-2 border font-semibold transition-colors focus:outline-none {selected ===
    'Bigrams'
      ? 'bg-slate-800 text-white border-slate-800'
      : 'bg-white text-slate-800 border-slate-800 hover:bg-slate-100'}"
    on:click={() => (selected = "Bigrams")}
  >
    Bigrams
  </button>
  <button
    class="px-4 py-2 border font-semibold transition-colors focus:outline-none {selected ===
    'Trigrams'
      ? 'bg-slate-800 text-white border-slate-800'
      : 'bg-white text-slate-800 border-slate-800 hover:bg-slate-100'}"
    on:click={() => (selected = "Trigrams")}
  >
    Trigrams
  </button>
</div>

{#key selected}
  <BarChart data={getTop(selected)} />
{/key}
