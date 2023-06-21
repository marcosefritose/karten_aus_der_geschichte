<script>
  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  import { setSelectedLocations, selectedLocations, setSelectedEpisodeById } from '../routes/store';

  let selectedLocationsNames = [];

  let searchResults = {
    locations: [],
    areas: [],
    topics: []
  };
  let searchQuery = '';

  async function search() {
    console.log(`${VITE_FLASK_API_URL}/search/${searchQuery}`);
    const response = await fetch(`${VITE_FLASK_API_URL}/search/${searchQuery}`);
    const data = await response.json();

    searchResults = data;
    console.log(searchResults);
  }

  selectedLocations.subscribe((value) => {
    selectedLocationsNames = value.map((location) => location.name);
  });
</script>

<div class="flex h-full flex-col">
  <form method="get" on:submit|preventDefault={() => search()} class="w-full py-2 px-4">
    <input
      type="text"
      name="search"
      id="search"
      class="focus:ring-gag-primary h-8 w-full rounded-full border border-gray-300 bg-white px-4 focus:border-transparent focus:outline-none focus:ring-2"
      bind:value={searchQuery}
      placeholder="Suche nach Themen, Orten oder Inhalten"
    />
  </form>

  <div
    class="scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary h-full flex-1 overflow-y-scroll px-4"
  >
    <!-- Locations -->
    {#if searchResults.locations && searchResults.locations.length > 0}
      <h2 class="text-lg font-bold">Orte</h2>
      <ul class="mb-2">
        {#each searchResults.locations as location}
          <li
            class="flex cursor-pointer items-center py-1 {selectedLocationsNames.includes(
              location.name
            )
              ? 'font-bold'
              : ''}"
            on:click={() => {
              setSelectedLocations([location], true);
              setSelectedEpisodeById(null);
            }}
            on:keydown={() => {
              setSelectedLocations([location]);
              setSelectedEpisodeById(null);
            }}
          >
            <div
              class="{selectedLocationsNames.includes(location.name)
                ? 'bg-gag-primary'
                : 'bg-gray-600'} mr-1 h-2 w-2 rounded-full"
            />
            {location.name}
          </li>
        {/each}
      </ul>
    {/if}

    <!-- Episodes -->
    {#if searchResults.episodes && searchResults.episodes.length > 0}
      <h2 class="text-lg font-semibold">Episoden</h2>
      <ul>
        {#each searchResults.episodes as episode}
          <li
            class="flex cursor-pointer items-start gap-1 py-1"
            on:click={setSelectedEpisodeById(episode.id)}
            on:keydown={setSelectedEpisodeById(episode.id)}
          >
            <span
              class="bg-gag-primary w-16 flex-none rounded-md px-2 py-1 text-center text-xs font-bold text-white"
              >{episode.key}</span
            >
            {episode.title}
          </li>
        {/each}
      </ul>
    {/if}

    <!-- Topics -->
    {#if searchResults.topics && searchResults.topics.length > 0}
      <h2 class="text-lg font-semibold">Themen</h2>
      <ul class="mb-2">
        {#each searchResults.topics as topic}
          <li class="py-1">
            {topic.name}
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</div>
