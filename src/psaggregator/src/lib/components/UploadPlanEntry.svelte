<script lang="ts">
    import type { ScheduledContentPiece } from "@prisma/client";
    import { PlayFilledAlt, Video, VideoPlayer } from "carbon-icons-svelte";
    import moment from "moment";
    import Sparkle from "./Sparkle.svelte";

    export let entry: ScheduledContentPiece;
</script>

<div class="card flex flex-col items-center gap-y-1 p-4 md:flex-row md:gap-x-4" title="Noch nicht veröffentlicht">
    <div class="flex shrink-0 items-center gap-x-4">
        <div>
            {#if entry.type === "TwitchStream"}
                <Video size={32} />
            {:else}
                <VideoPlayer size={32} />
            {/if}
        </div>
        {#if entry.startDate}
            {@const date = moment(entry.startDate)}
            <div>
                {#if !moment().isSame(date, "day")}
                    <span class="font-bold">{date.format("DD. MMM,")}</span>
                {/if}
                <span class="font-bold">{date.format("HH:mm")}</span>
            </div>
        {/if}
    </div>
    <span class="overflow-x-hidden text-ellipsis md:whitespace-nowrap" title={entry.title}>{entry.title}</span>
    {#if entry.href || entry.importedFrom === "OpenAI"}
        <div class="grow" />
    {/if}
    {#if entry.href}
        <a class="btn variant-filled" href={entry.href} target="_blank">
            <span>
                <PlayFilledAlt />
            </span>
            <span>Ansehen</span>
        </a>
    {/if}
    {#if entry.importedFrom === "OpenAI"}
        <div class="shrink-0" title="Diese Ressource wurde von der OpenAI Vision AI importiert">
            <Sparkle />
        </div>
    {/if}
</div>
