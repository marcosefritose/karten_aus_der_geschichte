<script>
  import { setLocations, locations } from '../../store';
  import DashboardLocationListEntry from '../../../components/DashboardLocationListEntry.svelte';

  export let data;

  setLocations(data.locations);

  let searchString = '';
  let filteredLocations = $locations;

  $: filteredLocations = $locations.filter((location) => {
    return location.name.toLowerCase().includes(searchString.toLowerCase());
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
    const response = await fetch(`http://localhost:5001/locations/${locationId}`);
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

    fetch(`http://localhost:5001/locations/${locationId}/status`, {
      method: 'PATCH',
      body: formData
    }).then(() => {
      const locationIndex = filteredLocations.findIndex((location) => location.id === locationId);
      filteredLocations[locationIndex].status = status;
    });
  }
</script>

<div class="bg-gag-white w-full overflow-y-scroll p-10">
  <div class="flex">
    <h1 class="text-3xl">{filteredLocations.length} Orte</h1>
    <input
      bind:value={searchString}
      class="focus:ring-gag-primary ml-auto rounded-lg bg-white px-2 py-1 focus:outline-none focus:ring-2 focus:ring-opacity-50"
      type="text"
      placeholder="Suche"
    />
  </div>

  <div class="bg-gag-light mt-3 flex flex-col flex-wrap rounded-lg">
    <table>
      <thead class="border-b font-medium">
        <tr>
          <td class="h-14 w-6/12 py-3 px-2">Name</td>
          <td class="h-14 w-2/12 py-3 px-2"># Folgen</td>
          <td class="h-14 w-2/12 py-3 px-2">Status</td>
          <td class="h-14 w-2/12 py-3 px-2">Aktion</td>
        </tr>
      </thead>
      <tbody class="bg-white">
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
                  src="../icons/edit.svg"
                  alt="Edit Location Icon"
                />
              </button>
              {#if location.status == 'active'}
                <button on:click={() => updateLocationStatus(location.id, 'hidden')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/hide.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {:else if location.status == 'hidden'}
                <button on:click={() => updateLocationStatus(location.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/show.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {:else if location.status == 'pending'}
                <button on:click={() => updateLocationStatus(location.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/activate.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {/if}
            </td>
          </tr>
          {#if selectedLocationId == location.id}
            <DashboardLocationListEntry locationData={selectedLocationData} />
          {/if}
        {/each}
      </tbody>
    </table>
  </div>
</div>
