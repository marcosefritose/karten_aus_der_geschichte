<script>
  import DeleteIcon from './icons/DeleteIcon.svelte';
  import AddLocation from './dialogs/AddLocation.svelte';
  import DeleteLocation from './dialogs/DeleteLocation.svelte';
  import AddTopic from './dialogs/AddTopic.svelte';
  import DeleteTopic from './dialogs/DeleteTopic.svelte';
  import EditIcon from './icons/EditIcon.svelte';
  import EditEpisode from './dialogs/EditEpisode.svelte';

  export let episodeData;

  const VITE_FLASK_API_URL = import.meta.env.VITE_FLASK_API_URL;

  let toggleAddLocation = false;
  let toggleDeleteLocation = false;
  let toggleAddTopic = false;
  let toggleDeleteTopic = false;
  let toggleEditEpisode = false;

  let deleteLocationAssocData = null;
  let deleteTopicAssocData = null;
</script>

{#if toggleAddLocation}
  <AddLocation {episodeData} bind:toggled={toggleAddLocation} />
{/if}

{#if toggleDeleteLocation}
  <DeleteLocation
    {episodeData}
    assocData={deleteLocationAssocData}
    bind:toggled={toggleDeleteLocation}
  />
{/if}

{#if toggleAddTopic}
  <AddTopic {episodeData} bind:toggled={toggleAddTopic} />
{/if}

{#if toggleDeleteTopic}
  <DeleteTopic {episodeData} assocData={deleteTopicAssocData} bind:toggled={toggleDeleteTopic} />
{/if}

{#if toggleEditEpisode}
  <EditEpisode {episodeData} bind:toggled={toggleEditEpisode} />
{/if}

<tr class="border-b">
  <td colspan="4" class="py-3 px-2">
    <div class="flex w-full gap-3">
      <div class="locations m-2 h-fit w-1/4 rounded-md bg-zinc-100 py-2 px-4">
        <h3 class="mb-2 font-medium">Schauplätze</h3>
        <ul>
          {#each episodeData.locations_association as assoc}
            <li class="pb-1">
              <div class="flex w-full items-center justify-between">
                <div class="flex w-full items-center gap-1 overflow-clip">
                  <span
                    class="{assoc.location.status == 'active'
                      ? 'bg-active-light'
                      : 'bg-hidden-light'} inline-block h-3 w-3 rounded-full"
                  />
                  <span class="inline-block w-3/4 truncate">{assoc.location.name}</span>
                </div>
                <div
                  on:click={() => {
                    deleteLocationAssocData = assoc;
                    toggleDeleteLocation = true;
                  }}
                >
                  <DeleteIcon height="h-4" width="w-4" />
                </div>
              </div>
              {#if assoc.context}
                <p class="italic text-gray-500">{assoc.context}</p>
              {/if}
            </li>
          {/each}
          <li class="pb-2">
            <div class="flex items-center gap-1" on:click={() => (toggleAddLocation = true)}>
              <div class="inline-block h-3 w-3 rounded-full bg-gray-500" />
              <span class="underline underline-offset-1">Ort hinzufügen</span>
            </div>
          </li>
        </ul>
      </div>
      <div class="topics  m-2 h-fit w-1/4 rounded-md bg-zinc-100 py-2 px-4">
        <h3 class="mb-2 font-medium">Themen</h3>
        <ul>
          {#each episodeData.topics_association as topic}
            <li class="pb-1">
              <div class="flex w-full items-center justify-between">
                <div class="flex w-full items-center gap-1 overflow-clip">
                  <span
                    class="{topic.status == 'active'
                      ? 'bg-active-light'
                      : 'bg-hidden-light'} inline-block h-3 w-3 rounded-full"
                  />
                  <span class="inline-block w-3/4 truncate">{topic.topic_name}</span>
                </div>
                <div
                  on:click={() => {
                    deleteTopicAssocData = topic;
                    toggleDeleteTopic = true;
                  }}
                >
                  <DeleteIcon height="h-4" width="w-4" />
                </div>
              </div>
              {#if topic.context}
                <p class="italic text-gray-500">{topic.context}</p>
              {/if}
            </li>
          {/each}
          <li class="pb-2">
            <div class="flex items-center gap-1" on:click={() => (toggleAddTopic = true)}>
              <div class="inline-block h-3 w-3 rounded-full bg-gray-500" />
              <span class="underline underline-offset-1">Thema hinzufügen</span>
            </div>
          </li>
        </ul>
      </div>
      <div class="topics  m-2 h-fit w-1/2 rounded-md bg-zinc-100 py-2 px-4">
        <div class="flex w-full justify-between">
          <h3 class="mb-2 font-medium">Zeitraum</h3>
          <div on:click={() => (toggleEditEpisode = true)}>
            <EditIcon height="h-4" width="w-4" />
          </div>
        </div>
        <p>
          von <span class="font-semibold">{episodeData.story_time_start}</span>
          bis <span class="font-semibold">{episodeData.story_time_end}</span>
        </p>
        <p class="italic text-gray-500">{episodeData.story_time_description}</p>

        <h3 class="my-2 font-medium">Beschreibung</h3>
        <p>{episodeData.summary}</p>
      </div>
    </div></td
  >
</tr>
