<script>
  import { goto } from "$app/navigation";

  let subreddit = "";

  function handleSearch() {
    if (subreddit.trim()) {
      goto(`/subreddit/${subreddit.trim()}`);
    }
  }
</script>

<div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
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
</div>

<style>
  /* You can write your custom CSS here */
</style>
