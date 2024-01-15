<script lang="ts">
    import type { PageServerData } from "./$types";
    import UploadPlanEntry from "$lib/components/UploadPlanEntry.svelte";

    export let data: PageServerData;
</script>

<div class="p-8">
    <div class="flex flex-col">
        {#each data.today as content}
            <UploadPlanEntry entry={content} />
        {/each}
    </div>
    <hr class="my-12 !border-t-4" />
</div>
