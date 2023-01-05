<script>
    import { createEventDispatcher, onMount } from 'svelte';
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
	import { locations, selectedLocations, setSelectedLocations } from './store';
    
    let selectedLocationsNames;

    let mapFeatureData = [];
    let markerElements = {};
    let markerPositions = [];

	// ToDo: Used for debuggin polygon geofeature - remove if prod
	// let geoFeaturePath = null;

    // D3 Porjection, Path & Zoom variables
	const projection = geoNaturalEarth1();
	const path = geoPath(projection);
	let bindHandleZoom, bindInitZoom;

    let popupLocation;
	let popupLocationPosition;
	let locationClicked = false;
	let showPopup = false;

	// Get screen size and update positions for new screen size
	let innerWidth = 0
    let innerHeight = 0
    
    $: if(innerHeight || innerWidth) {
		updateMarkerPositions()
	}

    function getGeoFeatureForLocations(locs) {
		locs = locs.filter((loc) => {
			return loc.latitude !== 'NaN'
		})
		
		if(locs.length == 0) return false

		let coordinates = locs.map((coord) => [parseFloat(coord.longitude), parseFloat(coord.latitude)]);

		// Sort by longitude to prevent unsortable coords for polygon
		coordinates = coordinates.sort((a, b) => a[0] - b[0])

		// Set end equal to start coordinate and fill until atleast 4 coords present
		coordinates.push(coordinates[0]);
		while (coordinates.length < 4) {
			coordinates.push(coordinates[0]);
		}
		
		// Create geojson Feature and order the coordinates clockwise
		let polygonFeatureRaw = polygon([coordinates]);
		let polygonFeature = rewind(polygonFeatureRaw, { reverse: true, mutate: true });
		return polygonFeature;
	}

    // Detect selection changes and adjust map
    selectedLocations.subscribe((selectedLocs) => {
        selectedLocationsNames = selectedLocs.map((loc) => loc.name)

        let geoFeature = getGeoFeatureForLocations(selectedLocs)
		
        if(geoFeature) {
			// geoFeaturePath = path(geoFeature)
			clicked(geoFeature);
        }
    })
	
	$: if (markerElements) {
		updateMarkerPositions()
	}

	function showLocationPopup(event, locationName) {
		popupLocation = $locations.filter((loc) => loc['name'] == locationName)[0]
		popupLocationPosition = markerElements[locationName].getBoundingClientRect()
		showPopup = true

		if(event.type == 'click') {
			setSelectedLocations([popupLocation])
			locationClicked = true;
		}

	}
	
	function updateMarkerPositions() {
		let updatedMarkerPostions = []
		
		for (let name in markerElements) {
			let {x, y} = markerElements[name].getBoundingClientRect()
			updatedMarkerPostions.push({'name': name, 'x': x, 'y': y})
		}
		
		markerPositions = updatedMarkerPostions
	}
	
	// Zoom and scroll functionality
	$: zoomX = zoom().scaleExtent([1, 8]).on('zoom', handleZoom);
	$: if (bindInitZoom) {
		select(bindInitZoom).call(zoomX);
	}
	
	function handleZoom(e) {
		select(bindHandleZoom).attr('transform', e.transform);
		updateMarkerPositions()
		if(popupLocation && showPopup) {
			popupLocationPosition = markerElements[popupLocation.name].getBoundingClientRect()
		}
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
					.scale(Math.min(6, 0.8 / Math.max((x1 - x0) / 1000, (y1 - y0) / 500)))
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

<svelte:window bind:innerWidth bind:innerHeight />

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
		{#if $locations}
			 {#each $locations as location}
				 <!-- svelte-ignore a11y-click-events-have-key-events -->
				 <line
					 id={location.name}
					 bind:this={markerElements[location.name]}
					 class="stroke-1"
					 x1={projection([location.longitude, location.latitude])[0]}
					 x2={projection([location.longitude, location.latitude])[0] + 0.1}
					 y1={projection([location.longitude, location.latitude])[1]}
					 y2={projection([location.longitude, location.latitude])[1] + 0.1}
				 />
			 {/each}
		{/if}
		<!-- {#if geoFeaturePath}
			<path class="fill-red stroke-3" d={geoFeaturePath}></path>
		{/if} -->
    </g>
</svg>

<div id="marker-wrapper" class="overflow-hidden">
{#each markerPositions as {name, x, y}}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div 
			class="absolute rounded-full
					{selectedLocationsNames.includes(name)
						? 'bg-gag-primary w-2 h-2 z-10 animate-pulse-slow'
						: 'bg-gray-600 w-2 h-2 hover:scale-150 hover:bg-gag-primary border-gray-300 border-[0.1px]'}"
			style="left: {x-2}px; top: {y-2}px"
			on:click={(e) => showLocationPopup(e, name)}
			on:mouseenter|once={(e) => locationClicked ? null : showLocationPopup(e, name)}
			on:mouseleave={(e) => {
				locationClicked ? null : showPopup = false
				e.target.addEventListener('mouseenter', (e) => locationClicked ? null : showLocationPopup(e, name), {once: true})
			}}
		>
			<!-- Possible slot for location SVG's -->
		</div>
		{/each}
</div>

<!-- Location Popup -->
{#if showPopup}
    <LocationPopup bind:location={popupLocation} bind:coords={popupLocationPosition} bind:showPopup bind:locationClicked />
{/if}