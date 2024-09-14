<script lang="ts">
    import { invalidate } from "$app/navigation";
    import PsVideo from "$lib/components/PSVideo.svelte";
    import Button from "$lib/components/ui/button/button.svelte";
    import type { PageData } from "./$types";
    import { toast } from "svelte-sonner";

    export let data: PageData;
</script>

<div class="flex h-full w-full items-center justify-center">
    <div class="flex flex-col items-center gap-8 lg:flex-row">
        <div>
            <PsVideo class="w-[16rem] lg:w-[30rem]" video={data.video} />
        </div>
        <div class="flex flex-col-reverse gap-4 lg:flex-col">
            <Button
                on:click={() => {
                    invalidate("data:randomvideo");
                }}>Nächstes Video</Button>
            <Button
                variant="secondary"
                on:click={() => {
                    navigator.clipboard.writeText(data.video.href ?? "");
                    toast("Link kopiert!");
                }}>Link kopieren</Button>
        </div>
    </div>
</div>
