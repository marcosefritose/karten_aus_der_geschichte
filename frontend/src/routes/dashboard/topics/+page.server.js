export async function load({ fetch, setHeaders }) {
    const topicsRes = await fetch('http://flask:5000/topics/')
    const topicData = await topicsRes.json()

    return {
        topics: topicData
    }
}