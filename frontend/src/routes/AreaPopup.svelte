<script>
  import { onMount } from 'svelte';

  export let coords;
  export let area;

  let popup;
  let left = 0;
  let top = 0;

  $: ({ x, y } = coords);
  $: updatePostion(x, y);

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
  class="border-gag-primary absolute z-20 m-1 w-64 rounded-md border bg-gray-300 bg-opacity-70 sm:w-96"
  style="left: {left}px; top: {top}px"
>
  <p class="py-2 text-center text-lg font-semibold">{area}</p>
</div>
