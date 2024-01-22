<script lang="ts">
    import type { ScheduledContentPiece } from "@prisma/client";
    import { Video, VideoPlayer } from "carbon-icons-svelte";
    import moment from "moment";

    export let entry: ScheduledContentPiece;
</script>

{#if entry.href}
    <a class="card card-hover flex items-center gap-x-4 p-4" href={entry.href} target="_blank">
        <div class="shrink-0">
            {#if entry.type === "TwitchStream"}
                <Video size={32} />
            {:else}
                <VideoPlayer size={32} />
            {/if}
        </div>
        {#if entry.startDate}
            {@const date = moment(entry.startDate)}
            <div class="shrink-0">
                {#if !moment().isSame(date, "day")}
                    <span class="font-bold">{date.format("DD. MMM,")}</span>
                {/if}
                <span class="font-bold">{date.format("HH:mm")}</span>
            </div>
        {/if}
        <span class="overflow-x-hidden text-ellipsis whitespace-nowrap" title={entry.title}>{entry.title}</span>
    </a>
{:else}
    <div class="card flex items-center gap-x-4 p-4" title="Noch nicht veröffentlicht">
        <div class="shrink-0">
            {#if entry.type === "TwitchStream"}
                <Video size={32} />
            {:else}
                <VideoPlayer size={32} />
            {/if}
        </div>
        {#if entry.startDate}
            {@const date = moment(entry.startDate)}
            <div class="shrink-0">
                {#if !moment().isSame(date, "day")}
                    <span class="font-bold">{date.format("DD. MMM,")}</span>
                {/if}
                <span class="font-bold">{date.format("HH:mm")}</span>
            </div>
        {/if}
        <span class="overflow-x-hidden text-ellipsis whitespace-nowrap" title={entry.title}>{entry.title}</span>
    </div>
{/if}
