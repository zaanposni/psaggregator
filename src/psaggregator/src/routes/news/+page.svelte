<script lang="ts">
    import type { PageData } from "./$types";
    import NewsBig from "$lib/components/NewsBig.svelte";
    import NewsSmall from "$lib/components/NewsSmall.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";

    export let data: PageData;
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    {#if matches}
        <NewsBig youtubeCommunityPosts={data.youtubeCommunityPosts} instagramPosts={data.instagramPosts} />
    {:else}
        <NewsSmall youtubeCommunityPosts={data.youtubeCommunityPosts} instagramPosts={data.instagramPosts} />
    {/if}
</MediaQuery>
