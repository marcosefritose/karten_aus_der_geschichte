<script>
  import EpisodeList from './EpisodeList.svelte';
  import { setShowHistoricMaps, selectedEpisode, setPopupSelection } from './store';
  import Timeline from './Timeline.svelte';

  let popupSelectorChecked = false;
  let selectedContent = 'list';

  $: if (popupSelectorChecked) {
    setPopupSelection('area');
  } else {
    setPopupSelection('location');
  }

  // ToDo: Static url until images are served from flask server
  let imgUrl =
    'https://images.podigee-cdn.net/0x,sw_d9izO9QfY97alR2f13b7IrOVeXM5gFZOjetk-5sTg=/https://cdn.podigee.com/uploads/u32412/b610d282-8f99-4604-a16f-28ada94ab76a.jpg';

  selectedEpisode.subscribe((episode) => {
    if (Object.keys(episode).length === 0) return null;

    let listEntry = document.getElementById(episode.id);
    setTimeout(() => {
      listEntry.scrollIntoView({
        behavior: 'smooth'
      });
    }, 1);
  });
</script>

<div
  class="pointer-events-none absolute right-0 bottom-0 z-20 flex h-2/5 w-full items-center md:top-0 md:h-full md:w-1/3 xl:w-1/4 2xl:w-1/5"
>
  <div
    class="pointer-events-auto relative my-3 h-full w-full overflow-clip rounded-xl opacity-80 md:h-5/6"
  >
    <div class="aboslute select-none border-b border-gray-800 px-3">
      <div class="flex items-center gap-2">
        <img
          class="h-8 w-8 cursor-pointer rounded-t-md border border-b-0 border-gray-800 {selectedContent ==
          'list'
            ? 'bg-gag-primary'
            : 'bg-gray-300'}"
          src="list.svg"
          alt="Episode List Icon"
          on:click={() => (selectedContent = 'list')}
        />
        <img
          class="h-8 w-8 cursor-pointer rounded-t-md border border-b-0 border-gray-800 p-1 {selectedContent ==
          'timeline'
            ? 'bg-gag-primary'
            : 'bg-gray-300'}"
          src="time-past.svg"
          alt="Episode List Icon"
          on:click={() => (selectedContent = 'timeline')}
        />
        <label
          for="popup-selector"
          class="flex cursor-pointer gap-1 self-start rounded-full border border-gray-800 bg-gray-300"
        >
          <input
            type="checkbox"
            id="popup-selector"
            class="peer sr-only"
            bind:checked={popupSelectorChecked}
          />
          <span class="bg-gag-primary flex h-7 w-7 rounded-full p-1 peer-checked:bg-gray-300">
            <img src="location-pin.svg" alt="Episode List Icon" />
          </span>
          <span class="peer-checked:bg-gag-primary flex h-7 w-7 rounded-full bg-gray-300 p-1">
            <img src="map.svg" alt="Episode List Icon" />
          </span>
        </label>
      </div>
    </div>

    {#if selectedContent == 'list'}
      <EpisodeList />
    {:else if selectedContent == 'timeline'}
      <Timeline />
    {/if}
  </div>
</div>
