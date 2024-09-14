<script lang="ts">
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { GITHUB_AUTHOR_URL, GITHUB_URL, LEGAL_URL, MAIL_TO_URL } from "../../config/config";
    import { version } from "$app/environment";
    import { Api, Favorite, Home, Document, Thumbnail_2, Settings, EventSchedule, Binoculars } from "carbon-icons-svelte";
    import { page } from "$app/stores";
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
        <div class="h-18 flex w-full flex-row items-center gap-x-2 overflow-x-auto overflow-y-hidden border-t">
            <div class="shrink-0 p-2 pt-4" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/"}>
                <a href="/">
                    <div class="flex justify-center">
                        <Home />
                    </div>
                    <span>Home</span>
                </a>
            </div>
            <div class="shrink-0 p-2 pt-4" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/plan"}>
                <a href="/plan">
                    <div class="flex justify-center">
                        <EventSchedule />
                    </div>
                    <span>Uploadplan</span>
                </a>
            </div>
            <div class="shrink-0 p-2 pt-4" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/videos"}>
                <a href="/videos">
                    <div class="flex justify-center">
                        <Thumbnail_2 />
                    </div>
                    <span>Videos</span>
                </a>
            </div>
            <div class="shrink-0 p-2 pt-4" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/news"}>
                <a href="/news">
                    <div class="flex justify-center">
                        <Document />
                    </div>
                    <span>News</span>
                </a>
            </div>
            <div class="shrink-0 p-2 pt-4" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/randomvideo"}>
                <a href="/randomvideo">
                    <div class="flex justify-center">
                        <Binoculars />
                    </div>
                    <span>Zufall</span>
                </a>
            </div>
            <div class="shrink-0 p-2 pt-4" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/api"}>
                <a href="/api">
                    <div class="flex justify-center">
                        <Api />
                    </div>
                    <span>API</span>
                </a>
            </div>
            <div class="shrink-0 p-2 pt-4" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/motivation"}>
                <a href="/motivation">
                    <div class="flex justify-center">
                        <Favorite />
                    </div>
                    <span>Motivation</span>
                </a>
            </div>
            <div class="shrink-0 p-2 pt-4" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/settings"}>
                <a href="/settings">
                    <div class="flex justify-center">
                        <Settings />
                    </div>
                    <span>Einstellungen</span>
                </a>
            </div>
        </div>
    {/if}
</MediaQuery>
