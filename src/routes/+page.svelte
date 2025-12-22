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
</script>

<svelte:head>
  <title>Subreddit Language Lab</title>
</svelte:head>

<div
  class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-8"
>
  <div class="text-center">
    <img
      src="/logo.png"
      alt="Subreddit Language Lab logo"
      class="mx-auto mb-4 h-24 w-24"
    />
    <h1 class="text-5xl font-bold text-gray-800">Subreddit Language Lab</h1>
    <p class="mt-2 text-lg text-gray-600">
      Analyze and explore the language of your favorite subreddits
    </p>
  </div>
  <div class="relative w-full max-w-md">
    <form class="mt-8 flex w-full" on:submit|preventDefault={handleSearch}>
      <input
        type="text"
        bind:value={subreddit}
        on:input={updateSuggestions}
        placeholder="Enter a subreddit name"
        class="grow rounded-l-md border-2 border-r-0 border-gray-300 p-3 focus:border-blue-500 focus:outline-none"
        autocomplete="off"
      />
      <button
        type="submit"
        class="rounded-r-md border-2 border-l-0 border-blue-500 bg-blue-500 px-6 py-3 text-white hover:bg-blue-600 focus:outline-none"
      >
        Search
      </button>
    </form>
    {#if suggestions.length > 0}
      <ul
        class="absolute z-10 mt-1 w-full rounded-md border border-gray-300 bg-white shadow-lg"
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
          class="mt-6 rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
          on:click={() => (showNoDataPopup = false)}
        >
          Close
        </button>
      </div>
    </div>
  {/if}

  {#if data.subreddits.length > 0}
    <div class="mt-12 w-full max-w-4xl">
      <h2 class="text-2xl font-bold text-gray-800">Available Subreddits</h2>
      <div class="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
        {#each data.subreddits as sub}
          <a
            href="{base}/subreddit/{sub}"
            class="rounded-lg bg-white p-4 text-center shadow-md transition-transform hover:scale-105"
          >
            <span class="font-semibold text-blue-600">/r/{sub}</span>
          </a>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  /* You can write your custom CSS here */
</style>
