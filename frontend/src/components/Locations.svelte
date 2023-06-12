<script>
  import { onMount } from 'svelte';
  import { selectedLocations, locations, setSelectedLocations } from '../routes/store';

  let selectedLocationsNames = [];
  let sortedLocations = [];

  // Create selected locations string comma seperated
  $: selectedLocations.subscribe((locations) => {
    selectedLocationsNames = locations.map((location) => location.name);
  });

  onMount(() => {
    // Sort locations by number of episodes
    sortedLocations = [...$locations].sort((a, b) => {
      return b.episodes.length - a.episodes.length;
    });
  });
</script>

<div class="flex h-full flex-col bg-gray-200">
  <div class="p-2">
    <p class="text-lg font-bold">Schauplätze</p>
    <p>Hervorgehobene Orte: <span class="font-bold">{selectedLocationsNames.join(', ')}</span></p>
  </div>
  <div
    class="scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary h-full flex-1 overflow-y-scroll"
  >
    <ol class="pt-1">
      {#each sortedLocations as location}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <li
          id={location.id}
          class="mx-1 mb-1 flex flex-col"
          on:click={() => {
            setSelectedLocations([location]);
            console.log($selectedLocations);
          }}
        >
          <div class="flex flex-1 justify-between">
            <div class="flex">
              <span
                class="inline-block h-5 w-5 cursor-pointer rounded-full {selectedLocationsNames.includes(
                  location.name
                )
                  ? 'bg-gag-primary'
                  : 'bg-gray-300'}"
              />
              <span class="ml-3 cursor-pointer">{location.name}</span>
            </div>
            <span class="w-fit flex-none cursor-pointer px-1">
              {location.episodes.length} Episode{location.episodes.length > 1 ? 'n' : ''}
            </span>
          </div>
        </li>
      {/each}
    </ol>
  </div>
</div>
