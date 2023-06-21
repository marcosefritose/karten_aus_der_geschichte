<script>
  import { onMount } from 'svelte';

  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  export let episodeData;
  export let toggled = false;

  let editEpisodeDialog = null;

  let episode_time_start = episodeData.story_time_start;
  let episode_time_end = episodeData.story_time_end;
  let episode_time_description = episodeData.story_time_description;
  let episode_summary = episodeData.summary;

  function updateEpisode() {
    let formData = new FormData();
    formData.append('story_time_start', episode_time_start);
    formData.append('story_time_end', episode_time_end);
    formData.append('story_time_description', episode_time_description);
    formData.append('summary', episode_summary);

    fetch(`${VITE_FLASK_API_URL}/episodes/${episodeData.id}`, {
      method: 'PATCH',
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

  onMount(() => {
    editEpisodeDialog.showModal();
  });
</script>

<dialog bind:this={editEpisodeDialog} class="min-w-[50%]">
  {#if episodeData != null}
    <form on:submit={() => updateEpisode()}>
      <h3 class="mb-2 text-lg font-medium">Episode bearbeiten</h3>

      <div class="flex flex-col gap-2">
        <div class="flex w-full gap-2">
          <div class="flex w-1/2 flex-col">
            <label for="episode_time_start">Start Jahr</label>
            <input
              class="rounded-lg border border-gray-500 px-4 py-2"
              id="episode_time_start"
              name="episode_time_start"
              type="number"
              bind:value={episode_time_start}
            />
          </div>
          <div class="flex w-1/2 flex-col">
            <label for="episode_time_end">Ende Jahr</label>
            <input
              class="rounded-lg border border-gray-500 px-4 py-2"
              id="episode_time_end"
              name="episode_time_end"
              type="number"
              bind:value={episode_time_end}
            />
          </div>
        </div>

        <label for="episode_time_description">Zeitbeschreibung</label>
        <textarea
          class="h-20 resize-none rounded-lg border border-gray-500 px-4 py-2"
          id="episode_time_description"
          name="episode_time_description"
          bind:value={episode_time_description}
        />
        <label for="episode_summary">Zusammenfassung</label>
        <textarea
          class="h-36 resize-none rounded-lg border border-gray-500 px-4 py-2"
          id="episode_summary"
          name="episode_summary"
          bind:value={episode_summary}
        />
        <div class="flex justify-end">
          <button
            class=" text-gag-primary mt-4 rounded-lg px-4 py-2"
            on:click={() => (toggled = false)}
            type="button">Abbrechen</button
          >
          <button class="bg-gag-primary mt-4 rounded-lg px-4 py-2 text-white" type="submit"
            >Aktualisieren</button
          >
        </div>
      </div>
    </form>
  {/if}
</dialog>
