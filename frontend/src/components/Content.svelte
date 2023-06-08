<script>
  import EpisodeList from '../components/EpisodeList.svelte';
  import Locations from '../components/Locations.svelte';
  import Search from '../components/Search.svelte';
  import { selectedTime, showHistoricMap } from '../routes/store';
  import Timeline from '../components/Timeline.svelte';

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
    class="flex h-full w-full flex-col opacity-90 transition md:h-5/6 md:flex-row"
  >
    <div
      class="pointer-events-auto flex h-8 w-fit flex-row justify-start bg-zinc-400 md:h-fit md:w-8 md:flex-col"
    >
      <div
        class="cursor-pointer px-2 md:px-0 md:py-2  {selectedContent == 'list'
          ? 'bg-zinc-200'
          : 'bg-zinc-400'}"
      >
        <img
          class="h-8 w-8"
          src="icons/list.svg"
          alt="Episode List Icon"
          on:click={() => (selectedContent = 'list')}
          on:keydown={() => (selectedContent = 'list')}
        />
      </div>
      <div
        class="cursor-pointer px-2 md:px-0 md:py-2 {selectedContent == 'timeline'
          ? 'bg-zinc-200'
          : 'bg-zinc-400'}"
      >
        <img
          class="h-8 w-8 p-1"
          src="icons/time-past.svg"
          alt="Episode List Icon"
          on:click={() => (selectedContent = 'timeline')}
          on:keydown={() => (selectedContent = 'timeline')}
        />
      </div>
      <div
        class="cursor-pointer px-2 md:px-0 md:py-2 {selectedContent == 'locations'
          ? 'bg-zinc-200'
          : 'bg-zinc-400'}"
      >
        <img
          class="h-8 w-8 p-1"
          src="icons/pinpoint.svg"
          alt="Location Pinpoint Icon"
          on:click={() => (selectedContent = 'locations')}
          on:keydown={() => (selectedContent = 'locations')}
        />
      </div>
      <label for="popup-selector" class="cursor-pointer border-x md:border-x-0 md:border-y">
        <input
          type="checkbox"
          id="popup-selector"
          class="peer sr-only"
          bind:checked={$showHistoricMap}
        />
        <div class="peer-checked:bg-gag-primary flex items-center px-1 md:h-fit md:w-8 md:flex-col">
          <img src="icons/map.svg" alt="Episode List Icon" class="h-8 w-8" />
          <span class="text-center text-xs font-bold">{$selectedTime.year}</span>
        </div>
      </label>
      <div class="px-1 md:px-0 md:py-1">
        <div class="transform cursor-pointer bg-gray-400 md:-rotate-90">
          <img
            class="h-8 w-8 {hideContent ? 'rotate-180 transform' : ''}"
            src="icons/double-arrow-down.svg"
            alt="Double Arrow Icon"
            on:click={() => {
              hideContent = !hideContent;
              console.log(contentBodyWidth);
            }}
          />
        </div>
      </div>
    </div>

    <div
      bind:offsetHeight={contentBodyHeight}
      bind:offsetWidth={contentBodyWidth}
      id="content-body"
      class="scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary pointer-events-auto h-full overflow-y-scroll bg-zinc-200 p-2 md:w-full"
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
