<script lang="ts">
    import type { ContentPiece } from "@prisma/client";
    import { Video } from "carbon-icons-svelte";
    import moment from "moment";

    export let entry: ContentPiece;
</script>

{#if entry.href}
    <a class="card card-hover flex items-center gap-x-4 p-4" href={entry.href}>
        <div class="shrink-0">
            <Video size={32} />
        </div>
        {#if entry.startDate}
            {@const date = moment(entry.startDate)}
            <span class="shrink-0 font-bold">{date.format("HH:mm")}</span>
        {/if}
        <span class="overflow-x-hidden text-ellipsis whitespace-nowrap" title={entry.title}
            >{entry.title}</span>
    </a>
{:else}
    <div class="card card-hover flex items-center gap-x-4 p-4">
        <div class="shrink-0">
            <Video size={32} />
        </div>
        <span class="overflow-x-hidden text-ellipsis whitespace-nowrap" title={entry.title}
            >{entry.title}</span>
    </div>
{/if}
