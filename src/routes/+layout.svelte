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

  // If you're using a fallback (i.e. SPA mode) you don't need to prerender all
  // pages by setting this here, but should prerender as many as possible to
  // avoid large performance and SEO impacts
  export const prerender = true;
  export const trailingSlash = "always";
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

{#if $page.route.id !== "/"}
  <MenuBar subreddits={data.subreddits} />
{/if}

{@render children()}
