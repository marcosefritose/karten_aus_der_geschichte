<script>
  import EpisodeList from './EpisodeList.svelte';
  import Locations from './Locations.svelte';
  import Search from './Search.svelte';
  import { setShowHistoricMaps, selectedEpisode, showHistoricMap } from './store';
  import Timeline from './Timeline.svelte';

  let popupSelectorChecked = false;
  let selectedContent = 'list';
  let hideContent = false;
  let contentWrapper = null;
  let contentBodyHeight = 0;
  let contentBodyWidth = 0;
  let windowWidth;
</script>

<svelte:window bind:innerWidth={windowWidth} />
<div
  class="pointer-events-none absolute right-0 bottom-0 z-20 flex h-2/5 w-full items-center md:top-0 md:h-full md:w-1/3 xl:w-1/4 2xl:w-1/5"
>
  <div
    bind:this={contentWrapper}
    style={hideContent
      ? windowWidth < 768
        ? `transform: translateY(${contentBodyHeight}px)`
        : `transform: translateX(${contentBodyWidth}px)`
      : ''}
    class="pointer-events-none my-3 flex h-full w-full flex-col opacity-80 transition md:h-5/6"
  >
    <div class="relative select-none px-3">
      <div class="flex justify-between">
        <div
          style={windowWidth > 768 ? `transform: translate(-135%, 101%) rotate(-90deg);` : ''}
          class="visible cursor-pointer rounded-t-md border border-b-0 border-gray-800 bg-gray-400"
        >
          <img
            class="pointer-events-auto h-8 w-8"
            style={hideContent ? 'transform: rotate(180deg)' : ''}
            src="icons/double-arrow-down.svg"
            alt="Double Arrow Icon"
            on:click={() => (hideContent = !hideContent)}
          />
        </div>
        <div class="pointer-events-auto flex items-center justify-end gap-2">
          <label
            for="popup-selector"
            class="flex cursor-pointer gap-1 self-start rounded-full border border-gray-800 bg-gray-300"
          >
            <input
              type="checkbox"
              id="popup-selector"
              class="peer sr-only"
              bind:checked={$showHistoricMap}
            />
            <span class="bg-gag-primary flex h-7 w-7 rounded-full p-1 peer-checked:bg-gray-300">
              <img src="icons/location-pin.svg" alt="Episode List Icon" />
            </span>
            <span class="peer-checked:bg-gag-primary flex h-7 w-7 rounded-full bg-gray-300 p-1">
              <img src="icons/map.svg" alt="Episode List Icon" />
            </span>
          </label>
          <img
            class="h-8 w-8 cursor-pointer rounded-t-md border border-b-0 border-gray-800 {selectedContent ==
            'list'
              ? 'bg-gag-primary'
              : 'bg-gray-300'}"
            src="icons/list.svg"
            alt="Episode List Icon"
            on:click={() => (selectedContent = 'list')}
            on:keydown={() => (selectedContent = 'list')}
          />
          <img
            class="h-8 w-8 cursor-pointer rounded-t-md border border-b-0 border-gray-800 p-1 {selectedContent ==
            'timeline'
              ? 'bg-gag-primary'
              : 'bg-gray-300'}"
            src="icons/time-past.svg"
            alt="Episode List Icon"
            on:click={() => (selectedContent = 'timeline')}
            on:keydown={() => (selectedContent = 'timeline')}
          />
          <img
            class="h-8 w-8 cursor-pointer rounded-t-md border border-b-0 border-gray-800 p-1 {selectedContent ==
            'locations'
              ? 'bg-gag-primary'
              : 'bg-gray-300'}"
            src="icons/pinpoint.svg"
            alt="Location Pinpoint Icon"
            on:click={() => (selectedContent = 'locations')}
            on:keydown={() => (selectedContent = 'locations')}
          />
          <img
            class="h-8 w-8 cursor-pointer rounded-t-md border border-b-0 border-gray-800 {selectedContent ==
            'search'
              ? 'bg-gag-primary'
              : 'bg-gray-300'}"
            src="icons/search.svg"
            alt="Search Icon"
            on:click={() => (selectedContent = 'search')}
            on:keydown={() => (selectedContent = 'search')}
          />
        </div>
      </div>
    </div>

    <div
      bind:clientHeight={contentBodyHeight}
      bind:clientWidth={contentBodyWidth}
      id="content-body"
      class="scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary pointer-events-auto overflow-y-scroll border-t border-gray-800 bg-gray-200 p-2"
    >
      {#if selectedContent == 'list'}
        <EpisodeList />
      {:else if selectedContent == 'timeline'}
        <Timeline />
      {:else if selectedContent == 'locations'}
        <Locations />
      {:else if selectedContent == 'search'}
        <Search />
      {/if}
    </div>
  </div>
</div>
