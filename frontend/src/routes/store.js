import { writable, get } from 'svelte/store';

export const locations = writable([])
export const episodes = writable([])
export const topics = writable([])
export const selectedEpisode = writable({})
export const selectedLocations = writable([])
export const selectedTime = writable({ year: 100, file: 'historic-maps/world_100.geojson' })
export const showHistoricMap = writable(false)

export const maps = [
    // { year: -123000, file: 'historic-maps/world_bc123000.geojson' },
    // { year: -10000, file: 'historic-maps/world_bc10000.geojson' },
    { year: -8000, file: 'historic-maps/world_bc8000.geojson' },
    { year: -5000, file: 'historic-maps/world_bc5000.geojson' },
    { year: -4000, file: 'historic-maps/world_bc4000.geojson' },
    { year: -3000, file: 'historic-maps/world_bc3000.geojson' },
    { year: -2000, file: 'historic-maps/world_bc2000.geojson' },
    { year: -1500, file: 'historic-maps/world_bc1500.geojson' },
    { year: -1000, file: 'historic-maps/world_bc1000.geojson' },
    { year: -700, file: 'historic-maps/world_bc700.geojson' },
    { year: -500, file: 'historic-maps/world_bc500.geojson}' },
    { year: -400, file: 'historic-maps/world_bc400.geojson' },
    { year: -323, file: 'historic-maps/world_bc323.geojson' },
    { year: -300, file: 'historic-maps/world_bc300.geojson' },
    { year: -200, file: 'historic-maps/world_bc200.geojson' },
    { year: -100, file: 'historic-maps/world_bc100.geojson' },
    { year: -1, file: 'historic-maps/world_bc1.geojson' },
    { year: 100, file: 'historic-maps/world_100.geojson' },
    { year: 200, file: 'historic-maps/world_200.geojson' },
    { year: 300, file: 'historic-maps/world_300.geojson' },
    { year: 400, file: 'historic-maps/world_400.geojson' },
    { year: 500, file: 'historic-maps/world_500.geojson' },
    { year: 600, file: 'historic-maps/world_600.geojson' },
    { year: 700, file: 'historic-maps/world_700.geojson' },
    { year: 800, file: 'historic-maps/world_800.geojson' },
    { year: 900, file: 'historic-maps/world_900.geojson' },
    { year: 1000, file: 'historic-maps/world_1000.geojson' },
    { year: 1100, file: 'historic-maps/world_1100.geojson' },
    { year: 1200, file: 'historic-maps/world_1200.geojson' },
    { year: 1279, file: 'historic-maps/world_1279.geojson' },
    { year: 1300, file: 'historic-maps/world_1300.geojson' },
    { year: 1400, file: 'historic-maps/world_1400.geojson' },
    { year: 1492, file: 'historic-maps/world_1492.geojson' },
    { year: 1500, file: 'historic-maps/world_1500.geojson' },
    { year: 1530, file: 'historic-maps/world_1530.geojson' },
    { year: 1600, file: 'historic-maps/world_1600.geojson' },
    { year: 1650, file: 'historic-maps/world_1650.geojson' },
    { year: 1700, file: 'historic-maps/world_1700.geojson' },
    { year: 1715, file: 'historic-maps/world_1715.geojson' },
    { year: 1783, file: 'historic-maps/world_1783.geojson' },
    { year: 1800, file: 'historic-maps/world_1800.geojson' },
    { year: 1815, file: 'historic-maps/world_1815.geojson' },
    { year: 1880, file: 'historic-maps/world_1880.geojson' },
    { year: 1900, file: 'historic-maps/world_1900.geojson' },
    { year: 1914, file: 'historic-maps/world_1914.geojson' },
    { year: 1920, file: 'historic-maps/world_1920.geojson' },
    { year: 1938, file: 'historic-maps/world_1938.geojson' },
    { year: 1945, file: 'historic-maps/world_1945.geojson' },
    { year: 1960, file: 'historic-maps/world_1960.geojson' },
    { year: 1994, file: 'historic-maps/world_1994.geojson' }
]

export function setLocations(locationsData) {
    locations.update(state => [...locationsData])
}

export function setEpisodes(episodesData) {
    episodes.update(state => [...episodesData])
}

export function setTopics(topicsData) {
    topics.update(state => [...topicsData])
}

export function setSelectedEpisodeById(episodeId) {
    if (episodeId == null) {
        selectedEpisode.update(state => { return {} })
        return
    }

    let episodesValue = get(episodes)
    let episode = episodesValue.filter((ep) => ep['id'] == episodeId)[0]

    if (episode.story_time_start != undefined) {
        let filteredMaps = maps.filter((m) => m.year < episode.story_time_start);
        let sortedMaps = filteredMaps.sort((a, b) => b.year - a.year);
        setSelectedTime(sortedMaps[0]);
    }

    selectedEpisode.update(state => episode)
    selectedLocations.update(state => [...episode.locations]);
}

export function setSelectedLocations(newSelectedLocations) {
    console.log(newSelectedLocations);
    selectedLocations.update(state => [...newSelectedLocations]);
}

export function setSelectedTime(newTime) {
    selectedTime.update(state => newTime)
}

export function setShowHistoricMaps(show) {
    showHistoricMap.update(state => show)
}