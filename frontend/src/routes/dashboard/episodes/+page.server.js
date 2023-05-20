
export async function load({ fetch, setHeaders }) {
    const externalApiUrl = import.meta.env.VITE_FLASK_API_URL;

    const episodesRes = await fetch(`${externalApiUrl}/episodes/`)
    const episodeData = await episodesRes.json()

    return {
        episodes: episodeData
    }
}