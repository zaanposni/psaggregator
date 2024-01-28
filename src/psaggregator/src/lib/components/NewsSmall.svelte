<script lang="ts">
    import InstagramPost from "$lib/components/InstagramPost.svelte";
    import YouTubeCommunityPost from "$lib/components/YouTubeCommunityPost.svelte";
    import { GITHUB_URL } from "../../config/config";
    import { LogoYoutube, LogoTwitter, LogoInstagram, FaceDissatisfied } from "carbon-icons-svelte";
    import { type Information, type InformationResource } from "@prisma/client";
    import { Tab, TabGroup } from "@skeletonlabs/skeleton";

    export let youtubeCommunityPosts: Array<Information & { InformationResource: InformationResource[] }>;
    export let instagramPosts: Array<Information & { InformationResource: InformationResource[] }>;

    let tabSet: number = 0;
</script>

<style>
    :global(.news-small .tab-list) {
        justify-content: center !important;
    }
</style>

<div class="news-small">
    <TabGroup>
        <Tab bind:group={tabSet} name="tab1" value={0}>
            <div class="flex w-full justify-center" slot="lead">
                <LogoYoutube size={32} />
            </div>
            <span>YouTube</span>
        </Tab>
        <Tab bind:group={tabSet} name="tab2" value={1}>
            <div class="flex w-full justify-center" slot="lead">
                <LogoInstagram size={32} />
            </div>
            <span>Instagram</span>
        </Tab>
        <Tab bind:group={tabSet} name="tab3" value={2}>
            <div class="flex w-full justify-center" slot="lead">
                <img alt="threads" src="/threads-logo.svg" class="inline-block h-8 w-8" />
            </div>
            <span>Threads</span>
        </Tab>
        <Tab bind:group={tabSet} name="tab4" value={3}>
            <div class="flex w-full justify-center" slot="lead">
                <LogoTwitter size={32} />
            </div>
            <span>Twitter</span>
        </Tab>

        <!-- Tab Panels --->
        <div slot="panel" class="px-4">
            {#if tabSet === 0}
                <div class="flex flex-col gap-y-4">
                    {#each youtubeCommunityPosts as youtube}
                        <YouTubeCommunityPost post={youtube} />
                    {/each}
                </div>
            {:else if tabSet === 1}
                <div class="flex flex-col gap-y-4">
                    {#each instagramPosts as instagram}
                        <InstagramPost post={instagram} />
                    {/each}
                </div>
            {:else if tabSet === 2 || tabSet === 3}
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
            {/if}
        </div>
    </TabGroup>
</div>
