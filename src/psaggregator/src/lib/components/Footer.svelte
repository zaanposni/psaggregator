<script lang="ts">
    import { LEGAL_URL } from "../../config/config";
</script>

<div class="flex w-full flex-row flex-wrap items-center gap-x-4 p-2 lg:flex-nowrap">
    <span class="mr-12">
        <a href="https://github.com/zaanposni/psaggregator/" target="_blank">
            <span>PS Aggregator</span>
        </a>by
        <a href="https://github.com/zaanposni" target="_blank">
            <span>zaanposni</span>
        </a>
    </span>
    <a href=" mailto:psaggregator@zaanposni.com?subject=PS%20Aggregator%20Anfrage" target="_blank">
        <span>Kontakt</span>
    </a>
    <a href="https://github.com/zaanposni/psaggregator/" target="_blank">
        <span>GitHub</span>
    </a>
    {#if LEGAL_URL}
        <a href={LEGAL_URL} target="_blank">
            <span>Legal</span>
        </a>
    {/if}
    <span class="ml-auto">
        Dies ist ein privates Projekt und steht in keiner Verbindung zur PietSmiet UG & Co. KG.
    </span>
</div>
