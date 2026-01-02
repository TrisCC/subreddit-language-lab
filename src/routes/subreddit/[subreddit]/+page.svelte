<script lang="ts">
  import { onMount } from "svelte";
  import WordCloud from "$lib/WordCloud.svelte";
  import PieChart from "$lib/PieChart.svelte";
  import BarChart from "$lib/BarChart.svelte";
  import CategoryBarChart from "$lib/CategoryBarChart.svelte";
  import NgramBarChart from "$lib/NgramBarChart.svelte";
  import StackedBarChart from "$lib/StackedBarChart.svelte";
  import HelpButton from "$lib/HelpButton.svelte";
  import { base } from "$app/paths";
  export let data;

  const info = {
    wordCloud:
      "This word cloud visualizes the most common words in the subreddit. The size of each word is proportional to its frequency.",
    posRatios:
      "This pie chart shows the distribution of grammatical categories (nouns, verbs, adjectives, etc.) in the subreddit.",
    mostCommonWords:
      "A bar chart of the most common words in the subreddit, excluding common English stop words.",
    categorizedCommonWords:
      "Bar charts showing the most common words in the subreddit, categorized by their grammatical type (nouns, verbs, adjectives, and adverbs).",
    ngrams:
      "Bar charts showing the most common bigrams (two-word phrases) and trigrams (three-word phrases) in the subreddit.",
    wordLength:
      "A stacked bar chart showing the distribution of word lengths for different grammatical categories.",
  };

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
  let showDownloadTooltip = false;
  let showSubredditTooltip = false;
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
    <div class="flex items-center space-x-2">
      <div class="relative">
        <a
          href="https://www.reddit.com/r/{data.subreddit}"
          target="_blank"
          rel="noopener noreferrer"
          class="p-2 w-10 h-10 rounded-full bg-gray-700 text-white hover:bg-gray-600 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 flex items-center justify-center"
          aria-label="Go to Subreddit"
          on:mouseenter={() => (showSubredditTooltip = true)}
          on:mouseleave={() => (showSubredditTooltip = false)}
        >
          <img
            src="{base}/reddit-logo.png"
            alt="Go to Subreddit"
            class="h-6 w-6"
          />
        </a>
        {#if showSubredditTooltip}
          <div
            class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-max p-2 bg-gray-800 text-white text-xs rounded-md shadow-lg z-10"
            role="tooltip"
          >
            Visit /r/{data.subreddit}
          </div>
        {/if}
      </div>
      <div class="relative">
        <button
          on:click={downloadJSON}
          on:mouseenter={() => (showDownloadTooltip = true)}
          on:mouseleave={() => (showDownloadTooltip = false)}
          class="p-2 w-10 h-10 rounded-full bg-gray-700 text-white hover:bg-gray-600 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 flex items-center justify-center"
          aria-label="Download JSON"
        >
          <span class="material-symbols-outlined" style="font-size: 22px;">
            download
          </span>
        </button>
        {#if showDownloadTooltip}
          <div
            class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-max p-2 bg-gray-800 text-white text-xs rounded-md shadow-lg z-10"
            role="tooltip"
          >
            Download analysis data
          </div>
        {/if}
      </div>
    </div>
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
    class="rounded-lg bg-white md:items-start p-4 mt-4 shadow-md"
    style="height: 40vh;"
  >
    <div class="flex flex-row-reverse items-center">
      <HelpButton info={info.wordCloud} />
    </div>
    <WordCloud words={Object.entries(data.analysis.most_common_words)} />
  </div>

  <div class="grid grid-cols-1 gap-8 md:grid-cols-2 mt-4">
    <!-- POS Ratios -->
    <div class="rounded-lg bg-white p-6 shadow-md flex flex-col">
      <div class="flex items-center pb-6">
        <h2 class="text-2xl font-semibold text-gray-700">
          Grammatical Category Ratios
        </h2>
        <HelpButton info={info.posRatios} />
      </div>
      <div class="grow">
        <PieChart data={grammaticalCategoryRatios as [string, number][]} />
      </div>
    </div>

    <!-- Most Common Words -->
    <div class="rounded-lg bg-white p-6 shadow-md flex flex-col">
      <div class="flex items-center">
        <h2 class="text-2xl font-semibold text-gray-700">Most Common Words</h2>
        <HelpButton info={info.mostCommonWords} />
      </div>
      <div class="grow">
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
  <div class="mt-4 rounded-lg bg-white p-6 shadow-md">
    <div class="flex items-center mb-4">
      <h2 class="text-2xl font-semibold text-gray-700">
        Most Common Words by Category
      </h2>
      <HelpButton info={info.categorizedCommonWords} />
    </div>
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
  <div class="mt-4 rounded-lg bg-white p-6 shadow-md">
    <div class="flex items-center mb-4">
      <h2 class="text-2xl font-semibold text-gray-700">Most Common N-grams</h2>
      <HelpButton info={info.ngrams} />
    </div>
    <NgramBarChart
      bigrams={data.analysis.most_common_bigrams}
      trigrams={data.analysis.most_common_trigrams}
    />
  </div>

  <!-- Word Length Distributions -->
  <div class="mt-4 rounded-lg bg-white p-6 shadow-md">
    <div class="flex items-center">
      <h2 class="text-2xl font-semibold text-gray-700">
        Word Length Distributions
      </h2>
      <HelpButton info={info.wordLength} />
    </div>
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
