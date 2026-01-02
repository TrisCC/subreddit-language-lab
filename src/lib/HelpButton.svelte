<script lang="ts">
    export let info: string;

    let showInfo = false;
</script>

<div class="relative inline-block ml-2">
    <button
        on:mouseenter={() => (showInfo = true)}
        on:mouseleave={() => (showInfo = false)}
        on:focus={() => (showInfo = true)}
        on:blur={() => (showInfo = false)}
        class="rounded-full w-5 h-5 bg-gray-600 text-white flex items-center justify-center hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-400"
        aria-label="More info"
    >
        <span class="material-symbols-outlined" style="font-size: 16px;">
            question_mark
        </span>
    </button>
    {#if showInfo}
        <div
            class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-2 bg-gray-700 text-white text-sm rounded-md shadow-lg z-10"
            role="tooltip"
        >
            {info}
        </div>
    {/if}
</div>
