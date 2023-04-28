export async function load({ fetch, setHeaders }) {
    const locationsRes = await fetch('http://flask:5000/locations/')
    const locationData = await locationsRes.json()

    return {
        locations: locationData
    }
}