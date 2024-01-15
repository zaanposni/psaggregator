<script lang="ts">
    import type { ContentPiece } from "@prisma/client";
    import moment from "moment";

    export let video: ContentPiece;

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
</style>

<a
    class="card relative aspect-square h-full w-64"
    href={video.href}
    target="_blank"
    title={video.title}>
    <div class="block">
        <div class="relative aspect-video">
            <img class="h-full w-full object-cover" src={video.imageUri} alt={video.title} />
            <div class="overlap"></div>
            {#if humanReadableMinutes !== null && humanReadableSeconds !== null}
                <span class="absolute bottom-0 right-0 m-2 text-xs font-bold text-white"
                    >{("00" + humanReadableMinutes).slice(-2)}:{("00" + humanReadableSeconds).slice(
                        -2
                    )}</span>
            {/if}
        </div>
    </div>
    <div>
        <div class="m-4 line-clamp-2 font-bold">
            {video.title}
        </div>
    </div>
    <div class="absolute bottom-0 right-0 m-2 text-sm font-bold">
        <span>{moment(video.startDate).fromNow()}</span>
    </div>
</a>
