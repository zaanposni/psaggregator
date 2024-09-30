<script lang="ts">
    import type { PageServerData } from "./$types";
    import UploadPlanEntry from "$lib/components/UploadPlanEntry.svelte";
    import PSVideo from "$lib/components/PSVideo.svelte";
    import TwitchStatus from "$lib/components/TwitchStatus.svelte";
    import RedditPost from "$lib/components/RedditPost.svelte";
    import { List, VideoPlayer, LogoYoutube, LogoInstagram, LogoTwitter } from "carbon-icons-svelte";
    import YouTubeCommunityPost from "$lib/components/YouTubeCommunityPost.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import InstagramPost from "$lib/components/InstagramPost.svelte";
    import TwitchEntry from "$lib/components/TwitchEntry.svelte";
    import { version } from "$app/environment";
    import { Notification } from "carbon-icons-svelte";
    import * as Alert from "$lib/components/ui/alert/index.js";
    import TwitterPost from "$lib/components/TwitterPost.svelte";

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

<MediaQuery query="(min-width: 768px)" let:matches>
    <div class="dashboardcontainer p-4 md:p-8">
        <MediaQuery query="(min-width: 1280px)" let:matches>
            {#if !matches}
                <div class="mb-4 flex items-center justify-between">
                    <span class="text-xl font-bold">Version {version}</span>
                    <a href="/changelog">Was ist neu?</a>
                </div>
            {/if}
        </MediaQuery>

        <div class="flex flex-col-reverse gap-y-4 md:flex-row md:items-start md:gap-x-8 md:gap-y-0">
            <div class="shrink-0 grow">
                <div class="mb-2 ml-2 flex items-center text-2xl">
                    <List size={32} class="mr-2" />
                    Uploadplan
                </div>
                <div class="flex shrink-0 grow flex-col gap-2">
                    {#each data.today as content}
                        <UploadPlanEntry entry={content} />
                    {:else}
                        <div class="flex items-center mt-4">
                            <span>Bisher konnte heute kein Uploadplan importiert werden.</span>
                        </div>
                    {/each}
                </div>
            </div>
            {#if data.twitchStatus}
                <div class="flex w-full shrink-0 flex-col md:w-80">
                    <div class="mb-2 ml-2 flex items-center text-2xl">
                        <img alt="twitch" src="/twitch-logo.svg" class="mr-2 inline-block h-8 w-8" />
                        Twitch
                    </div>
                    <TwitchStatus twitch={data.twitchStatus} />
                </div>
            {/if}
        </div>
        <div class="grid grid-cols-1 gap-x-8 gap-y-4 md:grid-cols-2 md:gap-y-8 xl:grid-cols-5">
            <div class="order-2">
                <div class="mb-2 ml-2 flex items-center text-2xl">
                    <LogoYoutube size={32} class="mr-2" />
                    YouTube
                </div>
                <div class="flex flex-col gap-2">
                    {#each data.youtubeCommunityPosts as youtube}
                        <YouTubeCommunityPost post={youtube} />
                    {/each}
                </div>
            </div>
            <div class="order-3">
                <div class="mb-2 ml-2 flex items-center text-2xl">
                    <LogoInstagram size={32} class="mr-2" />
                    Instagram
                </div>
                <div class="flex flex-col gap-2">
                    {#each data.instagramPosts as instagram}
                        <InstagramPost post={instagram} />
                    {/each}
                </div>
            </div>
            <div class="order-4">
                <div class="mb-2 ml-2 flex items-center text-2xl">
                    <LogoTwitter size={32} class="mr-2" />
                    Twitter
                </div>
                <div class="flex flex-col gap-2">
                    {#each data.twitterPosts as twitter}
                        <TwitterPost post={twitter} />
                    {/each}
                </div>
            </div>
            <div class="order-1 md:order-5">
                <div class="mb-2 ml-2 flex items-center text-2xl">
                    <img alt="twitch" src="/twitch-logo.svg" class="mr-2 inline-block h-8 w-8" />
                    Anstehende Streams
                </div>
                <div class="flex flex-col gap-2">
                    {#each data.upcomingStreams as stream}
                        <TwitchEntry entry={stream} />
                    {:else}
                        <div class="flex items-center mt-4">
                            <span>Momentan sind keine geplanten Streams bekannt.</span>
                        </div>
                    {/each}
                </div>
            </div>
            <div class="order-6">
                <div class="mb-2 ml-2 flex items-center text-2xl">
                    <img alt="reddit" src="/reddit-logo.svg" class="mr-2 inline-block h-8 w-8" />
                    Reddit
                </div>
                <div class="flex flex-col gap-2">
                    {#each data.redditPosts.slice(0, matches ? 10 : 5) as reddit}
                        <RedditPost entry={reddit} />
                    {/each}
                </div>
            </div>
        </div>
        <div>
            <div class="mb-2 ml-2 flex items-center text-2xl">
                <VideoPlayer size={32} class="mr-2" />
                Neuste Videos
            </div>
            <div class="scrollable flex h-64 flex-row items-center gap-4 overflow-x-auto overflow-y-hidden">
                {#each data.videos as video}
                    <PSVideo {video} isSquare />
                {/each}
            </div>
        </div>
    </div>
</MediaQuery>
