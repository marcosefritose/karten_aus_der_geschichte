export async function load({ fetch, setHeaders }) {
    const res = await fetch(`https://marcose.pythonanywhere.com/episodes/`)
    const data = await res.json()


    return {
        episodes: data,
    }
}