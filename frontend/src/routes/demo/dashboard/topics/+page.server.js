export async function load({ fetch, setHeaders }) {
    const externalApiUrl = import.meta.env.VITE_FLASK_API_URL;

    const topicsRes = await fetch(`${externalApiUrl}/topics/`)
    const topicData = await topicsRes.json()

    return {
        topics: topicData
    }
}