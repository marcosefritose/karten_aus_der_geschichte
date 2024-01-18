<script>
  import { setTopics, topics } from '../../store';
  import DashboardTopicListEntry from '../../../components/DashboardTopicListEntry.svelte';

  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  export let data;

  setTopics(data.topics);

  let searchString = '';
  let filterStatus = 'all';
  let filteredTopics = [...$topics];
  let mergeNewTopicId = null;
  let mergeDialog = null;
  let mergeFilterString = '';

  $: filteredTopics = $topics.filter((topic) => {
    let searchStringMatch = topic.name.toLowerCase().includes(searchString.toLowerCase());
    if (filterStatus === 'all') return searchStringMatch;
    else return topic.status === filterStatus && searchStringMatch;
  });

  $: mergeFilteredTopics = $topics.filter((topic) => {
    return topic.name.toLowerCase().includes(mergeFilterString.toLowerCase());
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

  let selectedTopicId = null;
  let selectedTopicData = null;

  async function loadTopicData(topicId) {
    const response = await fetch(`${VITE_FLASK_API_URL}/topics/${topicId}`);
    const data = await response.json();

    selectedTopicId = topicId;
    selectedTopicData = data;
  }

  function toggleTopic(topicId) {
    if (selectedTopicId === topicId) {
      selectedTopicId = null;
      selectedTopicData = null;
    } else {
      loadTopicData(topicId);
    }
  }

  function updateTopicStatus(topicId, status) {
    const formData = new FormData();
    formData.append('status', status);

    fetch(`${VITE_FLASK_API_URL}/topics/${topicId}/status`, {
      method: 'PATCH',
      body: formData
    }).then(() => {
      const topicIndex = $topics.findIndex((topic) => topic.id === topicId);
      $topics[topicIndex].status = status;
    });
  }

  function deleteTopic(topicId) {
    fetch(`${VITE_FLASK_API_URL}/topics/${topicId}`, {
      method: 'DELETE'
    }).then(() => {
      const topicIndex = $topics.findIndex((topic) => topic.id === topicId);
      $topics.splice(topicIndex, 1);
      $topics = [...$topics];
    });
  }

  function showMergeForm(topicId) {
    selectedTopicId = topicId;
    selectedTopicData = filteredTopics.find((topic) => topic.id === topicId);

    mergeDialog.showModal();
  }

  function mergeTopic(topicId, newTopicId) {
    if (!newTopicId) {
      alert('Bitte wähle ein Thema aus');
      return;
    }

    fetch(`${VITE_FLASK_API_URL}/topics/${topicId}/merge/${newTopicId}`, {
      method: 'PATCH'
    }).then(() => {
      const topicIndex = $topics.findIndex((topic) => topic.id === topicId);
      $topics.splice(topicIndex, 1);
      $topics = [...$topics];
    });
  }

  $: totalCount = $topics.length;
  $: activeCount = $topics.filter((topic) => topic.status === 'active').length;
  $: hiddenCount = $topics.filter((topic) => topic.status === 'hidden').length;
</script>

<dialog bind:this={mergeDialog} class="w-full md:w-1/2 xl:w-1/3">
  {#if selectedTopicData}
    <form class="flex flex-col px-2" on:submit={mergeTopic(selectedTopicId, mergeNewTopicId)}>
      <h3 class="py-4">Zusammenführen von <b>{selectedTopicData.name}</b> mit:</h3>
      <input
        type="text"
        name="merge-filter"
        id="merge-filter"
        class="border-gray my-2 border p-2"
        placeholder="Filter"
        bind:value={mergeFilterString}
      />
      <div class="h-48 overflow-y-scroll py-2">
        {#each mergeFilteredTopics as topic}
          {#if topic.id !== selectedTopicId}
            <div class="mb-1 flex">
              <input
                type="radio"
                name="newTopicId"
                id={topic.id}
                value={topic.id}
                bind:group={mergeNewTopicId}
              />
              <label for={topic.id} class="pl-2">{topic.name}</label>
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
  <h1 class="text-3xl">{$topics.length} Themen</h1>

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
        {#each filteredTopics as topic}
          <tr class="border-b">
            <td class="h-14 py-3 px-2">{topic.name}</td>
            <td class="h-14 py-3 px-2">{topic.episodes.length}</td>
            <td class="h-14 py-3 px-2">
              <span
                class="{`bg-${topic.status}-light text-${topic.status}`} h-16 rounded-lg px-2 py-1"
                >{getStatusForSlug(topic.status)}</span
              >
            </td>
            <td class="py-3 px-2">
              <button on:click={() => toggleTopic(topic.id)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../../icons/edit.svg"
                  alt="Edit Topic Icon"
                />
              </button>
              <button on:click={() => deleteTopic(topic.id)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../../icons/delete.svg"
                  alt="Delete Topic Icon"
                />
              </button>
              <button on:click={() => showMergeForm(topic.id)}>
                <img
                  class="mx-2 h-6 w-6 rounded-t-md"
                  src="../../icons/merge.svg"
                  alt="Merge Topic Icon"
                />
              </button>
              {#if topic.status == 'active'}
                <button on:click={() => updateTopicStatus(topic.id, 'hidden')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/hide.svg"
                    alt="Hide Topic Icon"
                  />
                </button>
              {:else if topic.status == 'hidden'}
                <button on:click={() => updateTopicStatus(topic.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/show.svg"
                    alt="Show Topic Icon"
                  />
                </button>
              {:else if topic.status == 'pending'}
                <button on:click={() => updateTopicStatus(topic.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../../icons/activate.svg"
                    alt="Activate Topic Icon"
                  />
                </button>
              {/if}
            </td>
          </tr>
          {#if selectedTopicId == topic.id}
            <DashboardTopicListEntry topicData={selectedTopicData} />
          {/if}
        {/each}
      </tbody>
    </table>
  </div>
</div>
