<script>
	import Map from './Map.svelte';
	import EpisodeList from './EpisodeList.svelte';
	
	let selected;
	let selectedLocations = [];

    function forward(event) {
		selected = event.detail.id
    }
</script>

<main class="">
	<div id="world-map-wrapper" class="absolute bottom-0 flex-auto  w-screen h-screen overflow-clip pointer-events-auto">
		<!-- Main World Map -->
		<Map on:selectEpisode={forward} bind:selectedLocations/>

		<!-- Logo -->
		<div
			class="w-32 lg:w-40 absolute top-0 flex bg-slate-400 bg-opacity-80 border-dashed border-gag-primary border-b border-r rounded-br-md"
		>
			<img src="/gag_logo.png" class="object-contain" alt="" />
		</div>

		<!-- Episode List -->
		<EpisodeList bind:selectedLocations bind:selected/>
	</div>
</main>
