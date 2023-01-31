<script>
  import { onMount } from 'svelte';
  import { setSelectedEpisodeById } from './store';

  export let coords;
  export let location;
  export let showPopup;
  export let locationClicked;

  let popup;
  let left = 0;
  let top = 0;

  $: ({ x, y } = coords);
  $: updatePostion(x, y);

  function clickOutside(node) {
    const handleClick = (event) => {
      if (node && !node.contains(event.target) && !event.defaultPrevented) {
        node.dispatchEvent(new CustomEvent('click_outside', node));
      }
    };

    document.addEventListener('click', handleClick, true);

    return {
      destroy() {
        document.removeEventListener('click', handleClick, true);
      }
    };
  }

  function disablePopup() {
    showPopup = false;
    locationClicked = false;
  }

  function updatePostion(x, y) {
    if (!popup) return false;

    left = x - popup.offsetWidth / 2;

    if (left < 0) {
      left = 0;
    } else if (left > innerWidth - popup.offsetWidth) {
      console.log('shrink');
      left = innerWidth - popup.offsetWidth;
    }

    if (innerHeight / 2 < y + popup.offsetHeight) {
      top = y - popup.offsetHeight - 15;
    } else {
      top = y + 15;
    }
  }

  onMount(() => {
    updatePostion(x, y);
  });
</script>

<div
  bind:this={popup}
  use:clickOutside
  on:click_outside={disablePopup}
  class="absolute z-20 m-1 w-64 rounded-md border border-gag-primary bg-gray-300 bg-opacity-70 sm:w-96"
  style="left: {left}px; top: {top}px"
>
  <p class="py-2 text-center text-lg font-semibold">{location.name}</p>
  <ul
    class="max-h-48 overflow-y-scroll px-2 pb-1 scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary"
  >
    {#each location.episodes as episode, id}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <li class="mb-2 flex cursor-pointer gap-1" on:click={setSelectedEpisodeById(episode.id)}>
        <span
          class="inline-block h-fit rounded-md bg-gag-primary px-2 py-1 text-xs font-bold text-white"
          >{episode.id}</span
        >{episode.title}
      </li>
    {/each}
  </ul>
</div>
