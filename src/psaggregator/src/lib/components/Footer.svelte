<script lang="ts">
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { GITHUB_AUTHOR_URL, GITHUB_URL, LEGAL_URL, MAIL_TO_URL } from "../../config/config";
    import { version } from "$app/environment";
    import {
        Api,
        Favorite,
        Home,
        Document,
        Thumbnail_2,
        Settings,
        EventSchedule,
        Binoculars,
        IbmWatsonxCodeAssistantForZRefactor
    } from "carbon-icons-svelte";
    import { page } from "$app/stores";
</script>

<style lang="postcss">
    :global(.tab-list) {
        justify-content: unset !important;
    }

    #iconfooter > a {
        @apply flex items-center justify-center p-4 pt-4;
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
        <div class="flex h-16 flex-row items-center overflow-x-auto overflow-y-hidden border-t" id="iconfooter">
            <a href="/" class="" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/"}>
                <Home size={24} />
            </a>
            <a href="/plan" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/plan"}>
                <EventSchedule size={24} />
            </a>
            <a href="/videos" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/videos"}>
                <Thumbnail_2 size={24} />
            </a>
            <a href="/news" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/news"}>
                <Document size={24} />
            </a>
            <a href="/randomvideo" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/randomvideo"}>
                <Binoculars size={24} />
            </a>
            <a href="/api" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/api"}>
                <Api size={24} />
            </a>
            <a href="/motivation" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/motivation"}>
                <Favorite size={24} />
            </a>
            <a href="/changelog" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/changelog"}>
                <IbmWatsonxCodeAssistantForZRefactor size={24} />
            </a>
            <a href="/settings" class:bg-[hsl(var(--primary))]={$page.url.pathname === "/settings"}>
                <Settings size={24} />
            </a>
        </div>
    {/if}
</MediaQuery>
