<script>
	import Map from './Map.svelte';
	import EpisodeList from './EpisodeList.svelte';
</script>

<main class="">
	<div id="world-map-wrapper" class="absolute bottom-0 flex-auto  w-screen h-screen overflow-clip pointer-events-auto">
		<!-- Main World Map -->
		<Map/>

		<!-- Logo -->
		<div
			class="w-32 lg:w-40 absolute top-0 flex bg-slate-400 bg-opacity-80 border-dashed border-gag-primary border-b border-r rounded-br-md"
		>
			<img src="/gag_logo.png" class="object-contain" alt="" />
		</div>

		<!-- Link -->
		<div class="absolute right-0 top-0 p-2 text-sm">
			Made with 🧠 by <a href="https://marcose.eu" target="_blank" rel="noopener noreferrer" class="underline underline-offset-2">marcose</a>.
		</div>

		<!-- Episode List -->
		<EpisodeList/>
	</div>
</main>
