<script lang="ts">
    import InstagramPost from "$lib/components/InstagramPost.svelte";
    import YouTubeCommunityPost from "$lib/components/YouTubeCommunityPost.svelte";
    import { LogoYoutube, LogoTwitter, LogoInstagram } from "carbon-icons-svelte";
    import { type Information, type InformationResource } from "@prisma/client";
    import * as Tabs from "$lib/components/ui/tabs";
    import TwitterPost from "./TwitterPost.svelte";

    export let youtubeCommunityPosts: Array<Information & { InformationResource: InformationResource[] }>;
    export let instagramPosts: Array<Information & { InformationResource: InformationResource[] }>;
    export let twitterPosts: Array<Information & { InformationResource: InformationResource[] }>;
</script>

<style>
    :global(.news-small .tab-list) {
        justify-content: center !important;
    }
</style>

<div class="news-small">
    <Tabs.Root>
        <Tabs.List class="w-full justify-evenly">
            <Tabs.Trigger value="youtube" class="grow" aria-label="view youtube community posts">
                <div>
                    <LogoYoutube size={32} />
                </div>
            </Tabs.Trigger>
            <Tabs.Trigger value="instagram" class="grow" aria-label="view instagram posts">
                <div>
                    <LogoInstagram size={32} />
                </div>
            </Tabs.Trigger>
            <Tabs.Trigger value="twitter" class="grow" aria-label="view twitter posts">
                <div>
                    <LogoTwitter size={32} />
                </div>
            </Tabs.Trigger>
        </Tabs.List>
        <Tabs.Content value="youtube">
            <div class="flex flex-col gap-y-4">
                {#each youtubeCommunityPosts as youtube, index}
                    <YouTubeCommunityPost post={youtube} loading={index < 2 ? "eager" : "lazy"} />
                {/each}
            </div>
        </Tabs.Content>
        <Tabs.Content value="instagram">
            <div class="flex flex-col gap-y-4">
                {#each instagramPosts as instagram, index}
                    <InstagramPost post={instagram} loading={index < 2 ? "eager" : "lazy"} />
                {/each}
            </div>
        </Tabs.Content>
        <Tabs.Content value="twitter">
            <div class="flex flex-col gap-y-4">
                {#each twitterPosts as twitter, index}
                    <TwitterPost post={twitter} loading={index < 2 ? "eager" : "lazy"} />
                {/each}
            </div>
        </Tabs.Content>
    </Tabs.Root>
</div>
