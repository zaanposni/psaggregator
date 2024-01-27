<script lang="ts">
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { GITHUB_AUTHOR_URL, GITHUB_URL, LEGAL_URL, MAIL_TO_URL } from "../../config/config";
    import { version } from "$app/environment";
    import { TabAnchor, TabGroup } from "@skeletonlabs/skeleton";
    import { page } from "$app/stores";
    import { Api, FavoriteFilled, Home, Document, Thumbnail_2, Settings, EventSchedule } from "carbon-icons-svelte";
</script>

<style lang="postcss">
    :global(.tab-list) {
        justify-content: unset !important;
    }
</style>

<MediaQuery query="(min-width: 1280px)" let:matches>
    {#if matches}
        <div class="flex w-full flex-row flex-nowrap items-center gap-x-4 p-2">
            <span class="mr-12">
                <a href={GITHUB_URL} target="_blank">
                    <span>PS Aggregator</span>
                </a>by
                <a href={GITHUB_AUTHOR_URL} target="_blank">
                    <span>zaanposni</span>
                </a>
            </span>
            <a href={MAIL_TO_URL} target="_blank">
                <span>Kontakt</span>
            </a>
            <a href={GITHUB_URL} target="_blank">
                <span>GitHub</span>
            </a>
            {#if LEGAL_URL}
                <a href={LEGAL_URL} target="_blank">
                    <span>Legal</span>
                </a>
            {/if}
            <span class="ml-auto">v{version}</span>
            <span> Dies ist ein privates Projekt und steht in keiner Verbindung zur PietSmiet UG & Co. KG. </span>
        </div>
    {:else}
        <TabGroup
            justify="justify-center"
            active="variant-filled-primary"
            hover="hover:variant-soft-primary"
            flex="flex-1"
            rounded=""
            border=""
            class="bg-surface-100-800-token w-full">
            <TabAnchor href="/" selected={$page.url.pathname === "/"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <Home />
                </div>
                <span>Home</span>
            </TabAnchor>
            <TabAnchor href="/plan" selected={$page.url.pathname === "/plan"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <EventSchedule />
                </div>
                <span>Uploadplan</span>
            </TabAnchor>
            <TabAnchor href="/videos" selected={$page.url.pathname === "/videos"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <Thumbnail_2 />
                </div>
                <span>Videos</span>
            </TabAnchor>
            <TabAnchor href="/news" selected={$page.url.pathname === "/news"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <Document />
                </div>
                <span>News</span>
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
            <TabAnchor href="/settings" selected={$page.url.pathname === "/settings"} class="shrink-0">
                <div class="flex justify-center" slot="lead">
                    <Settings />
                </div>
                <span>Einstellungen</span>
            </TabAnchor>
            <!-- ... -->
        </TabGroup>
    {/if}
</MediaQuery>
