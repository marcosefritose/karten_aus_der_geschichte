<script>
  import { setEpisodes, episodes } from '../../store';

  export let data;
  setEpisodes(data.episodes);
</script>

<div class="p-10">
  <h1 class="text-3xl">{$episodes.length} Episoden</h1>

  <div class="bg-gag-light mt-3 flex flex-col flex-wrap rounded-lg">
    {#each $episodes as episode}
      <div class="flex p-4">
        <h2 class="text-lg font-semibold">
          {episode.title}
        </h2>
      </div>
    {/each}
  </div>
</div>
