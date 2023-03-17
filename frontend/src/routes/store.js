import { writable, get } from 'svelte/store';

export const locations = writable([])
export const episodes = writable([])
export const selectedEpisode = writable({})
export const selectedLocations = writable([])
export const selectedTime = writable({ year: 100, file: 'historic-maps/world_100.geojson' })
export const showHistoricMap = writable(false)

export function setLocations(locationsData) {
    locations.update(state => [...locationsData])
}

export function setEpisodes(episodesData) {
    episodes.update(state => [...episodesData])
}

export function setSelectedEpisodeById(episodeId) {
    let episodesValue = get(episodes)
    let episode = episodesValue.filter((ep) => ep['id'] == episodeId)[0]

    selectedEpisode.update(state => episode)
    selectedLocations.update(state => [...episode.locations]);
}

export function setSelectedLocations(newSelectedLocations) {
    selectedLocations.update(state => [...newSelectedLocations]);
}

export function setSelectedTime(newTime) {
    selectedTime.update(state => newTime)
}

export function setShowHistoricMaps(show) {
    showHistoricMap.update(state => show)
}