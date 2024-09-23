<script lang="ts">
    import InstagramPost from "$lib/components/InstagramPost.svelte";
    import YouTubeCommunityPost from "$lib/components/YouTubeCommunityPost.svelte";
    import { GITHUB_URL } from "../../config/config";
    import { LogoYoutube, LogoTwitter, LogoInstagram, FaceDissatisfied } from "carbon-icons-svelte";
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
        <Tabs.List>
            <Tabs.Trigger value="youtube">
                <div>
                    <LogoYoutube size={32} />
                </div>
            </Tabs.Trigger>
            <Tabs.Trigger value="instagram">
                <div>
                    <LogoInstagram size={32} />
                </div>
            </Tabs.Trigger>
            <Tabs.Trigger value="twitter">
                <div>
                    <LogoTwitter size={32} />
                </div>
            </Tabs.Trigger>
            <Tabs.Trigger value="threads">
                <div>
                    <img alt="threads" src="/threads-logo.svg" class="inline-block h-8 w-8" />
                </div>
            </Tabs.Trigger>
        </Tabs.List>
        <Tabs.Content value="youtube">
            <div class="flex flex-col gap-y-4">
                {#each youtubeCommunityPosts as youtube}
                    <YouTubeCommunityPost post={youtube} />
                {/each}
            </div>
        </Tabs.Content>
        <Tabs.Content value="instagram">
            <div class="flex flex-col gap-y-4">
                {#each instagramPosts as instagram}
                    <InstagramPost post={instagram} />
                {/each}
            </div>
        </Tabs.Content>
        <Tabs.Content value="twitter">
            <div class="flex flex-col gap-y-4">
                {#each twitterPosts as twitter}
                    <TwitterPost post={twitter} />
                {/each}
            </div>
        </Tabs.Content>
        <Tabs.Content value="threads">
            <div class="mx-auto flex flex-col items-center text-center">
                <div>
                    <FaceDissatisfied size={32} />
                </div>
                <span>Leider gibt es noch keinen Threads-Import.</span>
                <span>Dieses Projekt ist Open Source.</span>
                <span
                    >Beteilige dich gerne auf
                    <a href={GITHUB_URL} class="underline" target="_blank">GitHub</a>
                </span>
            </div>
        </Tabs.Content>
    </Tabs.Root>
</div>
