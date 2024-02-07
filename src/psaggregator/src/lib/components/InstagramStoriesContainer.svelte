<script lang="ts">
    import { browser } from "$app/environment";
    import type { InstaStoryWatchHistory } from "$lib/models/InstaStoryWatchHistory";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import type { Information, InformationResource } from "@prisma/client";
    import { CloseLarge, VolumeMute, VolumeUp } from "carbon-icons-svelte";
    import { onMount } from "svelte";

    export let stories: Array<Information & { InformationResource: InformationResource[] }>;
    export let filterKey: "peter" | "brammen" | "jay" | "sep" | "chris";

    let video: HTMLVideoElement;

    stories = stories.filter((story) => story.text.toLowerCase().includes(filterKey));

    let progressContainer: HTMLElement;
    let storyView: HTMLElement;

    let active = false;
    let currentIndex = -1;
    let selectedStory: (Information & { InformationResource: InformationResource[] }) | null = null;
    let touchStartX: number;

    let watchHistory: InstaStoryWatchHistory[] = [];
    $: existingNewStories = stories.some((story) => !watchHistory.find((watchedStory) => watchedStory.id === story.id));

    const playSpecific = (index: number) => {
        currentIndex = index;
        selectedStory = stories[currentIndex];
        addToWatchHistory(selectedStory);
    };

    const playNext = (e?: AnimationEvent) => {
        if (currentIndex == stories.length - 1) {
            active = false;
            currentIndex = 0;
            return;
        }

        currentIndex++;
        selectedStory = stories[currentIndex];
        addToWatchHistory(selectedStory);
    };

    const playPrevious = () => {
        if (currentIndex == 0) {
            return;
        }

        currentIndex--;
        selectedStory = stories[currentIndex];
    };

    const clickImageHandler = (e: MouseEvent) => {
        // check if click is on the right or left side of the image and go to the next or previous story
        if (e.offsetX < storyView.clientWidth / 2) {
            playPrevious();
        } else {
            playNext();
        }
    };

    const touchStartHandler = (e: TouchEvent) => {
        // Store the initial touch position
        touchStartX = e.touches[0].clientX;
    };

    const touchEndHandler = (e: TouchEvent) => {
        // Compare the initial and final touch positions to determine the direction
        const touchEndX = e.changedTouches[0].clientX;
        const deltaX = touchEndX - touchStartX;

        if (Math.abs(deltaX) < 100) {
            return;
        }

        // Adjust currentIndex based on swipe direction
        if (deltaX > 0) {
            playPrevious();
        } else {
            playNext();
        }

        touchStartX = 0;
    };

    function addToWatchHistory(story: Information) {
        if (!watchHistory.find((watchedStory) => watchedStory.id === story.id)) {
            const date = story.date?.valueOf() ?? Date.now();
            watchHistory.push({ id: story.id, validUntil: date + 24 * 60 * 60 * 1000 });
            watchHistory = [...watchHistory];
            localStorage.setItem(`instaStoryWatchHistory_${filterKey}`, JSON.stringify(watchHistory));
        }
    }

    function start() {
        if (!stories.length) return;

        // find first index that is not in watchHistory
        let index = stories.findIndex((story) => !watchHistory.find((watchedStory) => watchedStory.id === story.id));
        if (index === -1) {
            index = 0;
        }

        playSpecific(index);
        active = true;
    }

    function titleCase(str: string | null) {
        if (!str) return "";
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    onMount(() => {
        if (browser) {
            watchHistory = JSON.parse(localStorage.getItem(`instaStoryWatchHistory_${filterKey}`) || "[]");
            watchHistory = watchHistory.filter((story) => story.validUntil > Date.now());
        }
    });
</script>

<style>
    .progress {
        height: 2px;
        flex-grow: 1;
        border-radius: 4px;
        margin: 0 5px;
        display: flex;
        background-image: -webkit-linear-gradient(
            left,
            rgba(255, 255, 255, 0.5) 0%,
            rgba(255, 255, 255, 0.5) 50%,
            rgba(88, 89, 104, 0.5) 50.001%,
            rgba(88, 89, 104, 0.5) 100%
        );
        background-repeat: no-repeat;
        background-size: 200%;
        background-color: #666;
        background-position: 100% 50%;
        animation-timing-function: linear;
    }

    :global(.progress.active) {
        animation-name: Loader;
    }

    :global(.progress.passed) {
        background-color: #fff !important;
    }

    @keyframes Loader {
        0% {
            background-position: 100% 0;
        }
        100% {
            background-position: 0 0;
        }
    }

    @-webkit-keyframes Loader {
        0% {
            background-position: 100% 0;
        }
        100% {
            background-position: 0 0;
        }
    }

    :global(.story-container:hover .progress) {
        animation-play-state: paused;
    }

    :global(.story-container.pause .progress) {
        animation-play-state: paused;
    }

    .instagramgradient {
        border-radius: 50%;
        background: linear-gradient(to right, red, orange);
        padding: 3px;
    }
</style>

<MediaQuery query="(min-width: 768px)" let:matches>
    {#if active}
        <div class="absolute left-0 top-0 z-10 flex h-full w-full flex-col bg-black">
            <div
                class="story-container flex h-full w-full flex-col overflow-hidden lg:mx-auto lg:w-1/2"
                class:pause={touchStartX}
                on:touchstart={touchStartHandler}
                on:touchend={touchEndHandler}>
                <div class="progress-container flex w-full px-2 pt-4" bind:this={progressContainer}>
                    {#each stories as story, index}
                        {@const duration =
                            story.InformationResource?.length && story.InformationResource[0].videoDuration
                                ? story.InformationResource[0].videoDuration
                                : 15}
                        <div
                            style="animation-duration: {duration}s"
                            class:active={currentIndex === index}
                            class:passed={currentIndex > index}
                            class="progress"
                            on:animationend={playNext}
                            on:click={() => {
                                playSpecific(index);
                            }}
                            on:keydown={void 0}
                            role="button"
                            tabindex="0">
                        </div>
                    {/each}
                </div>
                <div class="mt-2 flex w-full items-center justify-between px-2">
                    <div class="flex items-center gap-x-2">
                        <img src="{filterKey}.jpg" alt={filterKey} class="h-12 w-12 rounded-full object-cover" />
                        <span class="text-sm font-bold text-white">{titleCase(filterKey)}</span>
                    </div>
                    <div class="flex items-center gap-x-2">
                        {#if selectedStory && selectedStory.InformationResource?.length && selectedStory.InformationResource[0].videoUri}
                            <button
                                on:click={(e) => {
                                    video.muted = !video.muted;
                                    e.stopPropagation();
                                }}>
                                {#if video}
                                    {#if video.muted}
                                        <VolumeMute class="h-8 w-8" />
                                    {:else}
                                        <VolumeUp class="h-8 w-8" />
                                    {/if}
                                {/if}
                            </button>
                        {/if}
                        <button on:click={() => (active = false)}>
                            <CloseLarge class="h-8 w-8" />
                        </button>
                    </div>
                </div>
                <div
                    bind:this={storyView}
                    class="flex h-full w-full items-center justify-center overflow-y-auto py-2 md:py-8"
                    on:click={clickImageHandler}
                    on:keydown={void 0}
                    role="button"
                    tabindex="0">
                    {#if selectedStory}
                        {#if selectedStory.InformationResource?.length && selectedStory.InformationResource[0].videoUri}
                            <video
                                bind:this={video}
                                src={selectedStory.InformationResource[0].videoUri}
                                autoplay
                                loop
                                muted
                                playsinline
                                class="h-full w-full object-contain"></video>
                        {:else}
                            <img src={selectedStory.imageUri} alt={selectedStory.text} class="h-full w-full object-contain" />
                        {/if}
                    {/if}
                </div>
            </div>
        </div>
    {:else}
        <div
            class="aspect-square h-full w-auto"
            class:cursor-pointer={stories.filter((story) => story.text.toLowerCase().includes(filterKey)).length}
            class:!cursor-default={!stories.filter((story) => story.text.toLowerCase().includes(filterKey)).length}
            class:grayscale={!stories.filter((story) => story.text.toLowerCase().includes(filterKey)).length}
            class:instagramgradient={existingNewStories}
            title={filterKey}
            on:click={start}
            on:keydown={void 0}
            role="button"
            tabindex="0">
            <img class="h-full w-full rounded-full object-cover" src="{filterKey}.jpg" alt={filterKey} />
        </div>
    {/if}
</MediaQuery>
