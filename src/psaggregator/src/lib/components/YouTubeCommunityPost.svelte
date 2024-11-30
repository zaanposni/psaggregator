<script lang="ts">
    import { dateFormat } from "$lib/utils/dateFormat";
    import type { Information } from "@prisma/client";
    import { SHOW_ABSOLUTE_DATES } from "../../config/config";
    import * as Card from "$lib/components/ui/card";
    import CdnImage from "./CDNImage.svelte";

    export let post: Information;
    export let loading: "lazy" | "eager" = "lazy";
</script>

<Card.Root>
    <a class="flex flex-col gap-x-4 p-4" href={post.href} target="_blank">
        {#if post.date}
            <div class="mb-2 text-sm">{dateFormat(post.date, $SHOW_ABSOLUTE_DATES)}</div>
        {/if}
        <div>{post.text}</div>
        {#if post.imageUri}
            <CdnImage
                size="full"
                class="m-4 rounded-xl md:m-8"
                src={post.imageUri}
                alt={"community post attachment"}
                title={post.text}
                {loading} />
        {/if}
    </a>
</Card.Root>
