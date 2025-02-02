<script lang="ts">
    import type { ScheduledContentPiece } from "@prisma/client";
    import { PlayFilledAlt, Video, VideoPlayer } from "carbon-icons-svelte";
    import moment from "moment";
    import Sparkle from "./Sparkle.svelte";
    import * as Card from "$lib/components/ui/card";
    import { Button } from "./ui/button";

    export let entry: ScheduledContentPiece;
</script>

<Card.Root>
    <div class="flex flex-col items-center gap-y-1 p-4 md:flex-row md:gap-x-4" title="Noch nicht veröffentlicht">
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
            <Button variant="default" href={entry.href} target="_blank">
                <span class="mr-2">
                    <PlayFilledAlt />
                </span>
                <span>Ansehen</span>
            </Button>
        {/if}
        {#if entry.importedFrom === "OpenAI"}
            <div class="shrink-0" title="Diese Ressource wurde von der OpenAI Vision AI importiert">
                <Sparkle />
            </div>
        {/if}
    </div>
</Card.Root>
