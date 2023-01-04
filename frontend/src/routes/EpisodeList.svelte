<script>
    export let episodes;
    export let selected;
    export let selectedLocations;
    
    // ToDo: Static url until images are served from flask server
	let imgUrl =
		'https://images.podigee-cdn.net/0x,sw_d9izO9QfY97alR2f13b7IrOVeXM5gFZOjetk-5sTg=/https://cdn.podigee.com/uploads/u32412/b610d282-8f99-4604-a16f-28ada94ab76a.jpg';

    function selectEpisode(episode) {
		if (episode.id === selected) {
			selected = null;
			selectedLocations = [];
		} else {
			selected = episode.id;
			selectedLocations = [...episode.locations];
		}
		
		let listEntry = document.getElementById(episode.id);
		setTimeout(() => {
			listEntry.scrollIntoView({
				behavior: 'smooth'
			});
		}, 1);
	}
</script>

<div
    id="list"
    class="flex items-center absolute right-0 bottom-0 lg:top-0 w-full lg:w-1/3 xl:w-1/4 2xl:w-1/5 h-2/5 lg:h-full pointer-events-none"
    >
    <div
        class="bg-gray-200 opacity-80 overflow-y-scroll h-full md:h-5/6 my-3 p-3  scrollbar-thin rounded-xl scrollbar-thumb-gag-primary scrollbar-track-gray-400 pointer-events-auto"
    >
        {#each episodes as episode (episode.id)}
            <div id={episode.id} class="flex gap-2 border py-1">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <img
                    src={imgUrl}
                    class="w-16 h-16 rounded-sm border border-gray-400 hover:cursor-pointer"
                    alt="Thumbnail Picture Episode {episode.id}"
                    on:click={selectEpisode(episode)}
                />
                <div class="flex-row">
                    <!-- svelte-ignore a11y-click-events-have-key-events -->
                    <span
                        class="bg-gag-primary text-white px-2 py-1 rounded-md text-sm font-bold hover:cursor-pointer"
                        on:click={selectEpisode(episode)}>{episode.id}</span
                    >

                    <!-- svelte-ignore a11y-click-events-have-key-events -->
                    <div class="w-full">
                        <span
                            class="mb-1 inline-block text-small font-semibold hover:cursor-pointer"
                            on:click={selectEpisode(episode)}>{episode.title}</span
                        ><br />
                    </div>
                </div>
            </div>
            <div class="{selected === episode.id ? '' : 'hidden'} px-3">
                <div class="location-tabs flex flex-wrap gap-2 text-sm">
                    {#each episode.locations as loc}
                        <span
                            class="py-1 px-2 bg-white border border-gag-primary text-gag-primary rounded-lg"
                            >{loc.name}</span
                        >
                    {/each}
                </div>
                <span class="py-1 text-xs font-semibold"
                    >Veröffentlicht am {new Date(episode.published).toLocaleDateString('de-DE')}</span
                >
                <p class="text-small">
                    {episode.summary}
                </p>
            </div>
        {/each}
    </div>
</div>