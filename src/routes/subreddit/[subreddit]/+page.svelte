<script>
  import WordCloud from "$lib/WordCloud.svelte";
  import PieChart from "$lib/PieChart.svelte";
  import BarChart from "$lib/BarChart.svelte";
  import CategoryBarChart from "$lib/CategoryBarChart.svelte";
  import NgramBarChart from "$lib/NgramBarChart.svelte";
  import StackedBarChart from "$lib/StackedBarChart.svelte";
  export let data;

  function downloadJSON() {
    const jsonString = JSON.stringify(data.analysis, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${data.subreddit}_analysis.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
</script>

<div class="container mx-auto p-8">
  <div class="flex justify-between items-center">
    <h1 class="text-4xl font-bold text-gray-800">
      Analysis for /r/{data.subreddit}
    </h1>
    <button
      on:click={downloadJSON}
      class="p-2 rounded-full bg-gray-700 text-white hover:bg-gray-600 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500"
      aria-label="Download JSON"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
        />
      </svg>
    </button>
  </div>

  <!-- Word Cloud -->
  <div
    class="mt-8 rounded-lg bg-white p-6 shadow-md md:items-start"
    style="height: 40vh;"
  >
    <WordCloud words={Object.entries(data.analysis.most_common_words)} />
  </div>

  <div class="mt-8 grid grid-cols-1 gap-8 md:grid-cols-2 md:items-start">
    <!-- POS Ratios -->
    <div class="rounded-lg bg-white p-6 shadow-md">
      <h2 class="text-2xl font-semibold text-gray-700">
        Grammatical Category Ratios
      </h2>
      <PieChart data={Object.entries(data.analysis.pos_ratios)} />
    </div>

    <!-- Most Common Words -->
    <div class="rounded-lg bg-white p-6 shadow-md">
      <h2 class="text-2xl font-semibold text-gray-700">Most Common Words</h2>
      <BarChart
        data={Object.entries(data.analysis.most_common_words).slice(0, 15)}
      />
    </div>
  </div>

  <!-- Categorized Common Words -->
  <div class="mt-8 rounded-lg bg-white p-6 shadow-md">
    <h2 class="text-2xl font-semibold text-gray-700">
      Most Common Words by Category
    </h2>
    <CategoryBarChart
      categories={{
        nouns: data.analysis.most_common_nouns,
        verbs: data.analysis.most_common_verbs,
        adjectives: data.analysis.most_common_adjectives,
        adverbs: data.analysis.most_common_adverbs,
      }}
      categoryNames={["Nouns", "Verbs", "Adjectives", "Adverbs"]}
    />
  </div>

  <!-- N-grams -->
  <div class="mt-8 rounded-lg bg-white p-6 shadow-md">
    <h2 class="text-2xl font-semibold text-gray-700">Most Common N-grams</h2>
    <NgramBarChart
      bigrams={data.analysis.most_common_bigrams}
      trigrams={data.analysis.most_common_trigrams}
    />
  </div>

  <!-- Word Length Distributions -->
  <div class="mt-8 rounded-lg bg-white p-6 shadow-md">
    <h2 class="text-2xl font-semibold text-gray-700">
      Word Length Distributions
    </h2>
    <StackedBarChart
      data={{
        nouns: data.analysis.word_length_distributions.nouns,
        verbs: data.analysis.word_length_distributions.verbs,
        adjectives: data.analysis.word_length_distributions.adjectives,
        adverbs: data.analysis.word_length_distributions.adverbs,
      }}
      categories={["Nouns", "Verbs", "Adjectives", "Adverbs"]}
      colors={["#3b82f6", "#10b981", "#f59e42", "#ef4444"]}
    />
  </div>
</div>
