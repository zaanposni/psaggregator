<script lang="ts">
    import type { Information, InformationResource } from "@prisma/client";
    import { SHOW_ABSOLUTE_DATES } from "../../config/config";
    import { dateFormat } from "$lib/utils/dateFormat";
    import * as Card from "$lib/components/ui/card";
    import CdnImage from "./CDNImage.svelte";

    export let post: Information & { InformationResource: InformationResource[] };
    export let loading: "lazy" | "eager" = "lazy";

    function titleCase(str: string | null) {
        if (!str) return "";
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
</script>

<Card.Root>
    <div class="flex flex-col gap-x-4 p-4">
        <div class="mb-2 flex justify-between">
            <span>{titleCase(post.additionalInfo)}</span>
            {#if post.date}
                <span class="text-sm">{dateFormat(post.date, $SHOW_ABSOLUTE_DATES)}</span>
            {/if}
        </div>
        <div class="mb-4">
            <a href={post.href} target="_blank">
                {post.text}
            </a>
        </div>
        {#if post.InformationResource.filter((x) => x.imageUri || x.videoUri).length != 0}
            <div class="flex w-full gap-2 overflow-x-auto scroll-smooth pb-2">
                {#each post.InformationResource.filter((x) => x.imageUri || x.videoUri) as resource}
                    <div class="w-full shrink-0">
                        {#if resource.videoUri}
                            <video
                                class="rounded-xl"
                                src={resource.videoUri}
                                controls
                                preload="metadata"
                                title={resource.remoteId}
                                autoplay
                                muted />
                        {:else if resource.imageUri}
                            <CdnImage
                                size="large"
                                class="rounded-xl"
                                src={resource.imageUri}
                                alt={resource.remoteId}
                                title={resource.id}
                                {loading} />
                        {/if}
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</Card.Root>
