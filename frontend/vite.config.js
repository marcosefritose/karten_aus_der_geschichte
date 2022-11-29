import { sveltekit } from '@sveltejs/kit/vite';
import json from '@rollup/plugin-json'  

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()]
};

export default config;
