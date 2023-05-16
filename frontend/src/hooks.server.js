export async function handleFetch({ request, fetch }) {
    const externalApiUrl = import.meta.env.VITE_FLASK_API_URL;

    if (request.url.startsWith(externalApiUrl)) {
        request = new Request(
            request.url.replace(externalApiUrl, 'http://flask:5000'),
            request
        );

        console.log('Server replaced URL');
    }

    return fetch(request);
}