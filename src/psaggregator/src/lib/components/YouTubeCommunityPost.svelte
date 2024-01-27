<script lang="ts">
    import { dateFormat } from "$lib/utils/dateFormat";
    import type { Information } from "@prisma/client";
    import { SHOW_ABSOLUTE_DATES } from "../../config/config";

    export let post: Information;
</script>

<a class="card card-hover flex flex-col gap-x-4 p-4" href={post.href} target="_blank">
    {#if post.date}
        <div class="mb-2 text-sm">{dateFormat(post.date, $SHOW_ABSOLUTE_DATES)}</div>
    {/if}
    <div>{post.text}</div>
    {#if post.imageUri}
        <img class="m-4 rounded-xl md:m-8" src={post.imageUri} alt={"community post attachment"} />
    {/if}
</a>
