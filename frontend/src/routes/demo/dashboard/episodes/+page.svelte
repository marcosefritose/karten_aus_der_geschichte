<script>
  import DashboardEpisodeListEntry from '../../../../components/DashboardEpisodeListEntry.svelte';
  import { setEpisodes, episodes } from '../../../store';

  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  export let data;

  let selectedEpisodeId = null;
  let selectedEpisodeData = null;

  let searchString = '';
  let filterStatus = 'all';

  let totalCount = 0;
  let pendingCount = 0;
  let activeCount = 0;
  let hiddenCount = 0;

  setEpisodes(data.episodes);

  $: searchEpisodes = $episodes.map((episode) => {
    return {
      id: episode.id,
      key: episode.key,
      title: episode.title,
      status: episode.status,
      searchTerm: `${episode.key} ${episode.title} ${episode.summary}`
    };
  });

  $: filteredEpisodes = searchEpisodes.filter((episode) => {
    let searchStringMatch = episode.searchTerm.toLowerCase().includes(searchString.toLowerCase());
    if (filterStatus === 'all') return searchStringMatch;
    else return searchStringMatch && episode.status === filterStatus;
  });

  async function loadEpisodeData(id) {
    const response = await fetch(`${VITE_FLASK_API_URL}/episodes/${id}`);
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
    fetch(`${VITE_FLASK_API_URL}/episodes/${episodeId}/status`, {
      method: 'PATCH',
      body: formData
    }).then(() => {
      const episodeIndex = $episodes.findIndex((episode) => episode.id === episodeId);
      $episodes[episodeIndex].status = status;
    });
  }

  $: totalCount = $episodes.length;
  $: pendingCount = $episodes.filter((episode) => episode.status === 'pending').length;
  $: activeCount = $episodes.filter((episode) => episode.status === 'active').length;
  $: hiddenCount = $episodes.filter((episode) => episode.status === 'hidden').length;
</script>

<div class="bg-gag-light w-full overflow-y-scroll p-10">
  <h1 class="text-3xl">{$episodes.length} Episoden</h1>

  <div class="bg-gag-white mt-3 flex flex-col flex-wrap rounded-lg p-5">
    <div class="mb-4 flex items-center">
      <span
        class="mx-4 cursor-pointer {filterStatus == 'all' ? 'font-bold' : ''}"
        on:click={() => (filterStatus = 'all')}
        on:keydown={() => (filterStatus = 'all')}>Alle ({totalCount})</span
      >
      <span
        class="mx-4 cursor-pointer {filterStatus == 'pending' ? 'font-bold' : ''}"
        on:click={() => (filterStatus = 'pending')}
        on:keydown={() => (filterStatus = 'pending')}>Ausstehend ({pendingCount})</span
      >
      <span
        class="mx-4 cursor-pointer {filterStatus == 'active' ? 'font-bold' : ''}"
        on:click={() => (filterStatus = 'active')}
        on:keydown={() => (filterStatus = 'active')}>Aktiv ({activeCount})</span
      >
      <span
        class="mx-4 cursor-pointer {filterStatus == 'hidden' ? 'font-bold' : ''}"
        on:click={() => (filterStatus = 'hidden')}
        on:keydown={() => (filterStatus = 'hidden')}>Deaktiviert ({hiddenCount})</span
      >
      <input
        bind:value={searchString}
        class="focus:ring-gag-primary ml-auto h-10 w-64 rounded-lg border border-gray-400 px-2 py-1 focus:border-none focus:outline-none focus:ring-2 focus:ring-opacity-50"
        type="text"
        placeholder="Suche"
      />
    </div>
    <table>
      <thead class="bg-gag-light border-b font-medium text-zinc-500">
        <tr>
          <td class="h-14 w-1/12 px-2 py-5">ID</td>
          <td class="h-14 w-7/12 px-2 py-5">Titel</td>
          <td class="h-14 w-2/12 px-2 py-5">Status</td>
          <td class="h-14 w-2/12 px-2 py-5">Aktion</td>
        </tr>
      </thead>
      <tbody>
        {#each filteredEpisodes as episode}
          <tr class="border-b">
            <td class="h-14 py-3 px-2">{episode.key}</td>
            <td class="h-14 py-3 px-2">{episode.title}</td>
            <td class="h-14 py-3 px-2">
              <span
                class="{`bg-${episode.status}-light text-${episode.status}`} rounded-lg px-2 py-1"
                >{getStatusForSlug(episode.status)}</span
              >
            </td>
            <td class="h-14 py-3 px-2">
              <button on:click={() => toggleEpisode(episode.id)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../../icons/edit.svg"
                  alt="Edit Episode Icon"
                />
              </button>
              {#if episode.status == 'active'}
                <button on:click={() => updateEpisodeStatus(episode.id, 'hidden')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/hide.svg"
                    alt="Hide Episode Icon"
                  />
                </button>
              {:else if episode.status == 'hidden'}
                <button on:click={() => updateEpisodeStatus(episode.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/show.svg"
                    alt="Hide Episode Icon"
                  />
                </button>
              {:else if episode.status == 'pending'}
                <button on:click={() => updateEpisodeStatus(episode.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/activate.svg"
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
