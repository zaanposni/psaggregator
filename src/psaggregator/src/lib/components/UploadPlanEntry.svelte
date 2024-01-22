<script lang="ts">
    import type { ScheduledContentPiece } from "@prisma/client";
    import { Video, VideoPlayer } from "carbon-icons-svelte";
    import moment from "moment";
    import Sparkle from "./Sparkle.svelte";

    export let entry: ScheduledContentPiece;
</script>

{#if entry.href}
    <a class="card card-hover flex items-center p-4" href={entry.href} target="_blank">
        <div class="mr-4 shrink-0">
            {#if entry.type === "TwitchStream"}
                <Video size={32} />
            {:else}
                <VideoPlayer size={32} />
            {/if}
        </div>
        {#if entry.startDate}
            {@const date = moment(entry.startDate)}
            <div class="mr-4 shrink-0">
                {#if !moment().isSame(date, "day")}
                    <span class="font-bold">{date.format("DD. MMM,")}</span>
                {/if}
                <span class="font-bold">{date.format("HH:mm")}</span>
            </div>
        {/if}
        <span class="overflow-x-hidden text-ellipsis whitespace-nowrap" title={entry.title}>{entry.title}</span>
        {#if entry.importedFrom === "OpenAI"}
            <div class="grow" />
            <div class="shrink-0" title="Diese Ressource wurde von der OpenAI Vision AI erstellt">
                <Sparkle />
            </div>
        {/if}
    </a>
{:else}
    <div class="card flex items-center p-4" title="Noch nicht veröffentlicht">
        <div class="mr-4 shrink-0">
            {#if entry.type === "TwitchStream"}
                <Video size={32} />
            {:else}
                <VideoPlayer size={32} />
            {/if}
        </div>
        {#if entry.startDate}
            {@const date = moment(entry.startDate)}
            <div class="mr-4 shrink-0">
                {#if !moment().isSame(date, "day")}
                    <span class="font-bold">{date.format("DD. MMM,")}</span>
                {/if}
                <span class="font-bold">{date.format("HH:mm")}</span>
            </div>
        {/if}
        <span class="overflow-x-hidden text-ellipsis whitespace-nowrap" title={entry.title}>{entry.title}</span>
        {#if entry.importedFrom === "OpenAI"}
            <div class="grow" />
            <div class="shrink-0" title="Diese Ressource wurde von der OpenAI Vision AI erstellt">
                <Sparkle />
            </div>
        {/if}
    </div>
{/if}
