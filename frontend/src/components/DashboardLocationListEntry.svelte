<script>
  import { onMount } from 'svelte';
  import { json, geoPath, geoNaturalEarth1, zoom, select, zoomIdentity } from 'd3';

  export let locationData;

  const projection = geoNaturalEarth1();
  const path = geoPath(projection);

  let mapFeatureData = [];
  let bindHandleZoom, bindInitZoom;

  // Zoom and scroll functionality
  $: zoomX = zoom().scaleExtent([0.3, 10]).on('zoom', handleZoom);

  $: if (bindInitZoom) {
    select(bindInitZoom).call(zoomX);
  }

  function handleZoom(e) {
    select(bindHandleZoom).attr('transform', e.transform);
  }

  onMount(() => {
    json('../worldmap.geojson').then((data) => {
      mapFeatureData = data.features;
    });
  });
</script>

<tr class="border-b">
  <td colspan="4" class="py-3 px-2">
    <div class="flex w-full gap-3">
      <div class="episodes m-2 h-fit w-2/3 rounded-md bg-zinc-100 py-2 px-4">
        <h3 class="mb-2 font-medium">Koordinaten</h3>

        <div class="flex">
          <ul class="w-1/2">
            {#each locationData.coordinates as coordinate, id}
              <li class="pb-1">
                <div class="flex w-full items-center gap-1 overflow-clip">
                  <span
                    class="{coordinate.status == 'active'
                      ? 'bg-active-light'
                      : 'bg-hidden-light'} inline-block rounded-full py-1 px-3 text-center text-xs font-bold"
                    >{id + 1}</span
                  >
                  <span class="inline-block truncate"
                    >{coordinate.longitude}° N {coordinate.latitude}° W</span
                  >
                </div>
              </li>
            {/each}
          </ul>

          <div class="w-1/2">
            <!-- D3 Map displaying all coordinates of the location -->
            <svg
              id="world-map"
              class="h-full w-full bg-slate-400"
              viewBox="0 0 1000 500"
              preserveAspectRatio="xMidYMid slice"
              bind:this={bindInitZoom}
            >
              <g class="countries" bind:this={bindHandleZoom}>
                <g class="select-none">
                  {#each mapFeatureData as data}
                    <!-- svelte-ignore a11y-click-events-have-key-events -->
                    <path id={data.id} class="select-none fill-gray-300 stroke-1" d={path(data)} />
                  {/each}
                </g>
                <g class="select-none">
                  {#each locationData.coordinates as coordinate, id}
                    <circle
                      id="{coordinate.status == 'active' ? 'active' : 'hidden'}}"
                      class="{coordinate.status == 'active'
                        ? 'fill-active-light'
                        : 'fill-hidden-light'} "
                      cx={projection([coordinate.longitude, coordinate.latitude])[0]}
                      cy={projection([coordinate.longitude, coordinate.latitude])[1]}
                      r="3"
                    />
                    <text
                      x={projection([coordinate.longitude, coordinate.latitude])[0]}
                      y={projection([coordinate.longitude, coordinate.latitude])[1]}
                      class="text-xs"
                    >
                      {id + 1}</text
                    >
                  {/each}
                </g>
              </g></svg
            >
          </div>
        </div>
      </div>
      <div class="episodes m-2 h-fit w-1/3 rounded-md bg-zinc-100 py-2 px-4">
        <h3 class="mb-2 font-medium">Episoden</h3>
        <ul>
          {#each locationData.episodes as episode}
            <li class="pb-1">
              <div class="flex w-full items-center gap-1 overflow-clip">
                <span
                  class="{episode.status == 'active'
                    ? 'bg-active-light'
                    : 'bg-hidden-light'} inline-block h-3 w-3 rounded-full"
                />
                <p class="inline-block w-10/12 truncate">{episode.key}: {episode.title}</p>
              </div>
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </td>
</tr>
