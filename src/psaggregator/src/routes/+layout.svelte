<script lang="ts">
    import "../app.css";
    import Footer from "$lib/components/Footer.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import {
        LINK_YOUTUBE,
        LINK_YOUTUBE_KEY,
        MICROANALYTICS_ID,
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
    import { CloseLarge, WarningAltFilled } from "carbon-icons-svelte";
    import { ModeWatcher } from "mode-watcher";
    import { Toaster } from "$lib/components/ui/sonner";

    export let data: LayoutData;

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

    onMount(() => {
        if (browser) {
            SHOW_ABSOLUTE_DATES.set(localStorage.getItem(SHOW_ABSOLUTE_DATES_KEY) === "true");
            VIDEO_COMPLEXE_VIEW.set(localStorage.getItem(VIDEO_COMPLEXE_VIEW_KEY) === "true");
            LINK_YOUTUBE.set(localStorage.getItem(LINK_YOUTUBE_KEY) === "true");
        }
    });
</script>

<ModeWatcher />
<Toaster />

<MediaQuery query="(min-width: 768px)" let:matches>
    <div style="display: contents" class="h-full overflow-hidden">
        <div class="flex h-full w-full flex-col overflow-hidden">
            <BigHeader />
            {#each data.announcements as announcement}
                <aside class="alert variant-filled-warning flex-row items-center">
                    <div>
                        <WarningAltFilled size={32} />
                    </div>
                    <div class="alert-message !mt-0 px-2">
                        <p>{announcement.text}</p>
                    </div>
                    <button
                        class="alert-actions !mt-0"
                        on:click={() => {
                            data.announcements = data.announcements.filter((a) => a.id !== announcement.id);
                        }}>
                        <CloseLarge />
                    </button>
                </aside>
            {/each}
            <div class="flex h-full w-full flex-auto overflow-hidden">
                <div class="flex flex-1 flex-col overflow-x-hidden" style="scrollbar-gutter: auto;" id="page">
                    <slot />
                </div>
            </div>
            <Footer />
        </div>
    </div>
</MediaQuery>

{#if MICROANALYTICS_ID}
    <script
        data-host="https://app.microanalytics.io"
        data-dnt="false"
        src="https://app.microanalytics.io/js/script.js"
        id={MICROANALYTICS_ID}
        async
        defer></script>
{/if}
