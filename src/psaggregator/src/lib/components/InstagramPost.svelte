<script lang="ts">
    import type { Information, InformationResource } from "@prisma/client";
    import { LOW_DATA_MODE, SHOW_ABSOLUTE_DATES } from "../../config/config";
    import { dateFormat } from "$lib/utils/dateFormat";
    import * as Card from "$lib/components/ui/card";

    export let post: Information & { InformationResource: InformationResource[] };

    let video: HTMLVideoElement;
    $: isVideoOnly =
        post.InformationResource.length === 1 &&
        post.InformationResource[0].videoUri !== null &&
        post.InformationResource[0].imageUri === post.imageUri;

    function titleCase(str: string | null) {
        if (!str) return "";
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
</script>

<Card.Root>
    <a class="flex flex-col gap-x-4 p-4" href={post.href} target="_blank">
        <div class="mb-2 flex justify-between">
            <span>{titleCase(post.additionalInfo)}</span>
            {#if post.date}
                <span class="text-sm">{dateFormat(post.date, $SHOW_ABSOLUTE_DATES)}</span>
            {/if}
        </div>
        <div class="mb-4">{post.text}</div>
        {#if isVideoOnly && !$LOW_DATA_MODE}
            <video
                bind:this={video}
                src={post.InformationResource[0].videoUri}
                autoplay
                loop
                muted
                playsinline
                controls
                class="h-full w-full object-contain"
                on:pointerdown={(event) => event.stopPropagation()}
                on:click={(event) => event.stopPropagation()}></video>
        {:else if post.InformationResource.filter((x) => x.imageUri).length > 1}
            <div class="flex w-full gap-2 overflow-x-auto scroll-smooth pb-2">
                {#each post.InformationResource.filter((x) => x.imageUri) as resource}
                    <div class="w-full shrink-0">
                        <img class="rounded-xl" src={resource.imageUri} alt={resource.remoteId} title={resource.remoteId} loading="lazy" />
                    </div>
                {/each}
            </div>
        {:else if post.imageUri}
            <img class="m-4 rounded-xl md:m-8" src={post.imageUri} alt={"community post attachment"} />
        {/if}
    </a>
</Card.Root>
