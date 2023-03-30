<script>
  import { selectedTime, setSelectedTime, setShowHistoricMaps, maps } from './store';
</script>

<div class="flex h-full flex-col bg-gray-200">
  <div class="p-2">
    <p class="text-lg font-bold">Zeitstrahl</p>
    <p>Karten angezeigt für <span class="font-bold">{$selectedTime.year}</span></p>
  </div>
  <div
    class="scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary h-full flex-1 overflow-y-scroll"
  >
    <ol>
      {#each maps as map}
        <li
          class="flex items-center {$selectedTime.year == map.year ? 'font-bold' : ''}"
          on:click={() => {
            setSelectedTime(map);
            setShowHistoricMaps(true);
          }}
        >
          <div
            class="{$selectedTime.year == map.year
              ? 'bg-gag-primary'
              : 'bg-gray-300'} m-2 h-5 w-5 rounded-full"
          />
          {map.year}
        </li>
      {/each}
    </ol>
  </div>
</div>
