<script>
  import DashboardEpisodeListEntry from '../../../components/DashboardEpisodeListEntry.svelte';
  import { setEpisodes, episodes } from '../../store';

  export let data;

  let selectedEpisodeId = null;
  let selectedEpisodeData = null;

  setEpisodes(data.episodes);

  async function loadEpisodeData(id) {
    const response = await fetch(`http://localhost:5001/episodes/${id}`);
    const data = await response.json();

    selectedEpisodeId = id;
    selectedEpisodeData = data;
    console.log(data);
  }
</script>

<div class="bg-gag-white w-full overflow-y-scroll p-10">
  <h1 class="text-3xl">{$episodes.length} Episoden</h1>

  <div class="bg-gag-light mt-3 flex flex-col flex-wrap rounded-lg">
    <table>
      <thead class="border-b font-medium">
        <tr>
          <td class="py-3 px-2">ID</td>
          <td class="py-3 px-2">Titel</td>
          <td class="py-3 px-2">Status</td>
          <td class="py-3 px-2">Aktion</td>
        </tr>
      </thead>
      <tbody class="bg-white">
        {#each $episodes as episode}
          <tr class="border-b">
            <td class="py-3 px-2">{episode.id}</td>
            <td class="py-3 px-2">{episode.title}</td>
            <!-- Todo: Add Status to Episode API -->
            <!-- <td class="py-3 px-2">{episode.status}</td> -->
            <td class="py-3 px-2">
              <span class="bg-active-light rounded-lg px-2 py-1">Aktiv</span>
            </td>
            <td class="py-3 px-2">
              <button on:click={() => loadEpisodeData(episode.id)}>
                <img class="h-6 w-6 rounded-t-md" src="../icons/edit.svg" alt="Episode List Icon" />
              </button>
            </td>
          </tr>
          {#if selectedEpisodeId == episode.id}
            <DashboardEpisodeListEntry episodeData={selectedEpisodeData} />
          {/if}
        {/each}
      </tbody>
    </table>
  </div>
</div>
