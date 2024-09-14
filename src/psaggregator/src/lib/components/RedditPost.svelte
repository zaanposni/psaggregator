<script lang="ts">
    import type { RedditPost } from "@prisma/client";
    import { PinFilled, MacShift, AddComment } from "carbon-icons-svelte";
    import * as Card from "$lib/components/ui/card";

    export let entry: RedditPost;
</script>

<Card.Root>
    <a class="flex items-center gap-x-4 p-4" href={entry.href} target="_blank" title={entry.title}>
        <div class="flex w-14 shrink-0 grow-0 flex-col">
            <div class="flex items-center">
                <MacShift size={16} />
                <span class="ml-2 overflow-x-hidden text-ellipsis whitespace-nowrap">{entry.upvotes}</span>
            </div>
            <div class="flex items-center">
                <AddComment size={16} />
                <span class="ml-2 overflow-x-hidden text-ellipsis whitespace-nowrap">{entry.comments}</span>
            </div>
        </div>
        {#if entry.imageUri}
            <img alt="thumbnail" class="h-14 w-14 flex-shrink-0" src={entry.imageUri} />
        {/if}
        <div class="flex flex-col overflow-x-hidden text-ellipsis whitespace-nowrap">
            <div class="flex items-center gap-x-4">
                <span>u/{entry.username}</span>
                {#if entry.sticky}
                    <PinFilled size={16} class="text-green-500" />
                {/if}
            </div>
            <span title={entry.title}>
                {entry.title}
            </span>
        </div>
    </a>
</Card.Root>
