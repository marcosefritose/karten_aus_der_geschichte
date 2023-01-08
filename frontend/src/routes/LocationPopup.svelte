<script>
	import { onMount } from "svelte";
    import { setSelectedEpisodeById } from "./store";

    export let coords;
    export let location;
    export let showPopup;
    export let locationClicked;

    let popup;
    let left = 0;
    let top = 0;


    $: ({x, y} = coords)
    $: updatePostion(x, y)

    function clickOutside(node) {
		const handleClick = event => {
			if (node && !node.contains(event.target) && !event.defaultPrevented) {
			node.dispatchEvent(
				new CustomEvent('click_outside', node)
			)
			}
		}

			document.addEventListener('click', handleClick, true);
		
		return {
			destroy() {
				document.removeEventListener('click', handleClick, true);
			}
		}
	}

    function disablePopup() {
        showPopup = false; 
        locationClicked = false;
    }

    function updatePostion(x,y) {
        if(!popup) return false

        left = x - (popup.offsetWidth / 2)
        
        if(left < 0) {
            left = 0
        } else if(left > (innerWidth - popup.offsetWidth)) {
            console.log('shrink');
            left = innerWidth - popup.offsetWidth
        }

        if(innerHeight / 2 < y + popup.offsetHeight) {
            top = y - popup.offsetHeight - 15
        } else {
            top = y + 15
        }            
    }

    onMount(() => {
        updatePostion(x,y)
    })
</script>


<div 
    bind:this={popup}
    use:clickOutside 
    on:click_outside={disablePopup}
    class="absolute bg-gray-300 bg-opacity-80 w-64 sm:w-96 rounded-md border border-gag-primary m-1 z-20" 
    style="left: {left}px; top: {top}px"
>
    <p class="text-center text-lg font-semibold py-2">{location.name}</p>
    <ul class="pb-1 px-2 max-h-48 overflow-y-scroll scrollbar-thin scrollbar-thumb-gag-primary scrollbar-track-gray-400">
        {#each location.episodes as episode, id}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <li class="mb-2 cursor-pointer flex gap-1" on:click={setSelectedEpisodeById(episode.id)}>
                <span class="bg-gag-primary inline-block text-white px-2 py-1 rounded-md font-bold text-xs h-fit">{episode.id}</span>{episode.title}
            </li>
        {/each}
    </ul>
</div>