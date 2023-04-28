export async function load({ fetch, setHeaders }) {
    const episodesRes = await fetch('http://flask:5000/episodes/')
    const episodeData = await episodesRes.json()

    return {
        episodes: episodeData
    }
}