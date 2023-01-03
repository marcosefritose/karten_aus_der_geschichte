<script>
	import { onMount } from 'svelte';
	import Map from './Map.svelte';
	import EpisodeList from './EpisodeList.svelte';
	
	// Episodes & Location Data
	export let data;
	let episodes = [];
	let locations = [];
	
	let selected;
	let selectedLocations = [];

	onMount(() => {
		episodes = data.episodes;
		locations = data.locations;
	});
</script>

<main class="">
	<div class="flex-col w-screen h-screen bg-blue-100 place-items-center overflow-clip">
		<div id="world-map-wrapper" class="relative flex-auto w-full h-full overflow-hidden">
			<!-- Main World Map -->
			<Map bind:locations={locations} bind:selectedLocations={selectedLocations}/>

			<!-- Logo -->
			<div
				class="w-32 lg:w-40 absolute top-0 flex bg-slate-400 bg-opacity-80 border-dashed border-gag-primary border-b border-r rounded-br-md"
			>
				<img src="/gag_logo.png" class="object-contain" alt="" />
			</div>

			<!-- Episode List -->
			<EpisodeList bind:episodes={episodes} bind:selectedLocations={selectedLocations} bind:selected={selected}/>
		</div>
	</div>
</main>
