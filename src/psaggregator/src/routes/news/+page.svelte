<script lang="ts">
    import InstagramPost from "$lib/components/InstagramPost.svelte";
    import YouTubeCommunityPost from "$lib/components/YouTubeCommunityPost.svelte";
    import { GITHUB_URL } from "../../config/config";
    import type { PageData } from "./$types";
    import { LogoYoutube, LogoTwitter, LogoInstagram, FaceDissatisfied } from "carbon-icons-svelte";

    export let data: PageData;
</script>

<div class="grid grid-cols-1 gap-4 p-4 md:grid-cols-2 md:gap-8 md:p-8 xl:grid-cols-4">
    <div>
        <div class="mb-2 ml-2 flex items-center text-2xl">
            <LogoYoutube size={32} class="mr-2" />
            YouTube
        </div>
        <div class="flex flex-col gap-y-4">
            {#each data.youtubeCommunityPosts as youtube}
                <YouTubeCommunityPost post={youtube} />
            {/each}
        </div>
    </div>
    <div>
        <div class="mb-2 ml-2 flex items-center text-2xl">
            <LogoInstagram size={32} class="mr-2" />
            Instagram
        </div>
        <div class="flex flex-col gap-y-4">
            {#each data.instagramPosts as instagram}
                <InstagramPost post={instagram} />
            {/each}
        </div>
    </div>
    <div>
        <div class="mb-2 ml-2 flex items-center text-2xl">
            <img alt="threads" src="/threads-logo.svg" class="mr-2 inline-block h-8 w-8" />
            Threads
        </div>
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
    </div>
    <div>
        <div class="mb-2 ml-2 flex items-center text-2xl">
            <LogoTwitter size={32} class="mr-2" />
            Twitter
        </div>
        <div class="mx-auto flex flex-col items-center text-center">
            <div>
                <FaceDissatisfied size={32} />
            </div>
            <span>Leider gibt es noch keinen Twitter-Import.</span>
            <span>Dieses Projekt ist Open Source.</span>
            <span
                >Beteilige dich gerne auf
                <a href={GITHUB_URL} class="underline" target="_blank">GitHub</a>
            </span>
        </div>
    </div>
</div>
