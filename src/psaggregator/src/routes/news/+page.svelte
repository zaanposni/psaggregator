<script lang="ts">
    import type { PageData } from "./$types";
    import NewsBig from "$lib/components/NewsBig.svelte";
    import NewsSmall from "$lib/components/NewsSmall.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import InstagramStoriesContainer from "$lib/components/InstagramStoriesContainer.svelte";

    export let data: PageData;
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    <div class="h-18 mx-4 mt-4 flex items-center gap-x-1 md:mx-8 md:mt-8 md:h-24 md:gap-x-4">
        <InstagramStoriesContainer stories={data.instagramStories} filterKey="peter" />
        <InstagramStoriesContainer stories={data.instagramStories} filterKey="brammen" />
        <InstagramStoriesContainer stories={data.instagramStories} filterKey="jay" />
        <InstagramStoriesContainer stories={data.instagramStories} filterKey="sep" />
        <InstagramStoriesContainer stories={data.instagramStories} filterKey="chris" />
    </div>
    {#if matches}
        <NewsBig youtubeCommunityPosts={data.youtubeCommunityPosts} instagramPosts={data.instagramPosts} />
    {:else}
        <NewsSmall youtubeCommunityPosts={data.youtubeCommunityPosts} instagramPosts={data.instagramPosts} />
    {/if}
</MediaQuery>
