<script lang="ts">
    import InstagramPost from "$lib/components/InstagramPost.svelte";
    import YouTubeCommunityPost from "$lib/components/YouTubeCommunityPost.svelte";
    import { afterUpdate, onDestroy } from "svelte";
    import { GITHUB_URL } from "../../config/config";
    import type { PageData } from "./$types";
    import { LogoYoutube, LogoTwitter, LogoInstagram, FaceDissatisfied } from "carbon-icons-svelte";
    import { browser } from "$app/environment";
    import { ImportType } from "@prisma/client";
    import { ProgressRadial } from "@skeletonlabs/skeleton";

    export let data: PageData;

    const batchSize = 20;

    let skip = 0;
    let loading = {
        [ImportType.YouTube]: false,
        [ImportType.Instagram]: false
    };
    let endReached = {
        [ImportType.YouTube]: data.youtubeCommunityPosts.length < batchSize,
        [ImportType.Instagram]: data.instagramPosts.length < batchSize
    };

    async function loadMore() {
        for (const type of [ImportType.YouTube, ImportType.Instagram]) {
            console.log(type, loading[type], endReached[type]);
            if (loading[type] || endReached[type]) {
                continue;
            }

            loading[type] = true;
            skip += batchSize;

            const response = await fetch(`/api/information?skip=${skip}&type=${type}`);
            const newInformation = await response.json();

            if (type === ImportType.YouTube) {
                data.youtubeCommunityPosts = [...data.youtubeCommunityPosts, ...newInformation];
            } else if (type === ImportType.Instagram) {
                data.instagramPosts = [...data.instagramPosts, ...newInformation];
            }

            loading[type] = false;
            endReached[type] = newInformation.length < batchSize;
        }
    }

    const onScroll = () => {
        const mediaQuery = window.matchMedia("(min-width: 1280px)");
        if (!mediaQuery.matches) {
            return;
        }

        const scrollElement = document.getElementById("page");
        if (!scrollElement) {
            return;
        }
        if (scrollElement.offsetHeight + scrollElement.scrollTop + 400 >= scrollElement.scrollHeight) {
            loadMore();
        }
    };

    afterUpdate(() => {
        if (browser) {
            const scrollElement = document.getElementById("page");
            if (!scrollElement) {
                return;
            }
            scrollElement.addEventListener("scroll", onScroll);
        }
    });

    onDestroy(() => {
        if (browser) {
            const scrollElement = document.getElementById("page");
            if (!scrollElement) {
                return;
            }
            scrollElement.removeEventListener("scroll", onScroll);
        }
    });
</script>

<div class="grid grid-cols-1 gap-4 p-4 md:grid-cols-2 md:gap-8 md:p-8 xl:grid-cols-4">
    <div>
        <div class="mb-2 ml-2 flex items-center text-2xl">
            <LogoYoutube size={32} class="mr-2" />
            YouTube
        </div>
        <div class="flex flex-col gap-y-4">
            {#each data.youtubeCommunityPosts as youtube}
                <YouTubeCommunityPost post={youtube} />
            {/each}
        </div>
        {#if loading[ImportType.YouTube]}
            <div class="col-span-full mt-4 flex w-full items-center justify-center text-center md:mt-8">
                <ProgressRadial />
            </div>
        {/if}
    </div>
    <div>
        <div class="mb-2 ml-2 flex items-center text-2xl">
            <LogoInstagram size={32} class="mr-2" />
            Instagram
        </div>
        <div class="flex flex-col gap-y-4">
            {#each data.instagramPosts as instagram}
                <InstagramPost post={instagram} />
            {/each}
        </div>
        {#if loading[ImportType.Instagram]}
            <div class="col-span-full mt-4 flex w-full items-center justify-center text-center md:mt-8">
                <ProgressRadial />
            </div>
        {/if}
    </div>
    <div>
        <div class="mb-2 ml-2 flex items-center text-2xl">
            <img alt="threads" src="/threads-logo.svg" class="mr-2 inline-block h-8 w-8" />
            Threads
        </div>
        <div class="mx-auto flex flex-col items-center text-center">
            <div>
                <FaceDissatisfied size={32} />
            </div>
            <span>Leider gibt es noch keinen Threads-Import.</span>
            <span>Dieses Projekt ist Open Source.</span>
            <span
                >Beteilige dich gerne auf
                <a href={GITHUB_URL} class="underline" target="_blank">GitHub</a>
            </span>
        </div>
    </div>
    <div>
        <div class="mb-2 ml-2 flex items-center text-2xl">
            <LogoTwitter size={32} class="mr-2" />
            Twitter
        </div>
        <div class="mx-auto flex flex-col items-center text-center">
            <div>
                <FaceDissatisfied size={32} />
            </div>
            <span>Leider gibt es noch keinen Twitter-Import.</span>
            <span>Dieses Projekt ist Open Source.</span>
            <span
                >Beteilige dich gerne auf
                <a href={GITHUB_URL} class="underline" target="_blank">GitHub</a>
            </span>
        </div>
    </div>
</div>
