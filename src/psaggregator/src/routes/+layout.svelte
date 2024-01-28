<script lang="ts">
    import "../app.css";
    import { Modal, Toast, AppShell, type ModalComponent } from "@skeletonlabs/skeleton";
    import { initializeStores } from "@skeletonlabs/skeleton";
    import Footer from "$lib/components/Footer.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import {
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
    import Changelog from "$lib/components/Changelog.svelte";
    import type { LayoutData } from "./$types";
    import { CloseLarge, WarningAltFilled } from "carbon-icons-svelte";

    export let data: LayoutData;

    initializeStores();

    const modalRegistry: Record<string, ModalComponent> = {
        changelog: { ref: Changelog }
    };

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
        }
    });
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    <div style="display: contents" class="h-full overflow-hidden">
        <AppShell>
            <svelte:fragment slot="header">
                <BigHeader />
            </svelte:fragment>
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
            <slot />
            <svelte:fragment slot="footer">
                <Footer />
            </svelte:fragment>
        </AppShell>
    </div>
</MediaQuery>

<Toast />
<Modal components={modalRegistry} />

{#if MICROANALYTICS_ID}
    <script
        data-host="https://app.microanalytics.io"
        data-dnt="false"
        src="https://app.microanalytics.io/js/script.js"
        id={MICROANALYTICS_ID}
        async
        defer></script>
{/if}
