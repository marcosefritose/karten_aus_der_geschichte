<script>
  import Map from '../components/Map.svelte';
  import Content from '../components/Content.svelte';

  const confident = import.meta.env.VITE_CONFIDENT;
</script>

<main class="font-classicalHumanist">
  <div
    id="world-map-wrapper"
    class="pointer-events-auto absolute bottom-0  w-screen flex-auto overflow-clip"
  >
    <!-- Main World Map -->
    <Map />

    <!-- Logo -->
    <div
      class="border-gag-primary absolute top-0 flex w-32  border-b border-r border-dashed bg-slate-400 bg-opacity-80 lg:w-40"
    >
      <img src="/gag_logo.png" class="object-contain" alt="" />
    </div>

    <!-- Link -->
    {#if confident === 'true'}
      <div
        class="absolute right-0 top-0 p-2 text-sm md:left-0 md:bottom-0 md:right-auto md:top-auto"
      >
        made with <a href="/dashboard/episodes">☕</a> by
        <a
          href="https://me.marcose.eu"
          target="_blank"
          rel="noopener noreferrer"
          class="underline underline-offset-2">marc</a
        >
      </div>
    {/if}

    <!-- Side/Bottom Bar Content -->
    <Content />
  </div>
</main>
