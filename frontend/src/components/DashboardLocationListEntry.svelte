<script>
  export let locationData;
</script>

<tr class="border-b">
  <td colspan="4" class="py-3 px-2">
    <div class="flex w-full gap-3">
      <div class="locations w-1/2">
        <h3 class="font-medium">Episoden</h3>
        <ul>
          {#each locationData.episodes as episode}
            <li>{episode.id} - {episode.title}</li>
          {/each}
        </ul>
      </div>
      <div class="topics w-1/2">
        <h3 class="font-medium">Koordinaten</h3>
        <ul>
          {#each locationData.coordinates as coordinate}
            <li>N{coordinate.longitude}° N {coordinate.latitude}° W</li>
          {/each}
        </ul>
      </div>
    </div>
  </td>
</tr>
