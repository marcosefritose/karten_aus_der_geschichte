export async function load({ fetch, setHeaders }) {
    const res = await fetch(`http://flask:5000/episodes/`)
    const data = await res.json()


    return {
        episodes: data,
    }
}