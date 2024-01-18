<script>
  import { setLocations, locations } from '../../store';
  import DashboardLocationListEntry from '../../../components/DashboardLocationListEntry.svelte';

  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  export let data;

  setLocations(data.locations);

  let searchString = '';
  let filterStatus = 'all';
  let filteredLocations = [...$locations];
  let mergeNewLocationId = null;
  let mergeDialog = null;
  let mergeFilterString = '';

  $: filteredLocations = $locations.filter((location) => {
    let searchStringMatch = location.name.toLowerCase().includes(searchString.toLowerCase());

    if (filterStatus === 'all') return searchStringMatch;
    else return location.status === filterStatus && searchStringMatch;
  });

  $: mergeFilteredLocations = $locations.filter((location) => {
    return location.name.toLowerCase().includes(mergeFilterString.toLowerCase());
  });

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

  let selectedLocationId = null;
  let selectedLocationData = null;

  async function loadLocationData(locationId) {
    const response = await fetch(`${VITE_FLASK_API_URL}/locations/${locationId}`);
    const data = await response.json();

    selectedLocationId = locationId;
    selectedLocationData = data;
  }

  function toggleLocation(locationId) {
    if (selectedLocationId === locationId) {
      selectedLocationId = null;
      selectedLocationData = null;
    } else {
      loadLocationData(locationId);
    }
  }

  function updateLocationStatus(locationId, status) {
    const formData = new FormData();
    formData.append('status', status);

    fetch(`${VITE_FLASK_API_URL}/locations/${locationId}/status`, {
      method: 'PATCH',
      body: formData
    }).then(() => {
      const locationIndex = $locations.findIndex((location) => location.id === locationId);
      $locations[locationIndex].status = status;
    });
  }

  function deleteLocation(locationId) {
    fetch(`${VITE_FLASK_API_URL}/locations/${locationId}`, {
      method: 'DELETE'
    }).then(() => {
      const locationIndex = $locations.findIndex((location) => location.id === locationId);
      $locations.splice(locationIndex, 1);
      $locations = [...$locations];
    });
  }

  function showMergeForm(locationId) {
    selectedLocationId = locationId;
    selectedLocationData = filteredLocations.find((location) => location.id === locationId);

    mergeDialog.showModal();
  }

  function mergeLocation(locationId, newLocationId) {
    if (!newLocationId) {
      alert('Bitte wähle ein Thema aus');
      return;
    }

    fetch(`${VITE_FLASK_API_URL}/locations/${locationId}/merge/${newLocationId}`, {
      method: 'PATCH'
    }).then(() => {
      const locationIndex = $locations.findIndex((location) => location.id === locationId);
      $locations.splice(locationIndex, 1);
      $locations = [...$locations];
    });
  }

  $: totalCount = $locations.length;
  $: activeCount = $locations.filter((location) => location.status === 'active').length;
  $: hiddenCount = $locations.filter((location) => location.status === 'hidden').length;
</script>

<dialog bind:this={mergeDialog} class="w-full md:w-1/2 xl:w-1/3">
  {#if selectedLocationData}
    <form
      class="flex flex-col px-2"
      on:submit={mergeLocation(selectedLocationId, mergeNewLocationId)}
    >
      <h3 class="py-4">Zusammenführen von <b>{selectedLocationData.name}</b> mit:</h3>
      <input
        type="text"
        name="merge-filter"
        id="merge-filter"
        class="border-gray my-2 border p-2"
        placeholder="Filter"
        bind:value={mergeFilterString}
      />
      <div class="h-48 overflow-y-scroll py-2">
        {#each mergeFilteredLocations as location}
          {#if location.id !== selectedLocationId}
            <div class="mb-1 flex">
              <input
                type="radio"
                name="newTopicId"
                id={location.id}
                value={location.id}
                bind:group={mergeNewLocationId}
              />
              <label for={location.id} class="pl-2">{location.name}</label>
            </div>
          {/if}
        {/each}
      </div>
      <div class="flex justify-end">
        <button
          class=" text-gag-primary mt-4 rounded-lg px-4 py-2"
          on:click={() => mergeDialog.close()}
          type="button">Abbrechen</button
        >
        <button class="bg-gag-primary mt-4 rounded-lg px-4 py-2 text-white" type="submit"
          >Merge</button
        >
      </div>
    </form>
  {/if}
</dialog>

<div class="bg-gag-light w-full overflow-y-scroll p-10">
  <h1 class="text-3xl">{$locations.length} Orte</h1>

  <div class="bg-gag-white mt-3 flex flex-col flex-wrap rounded-lg p-5">
    <div class="mb-4 flex items-center">
      <span
        class="mx-4 cursor-pointer {filterStatus == 'all' ? 'font-bold' : ''}"
        on:click={() => (filterStatus = 'all')}
        on:keydown={() => (filterStatus = 'all')}>Alle ({totalCount})</span
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
          <td class="h-14 w-6/12 py-5 px-2">Name</td>
          <td class="h-14 w-2/12 py-5 px-2"># Folgen</td>
          <td class="h-14 w-2/12 py-5 px-2">Status</td>
          <td class="h-14 w-2/12 py-5 px-2">Aktion</td>
        </tr>
      </thead>
      <tbody>
        {#each filteredLocations as location}
          <tr class="border-b">
            <td class="h-14 py-3 px-2">{location.name}</td>
            <td class="h-14 py-3 px-2">{location.episodes.length}</td>
            <td class="h-14 py-3 px-2">
              <span
                class="{`bg-${location.status}-light text-${location.status}`} h-16 rounded-lg px-2 py-1"
                >{getStatusForSlug(location.status)}</span
              >
            </td>
            <td class="py-3 px-2">
              <button on:click={() => toggleLocation(location.id)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../../icons/edit.svg"
                  alt="Edit Location Icon"
                />
              </button>
              <button on:click={() => deleteLocation(location.id)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../../icons/delete.svg"
                  alt="Delete Location Icon"
                />
              </button>
              <button on:click={() => showMergeForm(location.id)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../../icons/merge.svg"
                  alt="Merge Location Icon"
                />
              </button>
              {#if location.status == 'active'}
                <button on:click={() => updateLocationStatus(location.id, 'hidden')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/hide.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {:else if location.status == 'hidden'}
                <button on:click={() => updateLocationStatus(location.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/show.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {:else if location.status == 'pending'}
                <button on:click={() => updateLocationStatus(location.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/activate.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {/if}
            </td></tr
          >
          {#if selectedLocationId == location.id}
            <DashboardLocationListEntry locationData={selectedLocationData} />
          {/if}
        {/each}
      </tbody>
    </table>
  </div>
</div>
