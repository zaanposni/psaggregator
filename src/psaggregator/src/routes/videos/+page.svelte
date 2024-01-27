<script lang="ts">
    import { onDestroy, afterUpdate } from "svelte";
    import type { PageData } from "./$types";
    import moment from "moment";
    import { browser } from "$app/environment";
    import { ProgressRadial, SlideToggle } from "@skeletonlabs/skeleton";
    import PsVideo from "$lib/components/PSVideo.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";

    export let data: PageData;

    const batchSize = 50;

    let showAdvancedView = false;
    let previousMonth: string | null = null;
    let skip = 0;
    let loading = false;
    let endReached = data.videos.length < batchSize;

    function checkMonth(videoStartDate: Date): string | null {
        const currentMonth = moment(videoStartDate).format("MMMM YYYY");

        if (currentMonth === previousMonth) {
            return null;
        }

        previousMonth = currentMonth;
        return currentMonth;
    }

    async function loadMore() {
        if (loading || endReached) {
            return;
        }

        loading = true;
        skip += batchSize;

        const response = await fetch(`/api/thumbnails?skip=${skip}`);
        const newVideos = await response.json();

        data.videos = [...data.videos, ...newVideos];
        loading = false;
        endReached = newVideos.length < batchSize;
    }

    const onScroll = () => {
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

<MediaQuery query="(min-width: 768px)" let:matches>
    <div class="p-4 md:p-8">
        <div class="mb-4 flex w-full flex-col justify-between gap-y-4 md:mb-8 md:flex-row md:items-center">
            <h1 class="text-3xl font-bold">Alle Videos</h1>
            <div class="mr-4 flex items-center gap-x-1 md:gap-x-4">
                <span>Komplexe Ansicht</span>
                <SlideToggle name="slide" bind:checked={showAdvancedView} />
            </div>
        </div>
        <section class="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-5 {!matches && showAdvancedView ? '!grid-cols-1' : ''}">
            {#each data.videos as video}
                {#if video.startDate}
                    {@const newMonth = checkMonth(video.startDate)}
                    {#if newMonth}
                        <div class="col-span-full text-lg font-bold">
                            {newMonth}
                        </div>
                    {/if}
                {/if}
                {#if showAdvancedView}
                    <PsVideo {video} class="w-full {matches || showAdvancedView ? '' : '!text-sm'}" />
                {:else}
                    <a href={video.href} target="_blank" class="overflow-hidden">
                        <img
                            class="h-auto max-w-full transform rounded-lg transition-transform duration-500 hover:scale-110"
                            src={video.imageUri}
                            alt={video.title} />
                    </a>
                {/if}
            {/each}
            {#if loading}
                <div class="col-span-full flex w-full items-center justify-center text-center">
                    <ProgressRadial />
                </div>
            {/if}
        </section>
    </div>
</MediaQuery>
