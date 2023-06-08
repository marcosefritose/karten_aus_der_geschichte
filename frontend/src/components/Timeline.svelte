<script>
  import { onMount } from 'svelte';
  import {
    selectedTime,
    setSelectedTime,
    setShowHistoricMaps,
    setSelectedEpisodeById,
    maps,
    episodes
  } from '../routes/store';

  function getEpisodesForPeriod(start, end) {
    let filteredEpisodes = $episodes.filter(
      (episode) => episode.story_time_start >= start && episode.story_time_start <= end
    );
    return filteredEpisodes;
  }

  const mapsWithDistance = maps.map((map, index) => {
    if (index === maps.length - 1) {
      let episodes = getEpisodesForPeriod(map.year, 2100);
      return { ...map, distance: 0, episodes };
    }

    let episodes = getEpisodesForPeriod(map.year, maps[index + 1].year);

    if (index === 0) return { ...map, distance: 0, episodes };
    const distance = map.year - maps[index - 1].year;

    return { ...map, distance, episodes };
  });

  mapsWithDistance.reverse();

  onMount(() => {
    selectedTime.subscribe((time) => {
      if (Object.keys(time).length === 0) return null;
      let listEntry = document.getElementById(time.year);

      setTimeout(() => {
        listEntry.scrollIntoView({
          behavior: 'smooth'
        });
      }, 1);
    });
  });
</script>

<div class="flex h-full flex-col bg-gray-200">
  <div class="p-2">
    <p class="text-lg font-bold">Zeitstrahl</p>
    <p>Karten angezeigt für das Jahr <span class="font-bold">{$selectedTime.year}</span></p>
  </div>
  <div
    class="scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary h-full flex-1 overflow-y-scroll"
  >
    <ol class="pt-1">
      <li class="mx-3 flex flex-col border-l-4 border-gray-300">
        <div class="mb-3 flex justify-between border-b border-dashed border-gray-300 pb-1">
          <img
            src="icons/triangle.svg"
            alt="Timeline Top"
            class="h-5 w-5 -translate-x-3 -translate-y-1"
          />
          <span>Anzahl Episoden</span>
        </div>
      </li>
      {#each mapsWithDistance as map}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <li
          id={map.year}
          class="mx-3 flex flex-col border-l-4 {$selectedTime.year == map.year
            ? 'border-gag-primary'
            : 'border-gray-300'}"
          style="padding-bottom: {Math.min(Math.floor(map.distance / 2), 70)}px;"
        >
          <div class="flex justify-between {$selectedTime.year == map.year ? 'font-bold' : ''}">
            <div class="flex">
              <span
                class="cursor-pointer {$selectedTime.year == map.year
                  ? 'bg-gag-primary'
                  : 'bg-gray-300'} inline-block h-5 w-5 -translate-x-3 rounded-full"
                on:click={() => {
                  setSelectedTime(map);
                  setShowHistoricMaps(true);
                }}
              />
              <span
                class="ml-3 cursor-pointer"
                on:click={() => {
                  setSelectedTime(map);
                  setShowHistoricMaps(true);
                }}>{map.year}</span
              >
            </div>
            <span
              class="cursor-pointer"
              on:click={() => {
                setSelectedTime(map);
                setShowHistoricMaps(true);
              }}>{map.episodes.length} Episoden</span
            >
          </div>
          {#if $selectedTime.year == map.year}
            <div class="flex flex-col gap-2 py-2 pl-2">
              {#each map.episodes as episode}
                <div
                  class="flex items-start gap-1"
                  on:click={() => setSelectedEpisodeById(episode.id)}
                >
                  <span
                    class="bg-gag-primary w-fit rounded-md px-2 py-1 text-xs font-bold text-white hover:cursor-pointer"
                    >{episode.key}</span
                  >
                  {episode.title}
                </div>
              {/each}
            </div>
          {/if}
        </li>
      {/each}
    </ol>
  </div>
</div>
