<script lang="ts">
    import type { Information, InformationResource } from "@prisma/client";
    import moment from "moment";

    export let post: Information & { InformationResource: InformationResource[] };

    function titleCase(str: string | null) {
        if (!str) return "";
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
</script>

<style>
    .instagramuser::first-letter {
        text-transform: uppercase;
    }
</style>

<a class="card card-hover flex flex-col gap-x-4 p-4" href={post.href} target="_blank">
    <div class="mb-2 flex justify-between">
        <span class="instagramuser">{titleCase(post.additionalInfo)}</span>
        {#if post.date}
            <span class="text-sm">{moment(post.date).fromNow()}</span>
        {/if}
    </div>
    <div class="mb-4">{post.text}</div>
    {#if post.InformationResource.filter((x) => x.imageUri).length > 1}
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
