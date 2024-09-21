<script lang="ts">
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { GITHUB_URL, KOFI_USERNAME, LEGAL_URL } from "../../config/config";
    import LightSwitch from "./LightSwitch.svelte";

    function openChangelog() {}
</script>

<MediaQuery query="(min-width: 1280px)" let:matches>
    <div class="flex items-center gap-x-4 border-b p-4">
        <div>
            <a href="/">
                <img src="/ps.png" alt="PS Aggregator Logo" class="h-8 w-8" />
            </a>
        </div>
        <div class="flex grow flex-nowrap items-center justify-between">
            <div class="flex items-center gap-x-4">
                {#if matches}
                    <a href="/">Home</a>
                    <a href="/plan">Uploadplan</a>
                    <a href="/videos">Videos</a>
                    <a href="/news">News</a>
                    <a href="/randomvideo">Zufall</a>
                    <a href="/api">API</a>
                    <a href="/motivation">Motivation</a>
                    <a href="/settings">Einstellungen</a>
                    <a href="/changelog">Was ist neu?</a>
                {/if}
            </div>
            <div class="flex items-center gap-x-4">
                {#if matches}
                    <a href={GITHUB_URL} target="_blank">
                        <span>GitHub</span>
                    </a>
                {/if}
                {#if KOFI_USERNAME}
                    <a href="https://ko-fi.com/{KOFI_USERNAME}" target="_blank">
                        <span>Ko-fi</span>
                    </a>
                {/if}
                <a href="https://pietsmiet.de" target="_blank">
                    <span>pietsmiet.de</span>
                </a>
                {#if !matches && LEGAL_URL}
                    <a href={LEGAL_URL} target="_blank">
                        <span>Legal</span>
                    </a>
                {/if}
            </div>
        </div>
        <LightSwitch />
    </div>
</MediaQuery>
