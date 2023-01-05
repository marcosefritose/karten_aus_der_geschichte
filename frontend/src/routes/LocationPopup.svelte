<script>
	import { onMount } from "svelte";


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
        console.log('update');
        if(popup) {
            console.log(popup.offsetWidth);
            console.log(innerWidth);
            left = x - popup.offsetWidth / 2
            
            if(left < 0) {
                left = 0
            } else if(left > innerWidth) {
                left = innerWidth - popup.offsetWidth
            }

            if(innerHeight < y + popup.offsetWidth) {
                top = y - popup.offsetHeight - 15
            } else {
                top = y + 15
            }            
        }
    }

    onMount(() => {
        updatePostion(x,y)
    })
</script>


<div 
    bind:this={popup}
    use:clickOutside on:click_outside={() => disablePopup()}
    class="absolute bg-gray-300 max-w-sm rounded-md border border-gray-900 m-1" 
    style="left: {left}px; top: {top}px"
>
    <p class="text-center text-lg font-semibold py-1">{location.name}</p>
    <ul class="p-1">
        {#each location.episodes as episode, id}
            <li class="pb-1"><span class="font-bold">{episode.id}</span>: {episode.title}</li>
        {/each}
    </ul>
</div>