<script lang="ts">
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { LEGAL_URL, MAIL_TO_URL } from "../../config/config";
    import { version } from "$app/environment";
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    <div class="flex w-full flex-row flex-wrap items-center gap-x-4 p-2 lg:flex-nowrap">
        <span class="mr-12 text-sm md:text-base">
            <a href="https://github.com/zaanposni/psaggregator/" target="_blank">
                <span>PS Aggregator</span>
            </a>by
            <a href="https://github.com/zaanposni" target="_blank">
                <span>zaanposni</span>
            </a>
        </span>
        {#if matches}
            <a href={MAIL_TO_URL} target="_blank">
                <span>Kontakt</span>
            </a>
            <a href="https://github.com/zaanposni/psaggregator/" target="_blank">
                <span>GitHub</span>
            </a>
        {/if}
        {#if LEGAL_URL}
            <a href={LEGAL_URL} class="text-sm md:text-base" target="_blank">
                <span>Legal</span>
            </a>
        {/if}
        <span class="ml-auto">v{version}</span>
        <span class="text-xs md:text-base"> Dies ist ein privates Projekt und steht in keiner Verbindung zur PietSmiet UG & Co. KG. </span>
    </div>
</MediaQuery>
