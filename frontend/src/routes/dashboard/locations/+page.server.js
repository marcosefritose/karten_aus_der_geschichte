export async function load({ fetch, setHeaders }) {
    const externalApiUrl = import.meta.env.VITE_FLASK_API_URL;

    const locationsRes = await fetch(`${externalApiUrl}/locations/`)
    const locationData = await locationsRes.json()

    return {
        locations: locationData
    }
}