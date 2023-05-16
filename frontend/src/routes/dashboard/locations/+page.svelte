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

  let selectedLocationName = null;
  let selectedLocationData = null;

  async function loadLocationData(locationName) {
    const response = await fetch(`http://localhost:5001/locations/${locationName}`);
    const data = await response.json();

    selectedLocationName = locationName;
    selectedLocationData = data;
  }

  function toggleLocation(locationName) {
    if (selectedLocationName === locationName) {
      selectedLocationName = null;
      selectedLocationData = null;
    } else {
      loadLocationData(locationName);
    }
  }

  function updateLocationStatus(locationName, status) {
    const formData = new FormData();
    formData.append('status', status);

    fetch(`http://localhost:5001/locations/${locationName}`, {
      method: 'PATCH',
      body: formData
    }).then(() => {
      const locationIndex = $locations.findIndex((location) => location.name === locationName);
      $locations[locationIndex].status = status;
    });
  }
</script>

<div class="bg-gag-white w-full overflow-y-scroll p-10">
  <div class="flex">
    <h1 class="text-3xl">{$locations.length} Orte</h1>
    <input
      bind:value={searchString}
      class="ml-auto rounded-lg bg-white px-2 py-1"
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
              <button on:click={() => toggleLocation(location.name)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../icons/edit.svg"
                  alt="Edit Location Icon"
                />
              </button>
              {#if location.status == 'active'}
                <button on:click={() => updateLocationStatus(location.name, 'hidden')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/hide.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {:else if location.status == 'hidden'}
                <button on:click={() => updateLocationStatus(location.name, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/show.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {:else if location.status == 'pending'}
                <button on:click={() => updateLocationStatus(location.name, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/activate.svg"
                    alt="Hide Location Icon"
                  />
                </button>
              {/if}
            </td>
          </tr>
          {#if selectedLocationName == location.name}
            <DashboardLocationListEntry locationData={selectedLocationData} />
          {/if}
        {/each}
      </tbody>
    </table>
  </div>
</div>
