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
    interpolateYlOrBr
  } from 'd3';

  import LocationPopup from './LocationPopup.svelte';
  import { locations, selectedLocations, setSelectedLocations, popupSelection } from './store';
  import AreaPopup from './AreaPopup.svelte';

  let selectedLocationsNames;

  let mapFeatureData = [];
  let markerElements = {};
  let markerPositions = [];

  let historicMapFeatureData = [];
  let historicMapFeatureNames = [];
  let historicMapFeaturePaths;

  // ToDo: Used for debuggin polygon geofeature - remove if prod
  // let geoFeaturePath = null;

  // D3 Porjection, Path & Zoom variables
  const projection = geoNaturalEarth1();
  const path = geoPath(projection);
  let bindHandleZoom, bindInitZoom;

  let popupLocation;
  let popupLocationPosition;
  let popupArea;
  let popupAreaPosition;
  let locationClicked = false;
  let locationPopupIsShown = false;
  let areaPopupIsShown = false;

  // Get screen size and update positions for new screen size
  let innerWidth = 0;
  let innerHeight = 0;

  $: if (innerHeight || innerWidth) {
    updateMarkerPositions();
  }

  function getGeoFeatureForLocations(locs) {
    locs = locs.filter((loc) => {
      return loc.latitude !== 'NaN';
    });

    if (locs.length == 0) return false;

    let coordinates = locs.map((coord) => [
      parseFloat(coord.longitude),
      parseFloat(coord.latitude)
    ]);

    // Sort by longitude to prevent unsortable coords for polygon
    coordinates = coordinates.sort((a, b) => a[0] - b[0]);

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
    selectedLocationsNames = selectedLocs.map((loc) => loc.name);

    let geoFeature = getGeoFeatureForLocations(selectedLocs);

    if (geoFeature) {
      // geoFeaturePath = path(geoFeature)
      clicked(geoFeature);
    }
  });

  $: if (markerElements) {
    updateMarkerPositions();
  }

  function showLocationPopup(event, locationName) {
    if ($popupSelection !== 'location') {
      return false;
    }

    popupLocation = $locations.filter((loc) => loc['name'] == locationName)[0];
    popupLocationPosition = markerElements[locationName].getBoundingClientRect();
    locationPopupIsShown = true;

    if (event.type == 'click') {
      setSelectedLocations([popupLocation]);
      locationClicked = true;
    }
  }

  function showAreaPopup(event, areaName) {
    if ($popupSelection !== 'area') {
      return false;
    }

    popupArea = areaName;
    popupAreaPosition = { x: event.clientX, y: event.clientY };
    areaPopupIsShown = true;
  }

  function updateMarkerPositions() {
    let updatedMarkerPostions = [];

    for (let name in markerElements) {
      let { x, y } = markerElements[name].getBoundingClientRect();
      updatedMarkerPostions.push({ name: name, x: x, y: y });
    }

    markerPositions = updatedMarkerPostions;
  }

  // Zoom and scroll functionality
  $: zoomX = zoom().scaleExtent([1, 8]).on('zoom', handleZoom);
  $: if (bindInitZoom) {
    select(bindInitZoom).call(zoomX);
  }

  function handleZoom(e) {
    select(bindHandleZoom).attr('transform', e.transform);
    updateMarkerPositions();
    if (popupLocation && locationPopupIsShown) {
      popupLocationPosition = markerElements[popupLocation.name].getBoundingClientRect();
    }
  }

  function clicked(d) {
    const [[x0, y0], [x1, y1]] = path.bounds(d);

    // TODO: Zoom factor more dynamic?
    let zoomFactor = innerWidth < 600 ? 0.3 : 0.8;

    select(bindInitZoom)
      .transition()
      .duration(750)
      .call(
        zoomX.transform,
        zoomIdentity
          .translate(1000 / 2, 500 / 2)
          // ToDo: Zoom factor depending on screen size!
          .scale(Math.min(6, zoomFactor / Math.max((x1 - x0) / 1000, (y1 - y0) / 500)))
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

    json('historic-maps/world_100.geojson').then((data) => {
      historicMapFeatureData = data.features;
      historicMapFeatureData = historicMapFeatureData.filter((d) => d.properties.NAME != null);
      historicMapFeatureNames = [...new Set(historicMapFeatureData.map((d) => d.properties.NAME))];

      setTimeout(() => {
        for (let areaPath of historicMapFeaturePaths.children) {
          areaPath.addEventListener('mouseenter', (e) => {
            showAreaPopup(e, areaPath.getAttribute('data-name'));
          });
          areaPath.addEventListener('mouseleave', (e) => {
            areaPopupIsShown = false;
          });
        }
      }, 20);
    });
  });
</script>

<svelte:window bind:innerWidth bind:innerHeight />

<!-- World Map -->
<svg
  id="world-map"
  class="h-full w-full bg-slate-600"
  viewBox="0 0 1000 500"
  preserveAspectRatio="xMidYMid slice"
  bind:this={bindInitZoom}
>
  <g class="countries" bind:this={bindHandleZoom}>
    <g class="select-none">
      {#each mapFeatureData as data}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <path id={data.id} class="select-none fill-gray-300 stroke-1" d={path(data)} />
      {/each}
    </g>
    <g class="historic-areas z-50" bind:this={historicMapFeaturePaths}>
      {#each historicMapFeatureData as data}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <path
          data-name={data.properties.NAME}
          class="historic-path z-50 stroke-1 opacity-30"
          d={path(data)}
          fill={interpolateYlOrBr(
            historicMapFeatureNames.indexOf(data.properties.NAME) / historicMapFeatureNames.length
          )}
        />
      {/each}
    </g>

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
  {#each markerPositions as { name, x, y }}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div
      class="absolute rounded-full
					{selectedLocationsNames.includes(name)
        ? 'animate-pulse-slow bg-gag-primary z-10 h-2 w-2'
        : 'hover:bg-gag-primary h-2 w-2 border-[0.1px] border-gray-300 bg-gray-600 hover:scale-150'}"
      style="left: {x - 2}px; top: {y - 2}px"
      on:click={(e) => showLocationPopup(e, name)}
      on:mouseenter|once={(e) => (locationClicked ? null : showLocationPopup(e, name))}
      on:mouseleave={(e) => {
        locationClicked ? null : (locationPopupIsShown = false);
        e.target.addEventListener(
          'mouseenter',
          (e) => (locationClicked ? null : showLocationPopup(e, name)),
          { once: true }
        );
      }}
    >
      <!-- Possible slot for location SVG's -->
    </div>
  {/each}
</div>

<!-- Location Popup -->
{#if locationPopupIsShown}
  <LocationPopup
    bind:location={popupLocation}
    bind:coords={popupLocationPosition}
    bind:locationPopupIsShown
    bind:locationClicked
  />
{/if}

<!-- Area Popup -->
{#if areaPopupIsShown}
  <AreaPopup bind:area={popupArea} bind:coords={popupAreaPosition} />
{/if}
