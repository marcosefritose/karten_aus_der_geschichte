import { redirect } from '@sveltejs/kit';

export function load({ page, fetch }) {
    throw redirect(307, '/demo/dashboard/episodes');
}