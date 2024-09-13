<script lang="ts">
    import { dateFormat } from "$lib/utils/dateFormat";
    import type { ContentPiece } from "@prisma/client";
    import { LINK_YOUTUBE, SHOW_ABSOLUTE_DATES } from "../../config/config";
    import * as Card from "$lib/components/ui/card";

    export let video: ContentPiece;
    export let isSquare = false;

    let classes = "";
    export { classes as class };

    $: humanReadableMinutes = video.duration ? Math.floor(video.duration / 60) : null;
    $: humanReadableSeconds = video.duration ? video.duration % 60 : null;
</script>

<style lang="postcss">
    .overlap {
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(0deg, rgba(0, 0, 0, 0.6) 0, transparent 40%);
        transition: background 0.2s;
    }

    .line-clamp {
        display: -webkit-box;
        -webkit-box-orient: vertical;
        overflow: hidden;
        -webkit-line-clamp: 2;
    }
</style>

<a
    class="flex w-64 shrink-0 grow flex-col {classes}"
    href={$LINK_YOUTUBE && video.secondaryHref ? video.secondaryHref : video.href}
    target="_blank"
    title={video.title}
    class:aspect-square={isSquare}>
    <Card.Root class="flex h-full w-full flex-col">
        <div class="block">
            <div class="relative aspect-video">
                <img class="h-full w-full object-cover" src={video.imageUri} alt={video.title} />
                <div class="overlap"></div>
                {#if humanReadableMinutes !== null && humanReadableSeconds !== null}
                    <span class="absolute bottom-0 right-0 m-2 text-xs font-bold text-white"
                        >{("00" + humanReadableMinutes).slice(-2)}:{("00" + humanReadableSeconds).slice(-2)}</span>
                {/if}
            </div>
        </div>
        <div class="line-clamp m-4 font-bold">
            {video.title}
        </div>
        {#if video.startDate}
            <div class="mt-auto flex justify-end">
                <div class="m-2 text-sm font-bold">
                    <span>{dateFormat(video.startDate, $SHOW_ABSOLUTE_DATES)}</span>
                </div>
            </div>
        {/if}
    </Card.Root>
</a>
