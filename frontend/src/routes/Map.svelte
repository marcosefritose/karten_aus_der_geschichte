<script>
    import { onMount } from 'svelte';
    import { polygon, rewind } from '@turf/turf';
    import {
		json,
		geoPath,
		zoom,
		zoomIdentity,
		select,
		geoNaturalEarth1,
		geoMercator
	} from 'd3';

    import LocationPopup from './LocationPopup.svelte';
    
    export let locations;
    export let selectedLocations;
    let selectedLocationsNames;

    let mapFeatureData = [];
    let locationPositions = {};

    // D3 Porjection, Path & Zoom variables
	const projection = geoNaturalEarth1();
	const path = geoPath(projection);
	let bindHandleZoom, bindInitZoom;

    let popupLocation;
	let popupLocationPosition;
	let showPopup = false;


    function getGeoFeatureForLocations(locations) {
		locations = locations.filter((loc) => {
			return loc.latitude !== 'NaN'
		})
		
		if(locations.length == 0){
			return false
		}

		let coordinates = locations.map((coord) => [parseFloat(coord.longitude), parseFloat(coord.latitude)]);
		
		// Set end equal to start coordinate and fill until atleast 4 coords present
		coordinates.push(coordinates[0]);
		while (coordinates.length < 4) {
			coordinates.push(coordinates[0]);
		}
		
		// Create geojson Feature and order the coordinates clockwise
		let polygonFeatureRaw = polygon([coordinates]);
		let polygonFeature = rewind(polygonFeatureRaw, { reverse: true });
		
		return polygonFeature;
	}

    // Detect selection changes and adjust map
    $: if(selectedLocations) {
        selectedLocationsNames = selectedLocations.map((loc) => loc.name)

        let geoFeature = getGeoFeatureForLocations(selectedLocations)
        if(geoFeature) {
            clicked(geoFeature);
        }
    }

    // Zoom and scroll functionality
	$: zoomX = zoom().scaleExtent([1, 4]).on('zoom', handleZoom);
	$: if (bindInitZoom) {
		select(bindInitZoom).call(zoomX);
	}


	function handleZoom(e) {
		select(bindHandleZoom).attr('transform', e.transform);
		if(popupLocation && showPopup) {
			popupLocationPosition = locationPositions[popupLocation].getBoundingClientRect()
		}
	}

    function showLocationPopup(event, name) {
		popupLocation = name
		popupLocationPosition = locationPositions[name].getBoundingClientRect()
		showPopup = true
	}

	function clicked(d) {
		const [[x0, y0], [x1, y1]] = path.bounds(d);

		select(bindInitZoom)
			.transition()
			.duration(750)
			.call(
				zoomX.transform,
				zoomIdentity
					.translate(1000 / 2, 500 / 2)
					// ToDo: Zoom factor depending on screen size!
					.scale(Math.min(4, 0.5 / Math.max((x1 - x0) / 1000, (y1 - y0) / 500)))
					.translate(-(x0 + x1) / 2, -(y0 + y1) / 2)
			);
	}

    onMount(() => {
		// ToDo move geojson to flask server/static files
		json(
			'https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson'
		).then((data) => {
			mapFeatureData = data.features;
		});

	});
</script>

<!-- World Map -->
<svg
    id="world-map"
    class="w-full h-full bg-slate-600"
    viewBox="0 0 1000 500"
    preserveAspectRatio="xMidYMid slice"
    bind:this={bindInitZoom}
>
    <g class="countries" bind:this={bindHandleZoom}>
        {#each mapFeatureData as data}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <path id={data.id} class="fill-gray-300 stroke-1" d={path(data)} />
        {/each}
        {#each locations as { name, longitude, latitude }}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <line
                id={name}
                bind:this={locationPositions[name]}
                on:mouseenter={(e) => showLocationPopup(e, name)}
                on:mouseleave={() => showPopup = false}
                class="{selectedLocationsNames.includes(name)
                    ? 'stroke-5 stroke-gag-primary'
                    : 'stroke-2 stroke-gray-600'} hover:stroke-4"
                stroke-linecap="round"
                x1={projection([longitude, latitude])[0]}
                x2={projection([longitude, latitude])[0] + 0.1}
                y1={projection([longitude, latitude])[1]}
                y2={projection([longitude, latitude])[1] + 0.1}
            />
        {/each}
    </g>
</svg>

<!-- Location Popup -->
{#if showPopup}
    <LocationPopup bind:location={popupLocation} bind:coords={popupLocationPosition} />
{/if}