<script lang="ts">
    import type { Information } from "@prisma/client";
    import moment from "moment";

    export let post: Information;
</script>

<a class="card card-hover flex flex-col gap-x-4 p-4" href={post.href} target="_blank">
    {#if post.date}
        <div class="mb-2 text-sm">{moment(post.date).fromNow()}</div>
    {/if}
    <div>{post.text}</div>
    {#if post.imageUri}
        <img class="m-4 rounded-xl md:m-8" src={post.imageUri} alt={"community post attachment"} />
    {/if}
</a>
