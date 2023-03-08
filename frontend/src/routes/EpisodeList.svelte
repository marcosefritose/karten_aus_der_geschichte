<script>
  import { episodes, setSelectedEpisodeById, selectedEpisode, setPopupSelection } from './store';

  let popupSelectorChecked = false;

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
  id="list"
  class="pointer-events-none absolute right-0 bottom-0 z-20 flex h-2/5 w-full items-center md:top-0 md:h-full md:w-1/3 xl:w-1/4 2xl:w-1/5"
>
  <div
    class="scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary pointer-events-auto my-3 h-full overflow-y-scroll  rounded-xl bg-gray-200 p-3 opacity-80 md:h-5/6"
  >
    <div class="select-none border-b border-gray-800">
      <div class="flex items-center gap-2">
        <img
          class="h-8 w-8 rounded-t-md border border-b-0 border-gray-800"
          src="list.svg"
          alt="Episode List Icon"
        />
        <img
          class="h-8 w-8 rounded-t-md border border-b-0 border-gray-800 p-1"
          src="time-past.svg"
          alt="Episode List Icon"
        />
        <label
          for="popup-selector"
          class="border-gag-primary flex cursor-pointer gap-1 rounded-full border bg-gray-300"
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

    {#if $episodes}
      {#each $episodes as episode (episode.id)}
        <div id={episode.id} class="flex gap-2 border py-1">
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <img
            src={imgUrl}
            class="h-12 w-12 rounded-sm border border-gray-400 hover:cursor-pointer md:h-16 md:w-16"
            alt="Thumbnail Picture Episode {episode.id}"
            on:click={setSelectedEpisodeById(episode.id)}
          />
          <div class="flex-row">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <span
              class="bg-gag-primary rounded-md px-2 py-1 text-sm font-bold text-white hover:cursor-pointer"
              on:click={setSelectedEpisodeById(episode.id)}>{episode.id}</span
            >

            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div class="w-full">
              <span
                class="text-small mb-1 inline-block font-semibold hover:cursor-pointer"
                on:click={setSelectedEpisodeById(episode.id)}>{episode.title}</span
              ><br />
            </div>
          </div>
        </div>
        {#if $selectedEpisode}
          <div class="{$selectedEpisode.id === episode.id ? '' : 'hidden'} px-3">
            <div class="location-tabs flex flex-wrap gap-2 text-sm">
              {#each episode.locations as loc}
                <span
                  class="border-gag-primary text-gag-primary rounded-lg border bg-white py-1 px-2"
                  >{loc.name}</span
                >
              {/each}
            </div>
            <!-- Date -->
            <span class="block pt-1 text-xs font-semibold"
              >Veröffentlicht am {new Date(episode.published).toLocaleDateString('de-DE')}</span
            >
            <!-- Link -->
            <span class="block py-1 text-sm font-semibold underline underline-offset-2"
              ><a href={episode.link} target="_blank" rel="noopener noreferrer">Zur Folge</a></span
            >

            <!-- Summary -->
            <p class="text-small">
              {episode.summary}
            </p>
          </div>
        {/if}
      {/each}
    {/if}
  </div>
</div>
