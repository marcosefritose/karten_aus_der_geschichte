<script>
    import { onMount } from 'svelte';

    export let data;
    const { episodes } = data;
    
</script>

<main class="">
    <div class="grid grid-cols-4 w-screen h-screen p-8 bg-gray-50 place-items-center">
        <h1 class="text-center text-2xl col-span-4">Karten aus der Geschichte</h1>
        <div class="col-span-3 w-full">
            <svg id="map" class="w-full h-full"></svg>
        </div>
        <div id="list" class="w-full h-full bg-gray-100 overflow-scroll">
            {#each episodes as episode}
            <span class="mb-1 inline-block">{episode.title}</span><br>
            {/each}
        </div>
    </div>
</main>