<script>
  import { goto } from "$app/navigation";
  import { base } from "$app/paths";

  export let data;
  let subreddit = "";
  /**
   * @type {string[]}
   */
  let suggestions = [];
  let showNoDataPopup = false;
  let sortMode = "alpha-asc"; // 'alpha-asc', 'alpha-desc', 'subs-desc', 'subs-asc'

  function handleInput() {
    if (subreddit.toLowerCase().startsWith("r/")) {
      subreddit = subreddit.substring(2);
    } else if (subreddit.toLowerCase().startsWith("/r/")) {
      subreddit = subreddit.substring(3);
    }
    updateSuggestions();
  }

  function updateSuggestions() {
    if (subreddit.trim() === "") {
      suggestions = [];
    } else {
      suggestions = data.subreddits.filter((s) =>
        s.toLowerCase().startsWith(subreddit.toLowerCase()),
      );
    }
  }

  function handleSearch() {
    const searchSub = subreddit.trim().toLowerCase();
    if (searchSub) {
      if (data.subreddits.map((s) => s.toLowerCase()).includes(searchSub)) {
        goto(`${base}/subreddit/${searchSub}`);
      } else {
        showNoDataPopup = true;
      }
    }
  }

  /**
   * @param {string} suggestion
   */
  function selectSuggestion(suggestion) {
    subreddit = suggestion;
    suggestions = [];
    handleSearch();
  }

  /**
   * @param {number} num
   */
  function formatSubscribers(num) {
    if (!num) return "";
    const millions = num / 1000000;
    return millions.toFixed(1) + " million";
  }

  const today = new Date();
  const start = new Date(today.getFullYear(), 0, 0);
  const oneDay = 1000 * 60 * 60 * 24;
  const diff = today.getTime() - start.getTime();
  const dayOfYear = Math.floor(diff / oneDay);

  const featuredSubredditName =
    data.subreddits[dayOfYear % data.subreddits.length];
  const featuredSubredditMeta = data.metadata[featuredSubredditName];
</script>

<svelte:head>
  <title>Subreddit Language Lab</title>
</svelte:head>

<!-- Hero Section -->
<div class="w-full bg-slate-950 py-12 px-8">
  <div class="max-w-4xl mx-auto text-center">
    <img
      src="{base}/logo.png"
      alt="Subreddit Language Lab logo"
      class="mx-auto mb-6 h-32 w-32"
    />
    <h1 class="text-6xl font-bold text-white mb-4">Subreddit Language Lab</h1>
    <p class="text-xl text-blue-100 mb-8">
      Analyze and explore the language of your favorite subreddits
    </p>
    <div class="max-w-md mx-auto">
      <form class="flex w-full" on:submit|preventDefault={handleSearch}>
        <input
          type="text"
          bind:value={subreddit}
          on:input={handleInput}
          placeholder="Enter a subreddit name"
          class="grow rounded-l-md border-2 border-r-0 border-gray-300 p-4 focus:border-orange-400 focus:outline-none bg-white text-gray-900 text-lg"
          autocomplete="off"
        />
        <button
          type="submit"
          class="rounded-r-md border-2 border-l-0 border-orange-700 bg-orange-600 px-8 py-4 text-white hover:bg-orange-700 focus:outline-none text-lg font-semibold"
        >
          Search
        </button>
      </form>
      {#if suggestions.length > 0}
        <ul
          class="absolute z-20 mt-2 w-full max-w-md mx-auto rounded-md border border-gray-300 bg-white shadow-lg"
        >
          {#each suggestions as suggestion}
            <li
              class="cursor-pointer p-3 hover:bg-gray-100"
              on:click={() => selectSuggestion(suggestion)}
              on:keydown={() => {}}
              role="option"
              aria-selected="false"
              tabindex="0"
            >
              {suggestion}
            </li>
          {/each}
        </ul>
      {/if}
    </div>
  </div>
</div>

<!-- Featured and About Section -->
<div class="bg-slate-200 py-6 px-6">
  <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-start">
    <!-- Featured Subreddit -->
    <div class="bg-white p-8 rounded-lg shadow-lg h-full flex flex-col">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Featured Subreddit</h2>
      {#if featuredSubredditMeta}
        <a
          href="{base}/subreddit/{featuredSubredditName}"
          class="block group grow flex-col"
        >
          <h3
            class="text-2xl font-semibold text-blue-600 group-hover:underline"
          >
            {featuredSubredditMeta.display_name}
          </h3>
          {#if featuredSubredditMeta.description}
            <p class="mt-2 text-gray-600 line-clamp-3 grow">
              {featuredSubredditMeta.description}
            </p>
          {/if}
          <div class="mt-auto">
            {#if featuredSubredditMeta.subscribers}
              <p class="mt-3 text-sm text-gray-500">
                {formatSubscribers(featuredSubredditMeta.subscribers)}
                subscribers
              </p>
            {/if}
            <div
              class="mt-4 text-orange-600 font-semibold group-hover:text-orange-700"
            >
              View Analysis &rarr;
            </div>
          </div>
        </a>
      {/if}
    </div>

    <!-- About the Project -->
    <div class="bg-white p-8 rounded-lg shadow-lg h-full">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">About the project</h2>
      <p class="text-gray-700 leading-relaxed">
        The Subreddit Language Lab is a project designed to provide linguistic
        insights into different Reddit communities. By analyzing post and
        comment data, we can uncover patterns in word frequency, grammatical
        structure, and more.
      </p>
      <p class="text-gray-700 leading-relaxed">
        The data for this project comes from the
        <a
          href="https://www.kaggle.com/datasets/sachinkanchan92/reddit-top-posts-50-subreddit-analysis-2011-2024"
          target="_blank"
          rel="noopener noreferrer"
          class="text-blue-600 hover:underline">Reddit Top Posts Dataset</a
        > on Kaggle. It features data from the 50 most popular subreddits with about
        50,000 records in total. These posts span from 2011 to 2024, providing a
        rich source of information for linguistic analysis.
      </p>
      <p class="mt-4 text-gray-700 leading-relaxed">
        Explore the available subreddits below to see what you can discover!
      </p>
    </div>
  </div>
</div>

<!-- Main Content -->
<div class="flex flex-col items-center justify-center bg-gray-50 px-8 py-8">
  {#if showNoDataPopup}
    <div
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="rounded-lg bg-white p-8 shadow-lg">
        <h2 class="text-2xl font-bold text-gray-800">Subreddit Not Found</h2>
        <p class="mt-4 text-gray-600">
          Sorry, we don't have any analysis data for the subreddit "{subreddit}".
        </p>
        <button
          class="mt-6 rounded-md bg-orange-500 px-4 py-2 text-white hover:bg-orange-600"
          on:click={() => (showNoDataPopup = false)}
        >
          Close
        </button>
      </div>
    </div>
  {/if}

  {#if data.subreddits.length > 0}
    <div class="w-full max-w-6xl">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-bold text-gray-800">Available Subreddits</h2>
        <select
          bind:value={sortMode}
          class="rounded-md bg-gray-200 px-4 py-2 text-sm hover:bg-gray-300"
        >
          <option value="alpha-asc">Alphabetical (A-Z)</option>
          <option value="alpha-desc">Alphabetical (Z-A)</option>
          <option value="subs-desc">Subscribers (High to Low)</option>
          <option value="subs-asc">Subscribers (Low to High)</option>
        </select>
      </div>
      <div
        class="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4"
      >
        {#each data.subreddits.slice().sort((a, b) => {
          if (sortMode === "alpha-asc") {
            return a.localeCompare(b);
          } else if (sortMode === "alpha-desc") {
            return b.localeCompare(a);
          } else {
            const aSubs = data.metadata[a]?.subscribers || 0;
            const bSubs = data.metadata[b]?.subscribers || 0;
            if (sortMode === "subs-desc") {
              return bSubs - aSubs;
            } else {
              // subs-asc
              return aSubs - bSubs;
            }
          }
        }) as sub}
          <a
            href="{base}/subreddit/{sub}"
            class="rounded-lg bg-white p-4 shadow-md transition-transform hover:scale-105 block"
          >
            <div class="font-semibold text-blue-600">
              {data.metadata[sub]?.display_name}
            </div>
            {#if data.metadata[sub]?.description}
              <p class="mt-2 text-sm text-gray-600 line-clamp-2">
                {data.metadata[sub].description}
              </p>
            {/if}
            {#if data.metadata[sub]?.subscribers}
              <p class="mt-1 text-xs text-gray-500">
                {formatSubscribers(data.metadata[sub].subscribers)} subscribers
              </p>
            {/if}
          </a>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .line-clamp-2,
  .line-clamp-3 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .line-clamp-2 {
    -webkit-line-clamp: 2;
    line-clamp: 2;
  }
  .line-clamp-3 {
    -webkit-line-clamp: 3;
    line-clamp: 3;
  }
</style>
