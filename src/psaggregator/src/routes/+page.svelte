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
    import { browser, version } from "$app/environment";
    import TwitterPost from "$lib/components/TwitterPost.svelte";
    import { GITHUB_URL, LOW_DATA_MODE, MAIL_TO_URL } from "../config/config";
    import { invalidateAll } from "$app/navigation";
    import { onDestroy, onMount } from "svelte";
    import FaviconNotification from "favicon-notification";
    import type { ContentPiece, Information, ScheduledContentPiece } from "@prisma/client";
    import moment from "moment";
    import NewsSmall from "$lib/components/NewsSmall.svelte";
    import YouTubeCommunityPostStreamplan from "$lib/components/YouTubeCommunityPostStreamplan.svelte";

    export let data: PageServerData;

    let reloadInterval: number | NodeJS.Timeout | undefined = undefined;
    let isNotificationVisible = false;

    function findNewestDate() {
        const dates = [
            ...(data.today?.map((entry: ScheduledContentPiece) => moment(entry.startDate)) ?? []),
            ...(data.youtubeCommunityPosts?.map((entry: Information) => moment(entry.date)) ?? []),
            ...(data.instagramPosts?.map((entry: Information) => moment(entry.date)) ?? []),
            ...(data.twitterPosts?.map((entry: Information) => moment(entry.date)) ?? []),
            ...(data.videos?.map((entry: ContentPiece) => moment(entry.startDate)) ?? []),
            moment((data.twitchStatus as TwitchStatus)?.startedAt ?? 0)
        ];

        return Math.max(...dates);
    }

    async function reload() {
        if ($LOW_DATA_MODE) return;

        const currentLastDate = findNewestDate();
        const currentLastUploadPlanEntriesWithLink = data.today.filter((entry: ScheduledContentPiece) => entry.href).length;

        await invalidateAll();

        const newLastDate = findNewestDate();
        const newUploadPlanEntriesWithLink = data.today.filter((entry: ScheduledContentPiece) => entry.href).length;

        if (
            (currentLastDate !== newLastDate && currentLastDate && newLastDate) ||
            currentLastUploadPlanEntriesWithLink !== newUploadPlanEntriesWithLink
        ) {
            isNotificationVisible = true;
            try {
                FaviconNotification.add();
            } catch (e) {
                console.error(e);
            }
        }
    }

    function onUserActive() {
        if (!isNotificationVisible) return;

        isNotificationVisible = false;
        try {
            FaviconNotification.remove();
        } catch (e) {
            console.error(e);
        }
    }

    function handleVisibilityChange() {
        if (document.visibilityState === "visible") {
            onUserActive();
        }
    }

    function handleUserInteraction() {
        onUserActive();
    }

    onMount(() => {
        if (browser) {
            reloadInterval = setInterval(reload, 1000 * 60 * 5);

            FaviconNotification.init({
                color: "#ff0000",
                lineColor: "#000000",
                url: "/favicon.png"
            });

            document.addEventListener("visibilitychange", handleVisibilityChange);
            window.addEventListener("mousemove", handleUserInteraction);
            window.addEventListener("focus", handleUserInteraction);
        }
    });

    onDestroy(() => {
        if (browser) {
            if (reloadInterval) clearInterval(reloadInterval);

            document.removeEventListener("visibilitychange", handleVisibilityChange);
            window.removeEventListener("mousemove", handleUserInteraction);
            window.removeEventListener("focus", handleUserInteraction);
        }
    });
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

<MediaQuery query="(min-width: 768px)" let:matches>
    <div class="grid w-full grid-cols-1 gap-4 p-4 md:gap-8 md:p-8">
        {#if !matches && data.twitchStatus}
            <div class="flex w-full justify-center">
                <div class="md:w-80">
                    <div class="mb-2 ml-2 flex items-center text-2xl">
                        <img alt="twitch" src="/twitch-logo.svg" class="mr-2 inline-block h-8 w-8" />
                        Twitch
                    </div>
                    <TwitchStatus twitch={data.twitchStatus} />
                </div>
            </div>
        {/if}
        {#if matches}
            <div class="grid grid-cols-1 gap-x-8 gap-y-4 md:grid-cols-2 md:gap-y-8 xl:grid-cols-5">
                <div class="order-2">
                    <div class="mb-2 ml-2 flex items-center text-2xl">
                        <LogoYoutube size={32} class="mr-2" />
                        YouTube
                    </div>
                    <div class="flex flex-col gap-2">
                        {#each data.youtubeCommunityPosts as youtube, index}
                            <YouTubeCommunityPost post={youtube} loading={index < 2 ? "eager" : "lazy"} />
                        {/each}
                    </div>
                </div>
                <div class="order-3">
                    <div class="mb-2 ml-2 flex items-center text-2xl">
                        <LogoInstagram size={32} class="mr-2" />
                        Instagram
                    </div>
                    <div class="flex flex-col gap-2">
                        {#each data.instagramPosts as instagram, index}
                            <InstagramPost post={instagram} loading={index < 2 ? "eager" : "lazy"} />
                        {/each}
                    </div>
                </div>
                <div class="order-4">
                    <div class="mb-2 ml-2 flex items-center text-2xl">
                        <LogoTwitter size={32} class="mr-2" />
                        Twitter
                    </div>
                    <div class="flex flex-col gap-2">
                        {#each data.twitterPosts as twitter, index}
                            <TwitterPost post={twitter} loading={index < 2 ? "eager" : "lazy"} />
                        {/each}
                    </div>
                </div>
                <div class="order-5">
                    <div class="mb-2 ml-2 flex items-center text-2xl">
                        <img alt="reddit" src="/reddit-logo.svg" class="mr-2 inline-block h-8 w-8" />
                        Reddit
                    </div>
                    <div class="flex flex-col gap-2">
                        {#each data.redditPosts.slice(0, matches ? 10 : 5) as reddit, index}
                            <RedditPost entry={reddit} loading={index < 4 ? "eager" : "lazy"} />
                        {/each}
                    </div>
                </div>
                <div class="order-1 md:order-6">
                    <div class="mb-2 ml-2 flex items-center text-2xl">
                        <img alt="twitch" src="/twitch-logo.svg" class="mr-2 inline-block h-8 w-8" />
                        Twitch
                    </div>
                    {#if data.twitchStatus}
                        <div class="mb-4">
                            <TwitchStatus twitch={data.twitchStatus} />
                        </div>
                    {/if}
                    <div class="flex flex-col gap-2">
                        {#if data.youtubeStreamplanPost}
                            <YouTubeCommunityPostStreamplan post={data.youtubeStreamplanPost} loading="eager" />
                        {/if}
                        {#each data.upcomingStreams as stream}
                            <TwitchEntry entry={stream} />
                        {:else}
                            {#if !data.youtubeStreamplanPost}
                                <div class="flex items-center">Momentan sind keine geplanten Streams bekannt.</div>
                            {/if}
                        {/each}
                    </div>
                </div>
            </div>
        {:else}
            <NewsSmall
                youtubeCommunityPosts={data.youtubeCommunityPosts}
                instagramPosts={data.instagramPosts}
                twitterPosts={data.twitterPosts}
                redditPosts={data.redditPosts}
                streams={data.upcomingStreams}
                youtubeStreamplanPost={data.youtubeStreamplanPost} />
        {/if}
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
    {#if !matches}
        <div class="md-px:8 flex w-full items-center justify-between px-4 pb-2">
            <a href={MAIL_TO_URL} target="_blank">
                <span>Kontakt</span>
            </a>
            <a href={GITHUB_URL} target="_blank">
                <span>GitHub</span>
            </a>
            <span>v{version}</span>
        </div>
        <div class="w-full pb-4 text-center">
            <span> Dies ist ein privates Projekt und steht in keiner Verbindung zur PietSmiet UG & Co. KG. </span>
        </div>
    {/if}
</MediaQuery>
