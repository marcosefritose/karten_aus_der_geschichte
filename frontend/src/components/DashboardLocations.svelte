<script>
  import { onMount } from 'svelte';
  import { locations } from '../routes/store';

  onMount(() => {
    console.log($locations[12]);
  });
</script>

<div class="p-10">
  <h1 class="text-3xl">{$locations.length} Orte</h1>

  <div class="bg-gag-light mt-3 flex flex-col flex-wrap rounded-lg">
    {#each $locations as location}
      <div class="flex p-4">
        <h2 class="text-lg font-bold">
          {location.name}
        </h2>
        <span class="bg-gag-primary text-gag-white ml-2 rounded-full py-1 px-2 text-sm"
          >{location.episodes.length}</span
        >
      </div>
    {/each}
  </div>
</div>
