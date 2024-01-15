<script lang="ts">
    import type { PageServerData } from "./$types";
    import UploadPlanEntry from "$lib/components/UploadPlanEntry.svelte";
    import PSVideo from "$lib/components/PSVideo.svelte";

    export let data: PageServerData;
</script>

<div class="p-8">
    <div class="flex flex-col">
        {#each data.today as content}
            <UploadPlanEntry entry={content} />
        {/each}
    </div>
    <hr class="my-8 !border-t-4" />
    <div class="flex h-64 flex-row items-center gap-4 overflow-x-auto">
        {#each data.videos as video}
            <PSVideo {video} />
        {/each}
    </div>
</div>
