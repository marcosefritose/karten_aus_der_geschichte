import { writable, get } from 'svelte/store';

export const locations = writable([])
export const episodes = writable([])
export const selectedEpisode = writable({})
export const selectedLocations = writable([])
export const popupSelection = writable('location')

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
    console.log(get(selectedLocations));
    selectedLocations.update(state => [...episode.locations]);
    console.log(get(selectedLocations));
}

export function setSelectedLocations(newSelectedLocations) {
    selectedLocations.update(state => [...newSelectedLocations]);
}

export function setPopupSelection(selection) {
    popupSelection.update(state => selection)
}