import { setEpisodes, setLocations } from "../store"

export async function load({ fetch, setHeaders }) {
    const externalApiUrl = import.meta.env.VITE_FLASK_API_URL;

    const episodesRes = await fetch(`${externalApiUrl}/episodes/`)
    const episodeData = await episodesRes.json()

    const locationsRes = await fetch(`${externalApiUrl}/locations/?hasCoordinate=true`)
    const locationData = await locationsRes.json()

    setEpisodes(episodeData)
    setLocations(locationData)
}