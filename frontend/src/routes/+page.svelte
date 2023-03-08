<script>
  import Map from './Map.svelte';
  import Content from './Content.svelte';

  const confident = import.meta.env.VITE_CONFIDENT;
</script>

<main class="">
  <div
    id="world-map-wrapper"
    class="pointer-events-auto absolute bottom-0  w-screen flex-auto overflow-clip"
  >
    <!-- Main World Map -->
    <Map />

    <!-- Logo -->
    <div
      class="border-gag-primary absolute top-0 flex w-32 rounded-br-md border-b border-r border-dashed bg-slate-400 bg-opacity-80 lg:w-40"
    >
      <img src="/gag_logo.png" class="object-contain" alt="" />
    </div>

    <!-- Link -->
    {#if confident === 'true'}
      <div class="absolute right-0 top-0 p-2 text-sm">
        Made with ☕ by <a
          href="https://me.marcose.eu"
          target="_blank"
          rel="noopener noreferrer"
          class="underline underline-offset-2">marcose</a
        >.
      </div>
    {/if}

    <!-- Side/Bottom Bar Content -->
    <Content />
  </div>
</main>
