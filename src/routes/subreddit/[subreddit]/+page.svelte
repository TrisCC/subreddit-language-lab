<script>
  export let data;
</script>

<div class="container mx-auto p-8">
  <h1 class="text-4xl font-bold text-gray-800">
    Analysis for /r/{data.subreddit}
  </h1>

  <div class="mt-8 grid grid-cols-1 gap-8 md:grid-cols-2">
    <!-- POS Ratios -->
    <div class="rounded-lg bg-white p-6 shadow-md">
      <h2 class="text-2xl font-semibold text-gray-700">
        Grammatical Category Ratios
      </h2>
      <ul class="mt-4 space-y-2">
        {#each Object.entries(data.analysis.pos_ratios) as [pos, ratio]}
          <li class="flex justify-between">
            <span class="font-medium text-gray-600">{pos}</span>
            <span class="text-gray-800">{(ratio * 100).toFixed(2)}%</span>
          </li>
        {/each}
      </ul>
    </div>

    <!-- Most Common Words -->
    <div class="rounded-lg bg-white p-6 shadow-md">
      <h2 class="text-2xl font-semibold text-gray-700">Most Common Words</h2>
      <ul class="mt-4 space-y-2">
        {#each Object.entries(data.analysis.most_common_words) as [word, count]}
          <li class="flex justify-between">
            <span class="font-medium text-gray-600">{word}</span>
            <span class="text-gray-800">{count}</span>
          </li>
        {/each}
      </ul>
    </div>
  </div>

  <!-- Categorized Common Words -->
  <div class="mt-8 rounded-lg bg-white p-6 shadow-md">
    <h2 class="text-2xl font-semibold text-gray-700">
      Most Common Words by Category
    </h2>
    <div class="mt-4 grid grid-cols-1 gap-8 sm:grid-cols-2 md:grid-cols-4">
      <div>
        <h3 class="text-xl font-semibold text-gray-600">Nouns</h3>
        <ul class="mt-2 space-y-1">
          {#each Object.entries(data.analysis.most_common_nouns) as [word, count]}
            <li class="flex justify-between">
              <span class="text-gray-700">{word}</span>
              <span class="font-medium text-gray-800">{count}</span>
            </li>
          {/each}
        </ul>
      </div>
      <div>
        <h3 class="text-xl font-semibold text-gray-600">Verbs</h3>
        <ul class="mt-2 space-y-1">
          {#each Object.entries(data.analysis.most_common_verbs) as [word, count]}
            <li class="flex justify-between">
              <span class="text-gray-700">{word}</span>
              <span class="font-medium text-gray-800">{count}</span>
            </li>
          {/each}
        </ul>
      </div>
      <div>
        <h3 class="text-xl font-semibold text-gray-600">Adjectives</h3>
        <ul class="mt-2 space-y-1">
          {#each Object.entries(data.analysis.most_common_adjectives) as [word, count]}
            <li class="flex justify-between">
              <span class="text-gray-700">{word}</span>
              <span class="font-medium text-gray-800">{count}</span>
            </li>
          {/each}
        </ul>
      </div>
      <div>
        <h3 class="text-xl font-semibold text-gray-600">Adverbs</h3>
        <ul class="mt-2 space-y-1">
          {#each Object.entries(data.analysis.most_common_adverbs) as [word, count]}
            <li class="flex justify-between">
              <span class="text-gray-700">{word}</span>
              <span class="font-medium text-gray-800">{count}</span>
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </div>

  <!-- N-grams and Word Lengths -->
  <div class="mt-8 grid grid-cols-1 gap-8 md:grid-cols-2">
    <!-- N-grams -->
    <div class="rounded-lg bg-white p-6 shadow-md">
      <h2 class="text-2xl font-semibold text-gray-700">Most Common N-grams</h2>
      <div class="mt-4 grid grid-cols-1 gap-8 sm:grid-cols-2">
        <div>
          <h3 class="text-xl font-semibold text-gray-600">Bigrams</h3>
          <ul class="mt-2 space-y-1">
            {#each Object.entries(data.analysis.most_common_bigrams) as [ngram, count]}
              <li class="flex justify-between">
                <span class="text-gray-700">{ngram}</span>
                <span class="font-medium text-gray-800">{count}</span>
              </li>
            {/each}
          </ul>
        </div>
        <div>
          <h3 class="text-xl font-semibold text-gray-600">Trigrams</h3>
          <ul class="mt-2 space-y-1">
            {#each Object.entries(data.analysis.most_common_trigrams) as [ngram, count]}
              <li class="flex justify-between">
                <span class="text-gray-700">{ngram}</span>
                <span class="font-medium text-gray-800">{count}</span>
              </li>
            {/each}
          </ul>
        </div>
      </div>
    </div>

    <!-- Word Length Distributions -->
    <div class="rounded-lg bg-white p-6 shadow-md">
      <h2 class="text-2xl font-semibold text-gray-700">
        Word Length Distributions
      </h2>
      <!-- This part can be visualized with a chart library -->
      <div class="mt-4 text-gray-600">
        Visualization of word length distributions will be implemented here.
      </div>
    </div>
  </div>
</div>
