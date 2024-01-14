<script lang="ts">
	import type { PageServerData } from "./$types";
    import { ProgressBar } from '@skeletonlabs/skeleton';

    export let data: PageServerData;
</script>

Hello World


<ProgressBar label="Progress Bar" value={50} max={100} />

{#each data.contentPieces as content}
    <div>
        <p>{content.id}</p>
    </div>
{/each}
