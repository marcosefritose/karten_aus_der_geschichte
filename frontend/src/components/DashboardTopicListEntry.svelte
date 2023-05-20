<script>
  export let topicData;
</script>

<tr class="border-b">
  <td colspan="4" class="py-3 px-2">
    <div class="flex w-full gap-3">
      <div>
        <h3 class="font-medium">Episoden</h3>
        <ul>
          {#each topicData.episodes as episode}
            <li>{episode.key} - {episode.title}</li>
          {/each}
        </ul>
      </div>
    </div>
  </td>
</tr>
