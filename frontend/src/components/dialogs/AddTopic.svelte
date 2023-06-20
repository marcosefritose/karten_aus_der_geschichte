<script>
  import { onMount } from 'svelte';
  import { setTopics, topics } from '../../routes/store';

  export let episodeData;
  export let toggled = false;

  //   console.log(episodeData);

  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  let addTopicDialog = null;
  let addedTopicId = null;
  let addFilterString = '';
  let addContextString = '';
  let episodeTopicNames = episodeData.topics_association.map((topic) => topic.topic_name);

  $: addTopicsList = $topics.filter((topic) => {
    let searchMatch = topic.name.toLowerCase().includes(addFilterString.toLowerCase());
    let topicExists = episodeTopicNames.includes(topic.name);
    return searchMatch && !topicExists;
  });

  function addTopic(topicId) {
    let formData = new FormData();
    formData.append('episode_id', episodeData.id);
    formData.append('topic_id', topicId);
    formData.append('context', addContextString);

    fetch(`${VITE_FLASK_API_URL}/topics/associate`, {
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

  async function loadTopics() {
    if ($topics.length === 0) {
      const topicsRes = await fetch(`${VITE_FLASK_API_URL}/topics`);
      const topicData = await topicsRes.json();

      setTopics(topicData);
    }
  }

  onMount(() => {
    addTopicDialog.showModal();
    loadTopics();
  });
</script>

<dialog bind:this={addTopicDialog}>
  <form class="flex flex-col px-2" on:submit={addTopic(addedTopicId)}>
    <h3 class="mb-2 text-lg font-medium">Thema hinzufügen</h3>
    <p>
      Welches Thema soll der Episode <b>{episodeData.key}: {episodeData.title}</b> hinzugefügt werden?
    </p>
    <input
      type="text"
      class="border-gray my-2 border p-2"
      placeholder="Filter"
      bind:value={addFilterString}
    />
    <div class="h-48 overflow-y-scroll py-2">
      {#each addTopicsList as topic}
        <div class="mb-1 flex">
          <input
            type="radio"
            name="newTopicId"
            id={topic.id}
            value={topic.id}
            bind:group={addedTopicId}
          />
          <label for={topic.id} class="pl-2">{topic.name}</label>
        </div>
      {/each}
    </div>
    <p class="mt-4">Möchtest du dem Thema noch einen Kontext hinzufügen?</p>
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
