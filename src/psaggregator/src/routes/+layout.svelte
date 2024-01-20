<script>
    import "../app.css";
    import { Drawer, Modal, Toast, AppShell, AppBar, LightSwitch } from "@skeletonlabs/skeleton";
    import { initializeStores } from "@skeletonlabs/skeleton";
    import Footer from "$lib/components/Footer.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { MICROANALYTICS_ID } from "../config/config";

    initializeStores();
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    <div style="display: contents" class="h-full overflow-hidden">
        <AppShell>
            <svelte:fragment slot="header">
                <AppBar>
                    <div slot="lead" class="flex flex-row items-center gap-x-4">
                        <a href="/">
                            <img src="/ps.png" alt="PS Aggregator Logo" class="h-8 w-8" />
                        </a>
                        <a href="/">Home</a>
                        {#if matches}
                            <a href="/thumbnails">Thumbnails</a>
                            <a href="/api">API</a>
                            <a href="/motivation">Motivation</a>
                            <a href="https://github.com/zaanposni/psaggregator/" target="_blank">
                                <span>GitHub</span>
                            </a>
                            <a href="https://pietsmiet.de" target="_blank">
                                <span>PietSmiet.de</span>
                            </a>
                        {/if}
                    </div>
                    <svelte:fragment slot="trail">
                        <LightSwitch />
                    </svelte:fragment>
                </AppBar>
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
