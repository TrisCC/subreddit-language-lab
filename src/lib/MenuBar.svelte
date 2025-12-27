<script lang="ts">
  import { goto } from "$app/navigation";
  import { base } from "$app/paths";

  export let subreddits: string[] = [];
  let subreddit = "";
  let suggestions: string[] = [];
  let showNoDataPopup = false;
  let activeSuggestion = -1;

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
      suggestions = subreddits.filter((s) =>
        s.toLowerCase().startsWith(subreddit.toLowerCase()),
      );
    }
    activeSuggestion = -1;
  }

  function handleSearch() {
    const subToSearch =
      activeSuggestion > -1 ? suggestions[activeSuggestion] : subreddit;
    const searchSub = subToSearch
      ? String(subToSearch).trim().toLowerCase()
      : "";

    if (searchSub) {
      if (subreddits.map((s) => s.toLowerCase()).includes(searchSub)) {
        goto(`${base}/subreddit/${searchSub}`);
        subreddit = "";
        suggestions = [];
        activeSuggestion = -1;
      } else {
        showNoDataPopup = true;
      }
    }
  }

  function selectSuggestion(suggestion: string) {
    subreddit = suggestion;
    suggestions = [];
    activeSuggestion = -1;
    handleSearch();
  }

  function handleKeydown(event: KeyboardEvent) {
    if (suggestions.length === 0) return;

    if (event.key === "ArrowDown") {
      event.preventDefault();
      activeSuggestion = (activeSuggestion + 1) % suggestions.length;
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      activeSuggestion =
        (activeSuggestion - 1 + suggestions.length) % suggestions.length;
    } else if (event.key === "Enter") {
      event.preventDefault();
      handleSearch();
    }
  }
</script>

<header class="bg-slate-950 text-white p-4 shadow-md sticky top-0 z-50">
  <div class="container mx-auto flex justify-between items-center">
    <a href="{base}/" class="text-2xl font-bold hover:text-gray-300">
      <img src="{base}/logo.png" alt="Logo" class="h-8 w-8 object-cover" />
    </a>
    <div class="relative w-full max-w-xs">
      <form class="flex w-full" on:submit|preventDefault={handleSearch}>
        <input
          type="text"
          bind:value={subreddit}
          on:input={handleInput}
          on:keydown={handleKeydown}
          placeholder="Search subreddit..."
          class="grow rounded-l-md border-gray-300 bg-white p-2 text-gray-900 focus:outline-none"
          autocomplete="off"
        />
        <button
          type="submit"
          class="rounded-r-md bg-orange-600 border-orange-700 px-4 py-2 hover:bg-orange-700 focus:outline-none"
        >
          Search
        </button>
      </form>
      {#if suggestions.length > 0}
        <ul
          class="absolute z-10 mt-1 w-full rounded-md border border-gray-600 bg-gray-700 shadow-lg"
        >
          {#each suggestions as suggestion, i}
            <li
              class="cursor-pointer p-2 {activeSuggestion === i
                ? 'bg-gray-600'
                : ''}"
              on:click={() => selectSuggestion(suggestion)}
              on:keydown={() => {}}
              role="option"
              aria-selected={activeSuggestion === i}
              tabindex="0"
            >
              {suggestion}
            </li>
          {/each}
        </ul>
      {/if}
    </div>
  </div>
</header>

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
