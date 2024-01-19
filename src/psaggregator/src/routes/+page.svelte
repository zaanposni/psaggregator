<script lang="ts">
    import type { PageServerData } from "./$types";
    import UploadPlanEntry from "$lib/components/UploadPlanEntry.svelte";
    import PSVideo from "$lib/components/PSVideo.svelte";
    import TwitchStatus from "$lib/components/TwitchStatus.svelte";

    export let data: PageServerData;
</script>

<style lang="postcss">
    .scrollable {
        overflow-x: auto;
        scrollbar-width: none; /* For Firefox */
        -ms-overflow-style: none; /* For Internet Explorer and Edge */
    }
    .scrollable::-webkit-scrollbar {
        width: 0px; /* For Chrome, Safari, and Opera */
    }
</style>

<div class="p-4 md:p-8">
    <div class="flex flex-col-reverse gap-y-4 md:flex-row md:items-start md:gap-x-8 md:gap-y-0">
        <div class="flex shrink-0 grow flex-col">
            {#each data.today as content}
                <UploadPlanEntry entry={content} />
            {/each}
        </div>
        {#if data.twitchStatus}
            <TwitchStatus twitch={data.twitchStatus} />
        {/if}
    </div>
    <div class="scrollable mt-4 flex h-64 flex-row items-center gap-4 overflow-x-auto md:mt-8">
        {#each data.videos as video}
            <PSVideo {video} />
        {/each}
    </div>
</div>
