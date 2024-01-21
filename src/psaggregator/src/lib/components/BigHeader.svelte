<script lang="ts">
    import { AppBar, LightSwitch } from "@skeletonlabs/skeleton";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { KOFI_USERNAME, LEGAL_URL } from "../../config/config";
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    <AppBar>
        <div slot="lead" class="flex flex-row items-center gap-x-4">
            <a href="/">
                <img src="/ps.png" alt="PS Aggregator Logo" class="h-8 w-8" />
            </a>
            {#if matches}
                <a href="/">Home</a>
                <a href="/thumbnails">Thumbnails</a>
                <a href="/api">API</a>
                <a href="/motivation">Motivation</a>
                <a href="https://github.com/zaanposni/psaggregator/" target="_blank">
                    <span>GitHub</span>
                </a>
            {/if}
            {#if KOFI_USERNAME}
                <a href="https://ko-fi.com/{KOFI_USERNAME}" target="_blank">
                    <span>Ko-fi</span>
                </a>
            {/if}
            <a href="https://pietsmiet.de" target="_blank">
                <span>PietSmiet.de</span>
            </a>
            {#if !matches && LEGAL_URL}
                <a href={LEGAL_URL} target="_blank">
                    <span>Legal</span>
                </a>
            {/if}
        </div>
        <svelte:fragment slot="trail">
            <LightSwitch />
        </svelte:fragment>
    </AppBar>
</MediaQuery>
