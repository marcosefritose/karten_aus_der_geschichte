<script>
  import { setTopics, topics } from '../../store';
  import DashboardTopicListEntry from '../../../components/DashboardTopicListEntry.svelte';

  export let data;

  setTopics(data.topics);

  let searchString = '';
  let filteredTopics = $topics;

  $: filteredTopics = $topics.filter((topic) => {
    return topic.name.toLowerCase().includes(searchString.toLowerCase());
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
    const response = await fetch(`http://localhost:5001/topics/${topicId}`);
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

    fetch(`http://localhost:5001/topics/${topicId}/status`, {
      method: 'PATCH',
      body: formData
    }).then(() => {
      const topicIndex = filteredTopics.findIndex((topic) => topic.id === topicId);
      filteredTopics[topicIndex].status = status;
    });
  }
</script>

<div class="bg-gag-white w-full overflow-y-scroll p-10">
  <div class="flex">
    <h1 class="text-3xl">{filteredTopics.length} Themen</h1>
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
                  src="../icons/edit.svg"
                  alt="Edit Topic Icon"
                />
              </button>
              {#if topic.status == 'active'}
                <button on:click={() => updateTopicStatus(topic.id, 'hidden')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/hide.svg"
                    alt="Hide Topic Icon"
                  />
                </button>
              {:else if topic.status == 'hidden'}
                <button on:click={() => updateTopicStatus(topic.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/show.svg"
                    alt="Hide Topic Icon"
                  />
                </button>
              {:else if topic.status == 'pending'}
                <button on:click={() => updateTopicStatus(topic.id, 'active')}>
                  <img
                    class="mx-2 h-6 w-6 rounded-t-md"
                    src="../icons/activate.svg"
                    alt="Hide Topic Icon"
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
