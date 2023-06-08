<script>
  import { episodes, setSelectedEpisodeById, selectedEpisode } from '../routes/store';
  import { onMount } from 'svelte';

  const apiUrl = import.meta.env.VITE_FLASK_API_URL;

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
        src={episode.thumbnail !== 'NaN' ? apiUrl + episode.thumbnail : 'default_thumbnail.jpeg'}
        class="h-12 w-12 rounded-sm border border-gray-400 hover:cursor-pointer md:h-16 md:w-16"
        alt="Thumbnail Picture Episode {episode.id}"
        loading="lazy"
        on:click={setSelectedEpisodeById(episode.id)}
      />
      <div class="flex-row">
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <span
          class="bg-gag-primary rounded-md px-2 py-1 text-sm font-bold text-white hover:cursor-pointer"
          on:click={setSelectedEpisodeById(episode.id)}>{episode.key}</span
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
        <!-- Time & Location Badges -->
        <div class="location-tabs flex flex-wrap gap-2 py-1 text-sm">
          <!-- Time Badge -->
          <span class="rounded-lg border border-gray-600 bg-white py-1 px-2 text-gray-600">
            {episode.story_time_start + ' - ' + episode.story_time_end}
          </span>
          <!-- Location Badges -->
          {#each episode.locations as loc}
            {#if loc.status == 'active'}
              <span class="border-gag-primary text-gag-primary rounded-lg border bg-white py-1 px-2"
                >{loc.name}</span
              >
            {/if}
          {/each}
        </div>

        <!-- Topic Badges -->
        <div class="topic-tabs flex flex-wrap gap-2 py-1 text-sm">
          {#each episode.topics_association as topic}
            {#if topic.status == 'active'}
              <span class="rounded-lg border border-slate-500 bg-white py-1 px-2 text-slate-500"
                >{topic.topic_name}</span
              >
            {/if}
          {/each}
        </div>

        <!-- Summary -->
        <span class="block pt-1 text-xs font-semibold">Beschreibung</span>
        <p class="text-small">
          {episode.summary}
        </p>

        <!-- Date -->
        <span class="block pt-1 text-xs font-semibold"
          >Veröffentlicht am {new Date(episode.published).toLocaleDateString('de-DE')}</span
        >
        <!-- Link -->
        <span class="block py-1 text-sm font-semibold underline underline-offset-2"
          ><a href={episode.link} target="_blank" rel="noopener noreferrer">Zur Folge</a></span
        >
      </div>
    {/if}
  {/each}
{/if}
