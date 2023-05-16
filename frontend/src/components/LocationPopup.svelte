<script>
  import { onMount } from 'svelte';
  import { setSelectedEpisodeById } from '../routes/store';

  export let coords;
  export let location;
  export let locationPopupIsShown;
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
    locationPopupIsShown = false;
    locationClicked = false;
  }

  function updatePostion(x, y) {
    if (!popup) return false;

    left = x - popup.offsetWidth / 2;

    if (left < 0) {
      left = 0;
    } else if (left > innerWidth - popup.offsetWidth) {
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
  class="border-gag-primary absolute z-20 m-1 w-64 rounded-md border bg-gray-300 bg-opacity-70 sm:w-96"
  style="left: {left}px; top: {top}px"
>
  <p class="py-2 text-center text-lg font-semibold">{location.name}</p>
  <ul
    class="scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary max-h-48 overflow-y-scroll px-2 pb-1"
  >
    {#each location.episodes as episode, id}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <li class="mb-2 flex cursor-pointer gap-1" on:click={setSelectedEpisodeById(episode.id)}>
        <span
          class="bg-gag-primary inline-block h-fit rounded-md px-2 py-1 text-xs font-bold text-white"
          >{episode.id}</span
        >{episode.title}
      </li>
    {/each}
  </ul>
</div>
