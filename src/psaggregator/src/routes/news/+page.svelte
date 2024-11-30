<script lang="ts">
    import type { PageData } from "./$types";
    import NewsBig from "$lib/components/NewsBig.svelte";
    import NewsSmall from "$lib/components/NewsSmall.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import InstagramStoriesContainer from "$lib/components/InstagramStoriesContainer.svelte";

    export let data: PageData;
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    <div class="flex flex-col gap-y-4 p-4 md:p-8">
        <div class="flex h-16 max-w-full items-center gap-x-1 md:h-24 md:gap-x-4">
            <InstagramStoriesContainer stories={data.instagramStories} filterKey="peter" />
            <InstagramStoriesContainer stories={data.instagramStories} filterKey="brammen" />
            <InstagramStoriesContainer stories={data.instagramStories} filterKey="jay" />
            <InstagramStoriesContainer stories={data.instagramStories} filterKey="sep" />
            <InstagramStoriesContainer stories={data.instagramStories} filterKey="chris" />
        </div>

        {#if matches}
            <NewsBig
                youtubeCommunityPosts={data.youtubeCommunityPosts}
                instagramPosts={data.instagramPosts}
                twitterPosts={data.twitterPosts} />
        {:else}
            <NewsSmall
                youtubeCommunityPosts={data.youtubeCommunityPosts}
                instagramPosts={data.instagramPosts}
                twitterPosts={data.twitterPosts} />
        {/if}
    </div>
</MediaQuery>
