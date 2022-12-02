<script>
	import { onMount } from 'svelte';
	import { json, geoPath, geoNaturalEarth1, geoMercator } from 'd3';

    const  projection  =  geoNaturalEarth1();
    const  path  =  geoPath(projection);
	export let data;
	let episodes = [];
    let dataset = [];
    let markers = [];
    let selected;

    // Static url until images are served from flask server
    let imgUrl = "https://images.podigee-cdn.net/0x,sw_d9izO9QfY97alR2f13b7IrOVeXM5gFZOjetk-5sTg=/https://cdn.podigee.com/uploads/u32412/b610d282-8f99-4604-a16f-28ada94ab76a.jpg";

    function selectEpisode(id) {
		if(id === selected) {
			selected = null;
		} else {
			selected = id;
		}
    }

	onMount(() => {
		episodes = data.episodes;
        episodes.forEach(ep => {
            let locations = ep.locations.map((loc) => {
                return {id: ep.id, longitude: loc.longitude, latitude: loc.latitude}
            });           
            markers = markers.concat(locations)
        })

        // ToDo move geojson to flask server/static files
		json(
			'https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson'
		).then((data) => {
			dataset = data.features;
		});

        console.log(episodes[0]);
	});
</script>

<main class="">
	<div class="flex-col w-screen h-screen bg-gray-50 place-items-center overflow-hidden">
		<h1 class="text-center text-3xl font-bold py-3">Karten aus der Geschichte</h1>
		<div class="w-full h-full relative overflow-hidden">
			<!-- World Map -->
			<div class="w-screen h-screen overflow-hidden">
				<svg class="w-full h-full" viewBox="0 0 1000 550" preserveAspectRatio="xMidYMin slice">
					{#each dataset as data}
						<path class="fill-gray-300 stroke-1" d={path(data)} />
					{/each}
					{#each markers as {id, longitude, latitude}}
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<line
							on:click={selectEpisode(id)}
							class="{selected === id ? 'stroke-5 stroke-gag-primary' : 'stroke-2 stroke-gray-600'} hover:stroke-4" stroke-linecap="round"
                            x1="{projection([longitude, latitude])[0]}"
                            x2="{projection([longitude, latitude])[0]+0.1}"
                            y1="{projection([longitude, latitude])[1]}"
                            y2="{projection([longitude, latitude])[1]+0.1}" 
						/>
					{/each}
				</svg>
			</div>
			<!-- Episode List -->
			<div id="list" class="flex items-center absolute right-0 bottom-5 lg:top-0 w-full lg:w-1/3 xl:w-1/4 h-1/2 lg:h-full">
				<div
					class="bg-gray-200 opacity-80 overflow-y-scroll h-5/6 m-3 p-3  scrollbar-thin rounded-xl scrollbar-thumb-gag-primary scrollbar-track-gray-400"
				>
					{#each episodes as episode (episode.id)}
						<div class="flex gap-2 border py-1">
							<!-- svelte-ignore a11y-click-events-have-key-events -->
							<img src={imgUrl} class="w-16 h-16 rounded-sm border border-gray-400 hover:cursor-pointer" alt="Thumbnail Picture Episode {episode.id}" on:click={selectEpisode(episode.id)} />
							<div class="flex-row">
								<!-- svelte-ignore a11y-click-events-have-key-events -->
								<span class="bg-gag-primary text-white px-2 py-1 rounded-md text-sm font-bold hover:cursor-pointer" on:click={selectEpisode(episode.id)}
                                >{episode.id}</span
								>
                                
								<!-- svelte-ignore a11y-click-events-have-key-events -->
								<div class="w-full">
									<span class="mb-1 inline-block text-small font-semibold hover:cursor-pointer" on:click={selectEpisode(episode.id)}>{episode.title.split(': ')[1]}</span
									><br />
								</div>
							</div>
						</div>
                        <div class="{selected === episode.id ? '' : 'hidden'} px-3">
                            <div class="location-tabs flex flex-wrap gap-2 text-sm">
								{#each episode.locations as loc}
								<span class="py-1 px-2 bg-white border border-gag-primary text-gag-primary rounded-lg">{loc.name}</span>
                                {/each}
                            </div>
							<span class="py-1 text-xs font-semibold">Veröffentlicht am {new Date(episode.published).toLocaleDateString('de-DE')}</span>
                            <p class="text-small">
                                {episode.summary}
                            </p>

                        </div>
					{/each}
				</div>
			</div>
		</div>
	</div>
</main>
