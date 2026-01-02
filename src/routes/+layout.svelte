<script lang="ts">
  import { page } from "$app/stores";
  import MenuBar from "$lib/MenuBar.svelte";
  import favicon from "$lib/assets/favicon.ico";
  import type { Snippet } from "svelte";

  interface LayoutData {
    subreddits: any[]; // replace `any` with a more specific type if you know the shape
  }

  let { children, data }: { children: Snippet; data: LayoutData } = $props();
  import "../app.css";
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<div class="flex flex-col min-h-screen bg-gray-50">
  {#if $page.route.id !== "/"}
    <MenuBar subreddits={data.subreddits} />
  {/if}

  <main class="grow">
    {@render children()}
  </main>

  <footer class="bg-slate-950 text-white p-8">
    <div class="max-w-6xl mx-auto text-center">
      <p>&copy; 2026 Subreddit Language Lab. All rights reserved.</p>
      <div class="flex justify-center space-x-6 mt-4">
        <a
          href="https://github.com/TrisCC/subreddit-language-lab"
          target="_blank"
          rel="noopener noreferrer"
          class="text-blue-300 hover:text-orange-400 transition-colors"
          >GitHub Repository</a
        >
        <a
          href="https://www.kaggle.com/datasets/sachinkanchan92/reddit-top-posts-50-subreddit-analysis-2011-2024"
          target="_blank"
          rel="noopener noreferrer"
          class="text-blue-300 hover:text-orange-400 transition-colors"
          >Original Dataset</a
        >
      </div>
    </div>
  </footer>
</div>
