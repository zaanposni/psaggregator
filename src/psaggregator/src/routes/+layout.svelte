<script>
    import "../app.css";
    import { Drawer, Modal, Toast, AppShell } from "@skeletonlabs/skeleton";
    import { initializeStores } from "@skeletonlabs/skeleton";
    import Footer from "$lib/components/Footer.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { MICROANALYTICS_ID, SHOW_ABSOLUTE_DATES } from "../config/config";
    import BigHeader from "$lib/components/BigHeader.svelte";
    import { afterNavigate, disableScrollHandling } from "$app/navigation";
    import { browser } from "$app/environment";
    import { onMount } from "svelte";

    initializeStores();

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
            SHOW_ABSOLUTE_DATES.set(localStorage.getItem("showAbsoluteDates") === "true");
        }
    });
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    <div style="display: contents" class="h-full overflow-hidden">
        <AppShell>
            <svelte:fragment slot="header">
                <BigHeader />
            </svelte:fragment>
            <slot />
            <svelte:fragment slot="footer">
                <Footer />
            </svelte:fragment>
        </AppShell>
    </div>
</MediaQuery>

<Toast />
<Modal />
<Drawer />

{#if MICROANALYTICS_ID}
    <script
        data-host="https://app.microanalytics.io"
        data-dnt="false"
        src="https://app.microanalytics.io/js/script.js"
        id={MICROANALYTICS_ID}
        async
        defer></script>
{/if}
