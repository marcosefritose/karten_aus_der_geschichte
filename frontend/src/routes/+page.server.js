export const load = async () => {
    console.log('Server Load Ran')
    
    const fetchEpisodes = async () => {
        const res = await fetch(`http://127.0.0.1:5000/episodes/`)
        const data = await res.json()
        console.log(data[0]);
        return data
    }

    return {
        episodes: fetchEpisodes(),
    }
}