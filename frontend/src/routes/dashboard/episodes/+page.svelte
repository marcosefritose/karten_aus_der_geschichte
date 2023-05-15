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
  }

  function toggleEpisode(episodeId) {
    if (selectedEpisodeId === episodeId) {
      selectedEpisodeId = null;
      selectedEpisodeData = null;
    } else {
      loadEpisodeData(episodeId);
    }
  }

  function getStatusForSlug(statusSlug) {
    switch (statusSlug) {
      case 'active':
        return 'Aktiv';
      case 'pending':
        return 'Ausstehend';
      case 'hidden':
        return 'Versteckt';
      default:
        return 'Unbekannt';
    }
  }

  function updateEpisodeStatus(episodeId, status) {
    const formData = new FormData();
    formData.append('status', status);

    fetch(`http://localhost:5001/episodes/${episodeId}/status`, {
      method: 'POST',
      body: formData
    }).then(() => {
      const episodeIndex = $episodes.findIndex((episode) => episode.id === episodeId);
      $episodes[episodeIndex].status = status;
    });
  }
</script>

<div class="bg-gag-white w-full overflow-y-scroll p-10">
  <h1 class="text-3xl">{$episodes.length} Episoden</h1>

  <div class="bg-gag-light mt-3 flex flex-col flex-wrap rounded-lg">
    <table>
      <thead class="border-b font-medium">
        <tr>
          <td class="w-1/12 py-3 px-2">ID</td>
          <td class="w-7/12 py-3 px-2">Titel</td>
          <td class="w-2/12 py-3 px-2">Status</td>
          <td class="w-2/12 py-3 px-2">Aktion</td>
        </tr>
      </thead>
      <tbody class="bg-white">
        {#each $episodes as episode}
          <tr class="border-b">
            <td class="py-3 px-2">{episode.id}</td>
            <td class="py-3 px-2">{episode.title}</td>
            <td class="py-3 px-2">
              <span
                class="{`bg-${episode.status}-light text-${episode.status}`} rounded-lg px-2 py-1"
                >{getStatusForSlug(episode.status)}</span
              >
            </td>
            <td class="py-3 px-2">
              <button on:click={() => toggleEpisode(episode.id)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../icons/edit.svg"
                  alt="Edit Episode Icon"
                />
              </button>
              {#if episode.status == 'active'}
                <button on:click={() => updateEpisodeStatus(episode.id, 'hidden')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/hide.svg"
                    alt="Hide Episode Icon"
                  />
                </button>
              {:else if episode.status == 'hidden'}
                <button on:click={() => updateEpisodeStatus(episode.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/show.svg"
                    alt="Hide Episode Icon"
                  />
                </button>
              {:else if episode.status == 'pending'}
                <button on:click={() => updateEpisodeStatus(episode.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/activate.svg"
                    alt="Hide Episode Icon"
                  />
                </button>
              {/if}
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
