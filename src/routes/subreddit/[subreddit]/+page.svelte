<script lang="ts">
  import { onMount } from "svelte";
  import WordCloud from "$lib/WordCloud.svelte";
  import PieChart from "$lib/PieChart.svelte";
  import BarChart from "$lib/BarChart.svelte";
  import CategoryBarChart from "$lib/CategoryBarChart.svelte";
  import NgramBarChart from "$lib/NgramBarChart.svelte";
  import StackedBarChart from "$lib/StackedBarChart.svelte";
  export let data;

  const categoryMap: { [key: string]: string } = {
    noun: "Nouns",
    verb: "Verbs",
    adj: "Adjectives",
    adv: "Adverbs",
    propn: "Proper Nouns",
    other: "Other",
  };

  const grammaticalCategoryRatios = Object.entries(
    data.analysis.pos_ratios,
  ).map(([key, value]) => [categoryMap[key.toLowerCase()] || key, value]);

  let showFullDescription = false;
  let threshold = 35;

  onMount(() => {
    const updateThreshold = () => {
      if (window.innerWidth < 640) threshold = 20;
      else if (window.innerWidth < 1024) threshold = 30;
      else threshold = 50;
    };
    updateThreshold();
    window.addEventListener("resize", updateThreshold);
    return () => window.removeEventListener("resize", updateThreshold);
  });

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

<svelte:head>
  <title>/r/{data.subreddit} - Subreddit Language Lab</title>
</svelte:head>

<div class="container mx-auto p-8">
  <div class="flex justify-between items-center">
    <h1 class="text-4xl font-bold text-gray-800">
      /r/{data.analysis.display_name || data.subreddit}
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

  <!-- Metadata -->
  <div class="mt-2 text-gray-600 flex flex-col space-y-2">
    <div class="flex items-center">
      <span class="material-icons text-base">description</span>
      <span
        class="ml-2 {data.analysis.description &&
        data.analysis.description.length > threshold &&
        !showFullDescription
          ? 'line-clamp-1'
          : ''}"
      >
        {data.analysis.description || "N/A"}
      </span>
      {#if data.analysis.description && data.analysis.description.length > threshold}
        <button
          on:click={() => (showFullDescription = !showFullDescription)}
          class="ml-1 text-blue-500 text-sm whitespace-nowrap"
        >
          {showFullDescription ? "Read less" : "Read more"}
        </button>
      {/if}
    </div>
    <div class="flex items-center">
      <span class="material-icons text-base">people</span>
      <span class="ml-2"
        >{data.analysis.subscribers?.toLocaleString() || "N/A"}</span
      >
    </div>
    <div class="flex items-center">
      <span class="material-icons">cake</span>
      <span class="ml-2">{data.analysis.created_date || "N/A"}</span>
    </div>
  </div>

  <!-- Word Cloud -->
  <div
    class="mt-4 rounded-lg bg-white p-4 shadow-md md:items-start"
    style="height: 40vh;"
  >
    <WordCloud words={Object.entries(data.analysis.most_common_words)} />
  </div>

  <div class="mt-8 grid grid-cols-1 gap-8 md:grid-cols-2">
    <!-- POS Ratios -->
    <div class="rounded-lg bg-white p-6 shadow-md flex flex-col">
      <h2 class="text-2xl font-semibold text-gray-700 pb-6">
        Grammatical Category Ratios
      </h2>
      <div class="flex-grow">
        <PieChart data={grammaticalCategoryRatios as [string, number][]} />
      </div>
    </div>

    <!-- Most Common Words -->
    <div class="rounded-lg bg-white p-6 shadow-md flex flex-col">
      <h2 class="text-2xl font-semibold text-gray-700">Most Common Words</h2>
      <div class="flex-grow">
        <BarChart
          data={Object.entries(data.analysis.most_common_words).slice(
            0,
            15,
          ) as [string, number][]}
        />
      </div>
    </div>
  </div>

  <!-- Categorized Common Words -->
  <div class="mt-8 rounded-lg bg-white p-6 shadow-md">
    <h2 class="text-2xl font-semibold text-gray-700 mb-4">
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
    <h2 class="text-2xl font-semibold text-gray-700 mb-4">
      Most Common N-grams
    </h2>
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
    />
  </div>
</div>
