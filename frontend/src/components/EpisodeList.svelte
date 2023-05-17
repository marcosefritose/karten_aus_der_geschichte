<script>
  import { episodes, setSelectedEpisodeById, selectedEpisode } from '../routes/store';
  import { onMount } from 'svelte';

  const apiUrl = import.meta.env.VITE_FLASK_API_URL;

  // ToDo: Static url until images are served from flask server
  let imgUrl =
    'https://images.podigee-cdn.net/0x,sw_d9izO9QfY97alR2f13b7IrOVeXM5gFZOjetk-5sTg=/https://cdn.podigee.com/uploads/u32412/b610d282-8f99-4604-a16f-28ada94ab76a.jpg';

  onMount(() => {
    selectedEpisode.subscribe((episode) => {
      if (Object.keys(episode).length === 0) return null;
      let listEntry = document.getElementById(episode.id);

      setTimeout(() => {
        listEntry.scrollIntoView({
          behavior: 'smooth'
        });
      }, 1);
    });
  });
</script>

{#if $episodes}
  {#each $episodes as episode (episode.id)}
    <div id={episode.id} class="flex gap-2 border py-1">
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <img
        src={episode.thumbnail !== 'NaN' ? apiUrl + episode.thumbnail : imgUrl}
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
            class="text-small my-1 inline-block font-semibold hover:cursor-pointer"
            on:click={setSelectedEpisodeById(episode.id)}>{episode.title}</span
          ><br />
        </div>
      </div>
    </div>
    {#if $selectedEpisode}
      <div class="{$selectedEpisode.id === episode.id ? '' : 'hidden'} px-3">
        <!-- Location Badges -->
        <div class="location-tabs flex flex-wrap gap-2 text-sm">
          {#each episode.locations as loc}
            {#if loc.status == 'active'}
              <span class="border-gag-primary text-gag-primary rounded-lg border bg-white py-1 px-2"
                >{loc.name}</span
              >
            {/if}
          {/each}
          <!-- Time Badge -->
          <span class="rounded-lg border border-gray-600 bg-white py-1 px-2 text-gray-600">
            {episode.story_time_start + ' - ' + episode.story_time_end}
          </span>
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
