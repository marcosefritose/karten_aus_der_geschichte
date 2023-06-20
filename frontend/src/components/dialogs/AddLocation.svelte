<script>
  import { onMount } from 'svelte';
  import { setLocations, locations } from '../../routes/store';

  export let episodeData;
  export let toggled = false;

  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  let addLocationDialog = null;
  let addedLocationId = null;
  let addFilterString = '';
  let addContextString = '';
  let episodeLocationIds = episodeData.locations.map((location) => location.id);

  $: addLocationsList = $locations.filter((location) => {
    let searchMatch = location.name.toLowerCase().includes(addFilterString.toLowerCase());
    let locationExists = episodeLocationIds.includes(location.id);
    return searchMatch && !locationExists;
  });

  function addLocation(locationId) {
    let formData = new FormData();
    formData.append('episode_id', episodeData.id);
    formData.append('location_id', locationId);
    formData.append('context', addContextString);

    fetch(`${VITE_FLASK_API_URL}/locations/associate`, {
      method: 'POST',
      body: formData
    })
      .then((response) => {
        if (response.ok) {
          location.reload();
        } else {
          throw new Error('Something went wrong');
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }

  async function loadLocations() {
    if ($locations.length === 0) {
      const locationsRes = await fetch(`${VITE_FLASK_API_URL}/locations`);
      const locationData = await locationsRes.json();

      setLocations(locationData);
    }
  }

  onMount(() => {
    addLocationDialog.showModal();
    loadLocations();

    addLocationsList = [...$locations];
    addLocationsList = addLocationsList.filter(
      (location) => !episodeLocationIds.includes(location.id)
    );
  });
</script>

<dialog bind:this={addLocationDialog}>
  <form class="flex flex-col px-2" on:submit={addLocation(addedLocationId)}>
    <h3 class="mb-2 text-lg font-medium">Ort hinzufügen</h3>
    <p>
      Welcher Ort soll der Episode <b>{episodeData.key}: {episodeData.title}</b> hinzugefügt werden?
    </p>
    <input
      type="text"
      class="border-gray my-2 border p-2"
      placeholder="Filter"
      bind:value={addFilterString}
    />
    <div class="h-48 overflow-y-scroll py-2">
      {#each addLocationsList as location}
        <div class="mb-1 flex">
          <input
            type="radio"
            name="newTopicId"
            id={location.id}
            value={location.id}
            bind:group={addedLocationId}
          />
          <label for={location.id} class="pl-2">{location.name}</label>
        </div>
      {/each}
    </div>
    <p class="mt-4">Möchtest du dem Ort noch einen Kontext hinzufügen?</p>
    <input
      type="text"
      class="border-gray my-2 border p-2"
      placeholder="Kontext"
      bind:value={addContextString}
    />
    <div class="flex justify-end">
      <button
        class=" text-gag-primary mt-4 rounded-lg px-4 py-2"
        on:click={() => (toggled = false)}
        type="button">Abbrechen</button
      >
      <button class="bg-gag-primary mt-4 rounded-lg px-4 py-2 text-white" type="submit"
        >Hinzufügen</button
      >
    </div>
  </form>
</dialog>
