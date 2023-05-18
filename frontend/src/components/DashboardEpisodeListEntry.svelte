<script>
  export let episodeData;

  console.log(episodeData);
</script>

<tr class="border-b">
  <td colspan="4" class="py-3 px-2">
    <div class="flex w-full gap-3">
      <div class="locations w-1/4">
        <h3 class="font-medium">Schauplätze</h3>
        <ul>
          {#each episodeData.locations_association as assoc}
            <li>{assoc.location.name} - {assoc.context}</li>
          {/each}
        </ul>
      </div>
      <div class="topics w-1/4">
        <h3 class="font-medium">Themen</h3>
        <ul>
          {#each episodeData.topics_association as topic}
            <li>{topic.topic_name} - {topic.context}</li>
          {/each}
        </ul>
      </div>
      <div class="summary w-1/4">
        <h3 class="font-medium">Beschreibung</h3>
        <p>{episodeData.summary}</p>
      </div>
      <div class="times w-1/4">
        <h3 class="font-medium">Zeitraum</h3>
        <p>
          <span>von: </span>{episodeData.story_time_start}
        </p>
        <p>
          <span>bis: </span>{episodeData.story_time_end}
        </p>
      </div>
    </div>
  </td>
</tr>
