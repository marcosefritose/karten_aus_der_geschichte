<script>
    import { onMount } from 'svelte';
    import { Runtime, Inspector } from '@observablehq/runtime';
	// import notebook from '@d3/zoom-to-bounding-box';
	import notebook from '@jashkenas/latitude-longitude-world-map-plotter';
    import * as topojson from "topojson-client";

    export let data;
    let episodes = [];

    let worldMap;
    let module;
    let landColor;
    let coordinates = "0,0"

    $: if (module) module.redefine('landColor', landColor)
    $: if (module) module.redefine('coordinates', coordinates)


	onMount(() => {
        episodes = data.episodes;


        const runtime = new Runtime();
        module = runtime.module(notebook, (name) => {
            
            if (name === 'earth') {
                return new Inspector(worldMap);
            }
        });
	});

</script>

<main class="">
    <div class="grid  w-screen h-screen p-8 bg-gray-50 place-items-center">
        <h1 class="text-center text-3xl font-bold">Karten aus der Geschichte</h1>
        <div class="w-full h-full relative overflow-hidden">
            <div bind:this={worldMap}></div>
            <div id="list" class="flex items-center absolute right-0 top-0 w-1/4 h-full">
                <div class="bg-gray-200 opacity-80 overflow-y-scroll h-3/4 m-5 p-3 scrollbar-thin rounded-xl scrollbar-thumb-gag-primary scrollbar-track-gray-400">
                    {#each episodes as episode (episode.id)}
                    <div class="flex gap-2 border py-1">
                        <img src="{episode.image}" class="w-16 h-16 rounded-sm border border-gray-400" alt="">
                        <div class="flex-row">
                            <span class="bg-gag-primary text-white px-2 py-1 rounded-md text-sm font-bold">{episode.title.split(': ')[0]}</span>
                            <div class="w-full">
                                <span class="mb-1 inline-block text-small">{episode.title.split(': ')[1]}</span><br>
                            </div>
                        </div>
                    </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>
</main>