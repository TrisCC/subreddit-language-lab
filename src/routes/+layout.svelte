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

{#if $page.route.id !== "/"}
  <MenuBar subreddits={data.subreddits} />
{/if}

{@render children()}
