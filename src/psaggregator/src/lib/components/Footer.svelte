<script lang="ts">
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { LEGAL_URL, MAIL_TO_URL } from "../../config/config";
    import { version } from "$app/environment";
    import { TabAnchor, TabGroup } from "@skeletonlabs/skeleton";
    import { page } from "$app/stores";
    import { Api, FavoriteFilled, Home, Information, Thumbnail_2 } from "carbon-icons-svelte";
</script>

<style lang="postcss">
    :global(.tab-list) {
        justify-content: unset !important;
    }
</style>

<MediaQuery query="(min-width: 768px)" let:matches>
    {#if matches}
        <div class="flex w-full flex-row flex-wrap items-center gap-x-4 p-2 lg:flex-nowrap">
            <span class="mr-12 text-sm md:text-base">
                <a href="https://github.com/zaanposni/psaggregator/" target="_blank">
                    <span>PS Aggregator</span>
                </a>by
                <a href="https://github.com/zaanposni" target="_blank">
                    <span>zaanposni</span>
                </a>
            </span>
            <a href={MAIL_TO_URL} target="_blank">
                <span>Kontakt</span>
            </a>
            <a href="https://github.com/zaanposni/psaggregator/" target="_blank">
                <span>GitHub</span>
            </a>
            {#if LEGAL_URL}
                <a href={LEGAL_URL} class="text-sm md:text-base" target="_blank">
                    <span>Legal</span>
                </a>
            {/if}
            <span class="ml-auto">v{version}</span>
            <span class="text-xs md:text-base">
                Dies ist ein privates Projekt und steht in keiner Verbindung zur PietSmiet UG & Co. KG.
            </span>
        </div>
    {:else}
        <TabGroup
            justify="justify-center"
            active="variant-filled-primary"
            hover="hover:variant-soft-primary"
            flex="flex-1 lg:flex-none"
            rounded=""
            border=""
            class="bg-surface-100-800-token w-full">
            <TabAnchor href="/" selected={$page.url.pathname === "/"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <Home />
                </div>
                <span>Home</span>
            </TabAnchor>
            <TabAnchor href="/thumbnails" selected={$page.url.pathname === "/thumbnails"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <Thumbnail_2 />
                </div>
                <span>Thumbnails</span>
            </TabAnchor>
            <TabAnchor href="/information" selected={$page.url.pathname === "/information"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <Information />
                </div>
                <span>Information</span>
            </TabAnchor>
            <TabAnchor href="/api" selected={$page.url.pathname === "/api"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <Api />
                </div>
                <span>API</span>
            </TabAnchor>
            <TabAnchor href="/motivation" selected={$page.url.pathname === "/motivation"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <FavoriteFilled />
                </div>
                <span>Motivation</span>
            </TabAnchor>
            <!-- ... -->
        </TabGroup>
    {/if}
</MediaQuery>
