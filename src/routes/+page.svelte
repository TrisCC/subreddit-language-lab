<script>
  import { goto } from "$app/navigation";

  export let data;
  let subreddit = "";

  function handleSearch() {
    if (subreddit.trim()) {
      goto(`/subreddit/${subreddit.trim()}`);
    }
  }
</script>

<div
  class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-8"
>
  <div class="text-center">
    <h1 class="text-5xl font-bold text-gray-800">Subreddit Language Lab</h1>
    <p class="mt-2 text-lg text-gray-600">
      Analyze and explore the language of your favorite subreddits
    </p>
  </div>
  <form
    class="mt-8 flex w-full max-w-md"
    on:submit|preventDefault={handleSearch}
  >
    <input
      type="text"
      bind:value={subreddit}
      placeholder="Enter a subreddit name"
      class="flex-grow rounded-l-md border-2 border-r-0 border-gray-300 p-3 focus:border-blue-500 focus:outline-none"
    />
    <button
      type="submit"
      class="rounded-r-md border-2 border-l-0 border-blue-500 bg-blue-500 px-6 py-3 text-white hover:bg-blue-600 focus:outline-none"
    >
      Search
    </button>
  </form>

  {#if data.subreddits.length > 0}
    <div class="mt-12 w-full max-w-4xl">
      <h2 class="text-2xl font-bold text-gray-800">Available Subreddits</h2>
      <div class="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
        {#each data.subreddits as sub}
          <a
            href="/subreddit/{sub}"
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
