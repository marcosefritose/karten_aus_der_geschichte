<script>
  import { onMount } from 'svelte';

  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  export let episodeData;
  export let assocData;
  export let toggled = false;

  let deleteTopicAssocDialog = null;

  function deleteTopicAssoc(topicId) {
    let formData = new FormData();
    formData.append('episode_id', episodeData.id);
    formData.append('topic_id', topicId);

    fetch(`${VITE_FLASK_API_URL}/topics/associate`, {
      method: 'DELETE',
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
    deleteTopicAssocDialog.showModal();
  });
</script>

<dialog bind:this={deleteTopicAssocDialog}>
  {#if assocData != null}
    <form on:submit={deleteTopicAssoc(assocData.topic_id)}>
      <h3 class="mb-2 text-lg font-medium">Themenverknüpfung löschen</h3>
      <p class="mb-4">
        Möchtest du die Verknüpfung von dem Ort
        <span class="block py-2 font-bold">{assocData.topic_name}</span>
        mit dem Thema
        <span class="block py-2 font-bold">{episodeData.key}: {episodeData.title}</span>
        wirklich löschen?
      </p>
      <p>
        Sowohl das Thema als auch die Episode bleiben erhalten. Das Thema kann jederzeit wieder mit
        der Episode verknüpft werden.
      </p>
      <div class="flex justify-end">
        <button
          class=" text-gag-primary mt-4 rounded-lg px-4 py-2"
          on:click={() => (toggled = false)}
          type="button">Abbrechen</button
        >
        <button class="bg-gag-primary mt-4 rounded-lg px-4 py-2 text-white" type="submit"
          >Löschen</button
        >
      </div>
    </form>
  {/if}
</dialog>
