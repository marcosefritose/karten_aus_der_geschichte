<script>
  import { episodes, setSelectedEpisodeById, selectedEpisode } from './store';

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
    class="pointer-events-auto my-3 h-full overflow-y-scroll rounded-xl bg-gray-200 p-3  opacity-70 scrollbar-thin scrollbar-track-gray-400 scrollbar-thumb-gag-primary md:h-5/6"
  >
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
              class="rounded-md bg-gag-primary px-2 py-1 text-sm font-bold text-white hover:cursor-pointer"
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
                  class="rounded-lg border border-gag-primary bg-white py-1 px-2 text-gag-primary"
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
