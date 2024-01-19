<script lang="ts">
    import type { PageServerData } from "./$types";
    import UploadPlanEntry from "$lib/components/UploadPlanEntry.svelte";
    import PSVideo from "$lib/components/PSVideo.svelte";
    import TwitchStatus from "$lib/components/TwitchStatus.svelte";
    import RedditPost from "$lib/components/RedditPost.svelte";

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
    .dashboardcontainer > div:not(:first-child) {
        @apply mt-4;
    }

    @media (min-width: 768px) {
        .dashboardcontainer > div:not(:first-child) {
            @apply mt-8;
        }
    }
</style>

<div class="dashboardcontainer p-4 md:p-8">
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
    <div class="grid grid-cols-1 md:grid-cols-2">
        <div>
            <div class="mb-2 ml-2 flex items-center text-2xl">
                <img alt="reddit" src="/reddit-logo.svg" class="mr-2 inline-block h-8 w-8" />
                Reddit
            </div>
            <div class="flex flex-col">
                {#each data.redditPosts as reddit}
                    <RedditPost entry={reddit} />
                {/each}
            </div>
        </div>
    </div>
    <div class="scrollable flex h-64 flex-row items-center gap-4 overflow-x-auto">
        {#each data.videos as video}
            <PSVideo {video} />
        {/each}
    </div>
</div>
