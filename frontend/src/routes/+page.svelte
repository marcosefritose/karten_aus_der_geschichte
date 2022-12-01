<script>
	import { onMount } from 'svelte';
	import { json, geoPath, geoNaturalEarth1, geoMercator } from 'd3';

    const  projection  =  geoNaturalEarth1();
    const  path  =  geoPath(projection);
	export let data;
	let episodes = [];
    let dataset = [];
    let markers = [];

    // Static url until images are served from flask server
    let imgUrl = "https://images.podigee-cdn.net/0x,sw_d9izO9QfY97alR2f13b7IrOVeXM5gFZOjetk-5sTg=/https://cdn.podigee.com/uploads/u32412/b610d282-8f99-4604-a16f-28ada94ab76a.jpg";

	onMount(() => {
		episodes = data.episodes;
        episodes.forEach(ep => {
            let locations = ep.locations.map((loc) => {
                return {id: ep.id, longitude: loc.longitude, latitude: loc.latitude}
            });           
            markers = markers.concat(locations)
        })

        console.log(markers);


        // ToDo move geojson to flask server/static files
		json(
			'https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson'
		).then((data) => {
			dataset = data.features;
		});
	});
</script>

<main class="">
	<div class="grid  w-screen h-screen p-8 bg-gray-50 place-items-center">
		<h1 class="text-center text-3xl font-bold">Karten aus der Geschichte</h1>
		<div class="w-full h-full relative overflow-hidden">
			<!-- World Map -->
			<div class="w-screen h-screen overflow-hidden">
				<svg class="w-full h-full" viewBox="0 0 1000 550" preserveAspectRatio="xMidYMin meet">
					{#each dataset as data}
						<path class="fill-gray-300 stroke-1" d={path(data)} />
					{/each}
					{#each markers as marker}
						<circle
							class="fill-yellow-500 "
							r="2"
							transform="translate({projection([marker.longitude, marker.latitude])})"
						/>
					{/each}
				</svg>
			</div>
			<!-- Episode List -->
			<div id="list" class="flex items-center absolute right-0 top-0 w-1/4 h-full">
				<div
					class="bg-gray-200 opacity-80 overflow-y-scroll h-3/4 m-5 p-3 scrollbar-thin rounded-xl scrollbar-thumb-gag-primary scrollbar-track-gray-400"
				>
					{#each episodes as episode (episode.id)}
						<div class="flex gap-2 border py-1">
							<img src={imgUrl} class="w-16 h-16 rounded-sm border border-gray-400" alt="" />
							<div class="flex-row">
								<span class="bg-gag-primary text-white px-2 py-1 rounded-md text-sm font-bold"
									>{episode.title.split(': ')[0]}</span
								>
								<div class="w-full">
									<span class="mb-1 inline-block text-small">{episode.title.split(': ')[1]}</span
									><br />
								</div>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</div>
</main>
