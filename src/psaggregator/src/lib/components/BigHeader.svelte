<script lang="ts">
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { GITHUB_URL, KOFI_USERNAME, LEGAL_URL } from "../../config/config";
    import LightSwitch from "./LightSwitch.svelte";
    import TwitchStatus from "./TwitchStatus.svelte";

    export let twitchStatus: TwitchStatus | null = null;
</script>

<MediaQuery query="(min-width: 768px)" let:matches={smallMatches}>
    <MediaQuery query="(min-width: 1280px)" let:matches>
        <div class="flex items-center gap-x-4 border-b p-4">
            <div>
                <a href="/">
                    <img
                        src="/ps.png"
                        alt="psaggregator logo, pietsmiet logo turned upside down, green game controller"
                        class="h-8 w-8"
                        height="100"
                        width="100" />
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
                    {#if smallMatches}
                        {#if twitchStatus}
                            <a class="flex flex-row items-center" href="https://twitch.tv/pietsmiet" target="_blank">
                                <div class="my-auto mr-2 h-2 w-2 rounded-full bg-red-600" />
                                <span>PietSmiet ist live!</span>
                            </a>
                        {:else}
                            <div class="flex flex-row items-center">
                                <div class="my-auto mr-2 h-2 w-2 rounded-full bg-gray-600" />
                                <span>PietSmiet ist offline!</span>
                            </div>
                        {/if}
                    {/if}
                    {#if matches}
                        <a href={GITHUB_URL} target="_blank">
                            <span>GitHub</span>
                        </a>
                    {/if}
                    {#if KOFI_USERNAME}
                        <a href="https://ko-fi.com/{KOFI_USERNAME}" target="_blank">
                            <span>Donate</span>
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
</MediaQuery>
