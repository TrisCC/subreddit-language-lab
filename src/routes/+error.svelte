<script>
  import { page } from "$app/stores";
</script>

<div
  class="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-center"
>
  <h1 class="text-9xl font-bold text-blue-500">{$page.status}</h1>
  <p class="mt-4 text-2xl font-semibold text-gray-700">
    {$page.error?.message}
  </p>
  <a
    href="/"
    class="mt-8 rounded-md bg-blue-500 px-6 py-3 text-white hover:bg-blue-600"
  >
    Go Home
  </a>
</div>
