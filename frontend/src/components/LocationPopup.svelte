<script>
    export let coords;

    $: ({x, y} = coords)
</script>


<div class="absolute w-32 h-32 bg-green-300" style="left: {x}px; top: {y}px">
    Location
</div>