<script>
  import DashboardTopics from '../../components/DashboardTopics.svelte';
  import DashboardLocations from '../../components/DashboardLocations.svelte';
  import DashboardEpisodes from '../../components/DashboardEpisodes.svelte';

  let content = 'locations';
</script>

<div class="flex">
  <nav class="bg-gag-light flex h-screen w-1/6 flex-col gap-2">
    <img src="/gag_logo.png" class="mx-auto w-56 object-contain" alt="" />
    <div
      class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {content == 'episodes'
        ? 'bg-gag-white'
        : 'bg-light'}"
      on:click={() => (content = 'episodes')}
      on:keydown={() => (content = 'episodes')}
    >
      <img class="h-8 w-8 rounded-t-md" src="icons/list.svg" alt="Episode List Icon" />
      <span class="px-2">Episoden</span>
    </div>
    <div
      class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {content == 'locations'
        ? 'bg-gag-white'
        : 'bg-light'}"
      on:click={() => (content = 'locations')}
      on:keydown={() => (content = 'locations')}
    >
      <img class="h-8 w-8 rounded-t-md" src="icons/location.svg" alt="Location List Icon" />
      <span class="px-2">Orte</span>
    </div>
    <div
      class="mx-4 flex cursor-pointer items-center rounded-lg p-2 {content == 'topics'
        ? 'bg-gag-white'
        : 'bg-light'}"
      on:click={() => (content = 'topics')}
      on:keydown={() => (content = 'topics')}
    >
      <img class="h-8 w-8 rounded-t-md" src="icons/topic.svg" alt="Episode Topics Icon" />
      <span class="px-2">Themen</span>
    </div>
  </nav>
  <main class="bg-gag-white h-screen w-5/6">
    {#if content == 'episodes'}
      <DashboardEpisodes />
    {:else if content == 'locations'}
      <DashboardLocations />
    {:else if content == 'topics'}
      <DashboardTopics />
    {/if}
  </main>
</div>
