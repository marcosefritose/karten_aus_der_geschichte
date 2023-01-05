import { writable } from 'svelte/store';

export const locations = writable([])
export const episodes = writable([])

export function setLocations(locationsData) {
    locations.update(state => [...locationsData])
}

export function setEpisodes(episodesData) {
    episodes.update(state => [...episodesData])
}