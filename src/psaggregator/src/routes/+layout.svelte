<script lang="ts">
    import "../app.css";
    import Footer from "$lib/components/Footer.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import {
        LINK_YOUTUBE,
        LINK_YOUTUBE_KEY,
        UMAMI_ID,
        SHOW_ABSOLUTE_DATES,
        SHOW_ABSOLUTE_DATES_KEY,
        VIDEO_COMPLEXE_VIEW,
        VIDEO_COMPLEXE_VIEW_KEY
    } from "../config/config";
    import BigHeader from "$lib/components/BigHeader.svelte";
    import { afterNavigate, disableScrollHandling } from "$app/navigation";
    import { browser } from "$app/environment";
    import { onMount } from "svelte";
    import type { LayoutData } from "./$types";
    import { CloseLarge } from "carbon-icons-svelte";
    import { ModeWatcher } from "mode-watcher";
    import { Toaster } from "$lib/components/ui/sonner";
    import * as Alert from "$lib/components/ui/alert";
    import { slide } from "svelte/transition";

    export let data: LayoutData;

    let scrollableContent: HTMLElement;
    let atTop = false;

    afterNavigate(() => {
        if (browser) {
            disableScrollHandling();
            const scrollElement = document.getElementById("page");
            if (!scrollElement) {
                return;
            }
            setTimeout(() => {
                scrollElement.scrollTo({ top: 0, behavior: "instant" });
            }, 1);
        }
    });

    function scrollToTop(event: TouchEvent) {
        const touchY = event.touches[0].clientY;
        if (touchY < 10 && !atTop) {
            scrollableContent.scrollTo({ top: 0, behavior: "smooth" });
        }
    }

    onMount(() => {
        if (browser) {
            SHOW_ABSOLUTE_DATES.set(localStorage.getItem(SHOW_ABSOLUTE_DATES_KEY) === "true");
            VIDEO_COMPLEXE_VIEW.set(localStorage.getItem(VIDEO_COMPLEXE_VIEW_KEY) === "true");
            LINK_YOUTUBE.set(localStorage.getItem(LINK_YOUTUBE_KEY) === "true");

            scrollableContent &&
                scrollableContent.addEventListener("scroll", () => {
                    atTop = scrollableContent.scrollTop === 0;
                });

            window && window.addEventListener("touchstart", scrollToTop, { passive: true });
        }
    });
</script>

<ModeWatcher />
<Toaster />

<MediaQuery query="(min-width: 768px)" let:matches>
    <div style="display: contents" class="h-full overflow-hidden">
        <div class="flex h-full w-full flex-col overflow-hidden">
            <BigHeader />
            {#each data.announcements as announcement (announcement.id)}
                <div out:slide>
                    <Alert.Root class="bg-primary flex items-center justify-between gap-x-2 rounded-none border-none">
                        <div class="text-primary-foreground font-bold">
                            {@html announcement.text}
                        </div>
                        <button
                            class="alert-actions !mt-0"
                            on:click={() => {
                                data.announcements = data.announcements.filter((a) => a.id !== announcement.id);
                            }}>
                            <CloseLarge class="text-primary-foreground" />
                        </button>
                    </Alert.Root>
                </div>
            {/each}
            <div class="flex h-full w-full flex-auto overflow-hidden">
                <div class="flex flex-1 flex-col overflow-x-hidden" style="scrollbar-gutter: auto;" id="page" bind:this={scrollableContent}>
                    <slot />
                </div>
            </div>
            <Footer />
        </div>
    </div>
</MediaQuery>

{#if UMAMI_ID}
    <script defer src="https://cloud.umami.is/script.js" data-website-id={UMAMI_ID}></script>
{/if}
