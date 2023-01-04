<script>
    export let coords;
    export let location;

    $: ({x, y} = coords)
</script>


<div class="absolute bg-gray-300 max-w-sm rounded-md border border-gray-900" style="left: {x}px; top: {y}px">
    <p class="text-center text-lg font-semibold py-1">{location.name}</p>
    <ul class="p-1">
        {#each location.episodes as episode, id}
            <li class="pb-1"><span class="font-bold">{episode.id}</span>: {episode.title}</li>
        {/each}
    </ul>
</div>