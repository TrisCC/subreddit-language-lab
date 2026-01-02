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
</script>

<svelte:head>
  <title>Subreddit Language Lab</title>
</svelte:head>

<!-- Hero Section -->
<div class="w-full bg-slate-950 py-16 px-8">
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

<!-- Main Content -->
<div class="flex flex-col items-center justify-center bg-gray-50 px-8 py-16">
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
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
