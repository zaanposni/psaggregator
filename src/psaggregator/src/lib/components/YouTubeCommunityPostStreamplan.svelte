<script lang="ts">
    import { dateFormat } from "$lib/utils/dateFormat";
    import type { Information } from "@prisma/client";
    import { SHOW_ABSOLUTE_DATES } from "../../config/config";
    import * as Card from "$lib/components/ui/card";
    import CdnImage from "./CDNImage.svelte";
    import { Badge } from "./ui/badge";

    export let post: Information;
    export let loading: "lazy" | "eager" = "lazy";
</script>

<Card.Root>
    <div class="flex flex-col gap-x-4 p-4">
        <div class="mb-2 flex items-center gap-2">
            <Badge>BETA</Badge>
            <div class="text-primary">Vermutlich aktueller Streamplan</div>
        </div>
        {#if post.date}
            <div class="mb-2 text-sm">{dateFormat(post.date, $SHOW_ABSOLUTE_DATES)}</div>
        {/if}
        <div>
            <a href={post.href} target="_blank">
                {post.text}
            </a>
        </div>
        {#if post.imageUri}
            <CdnImage
                size="full"
                class="m-4 rounded-xl md:m-8"
                src={post.imageUri}
                alt={"community post attachment"}
                title={post.text}
                {loading} />
        {/if}
        <div class="text-primary text-sm">
            Dies ist ein Beta-Feature. Dieser Beitrag wurde automatisch als potenzieller Streamplan erkannt. Falls es Probleme oder Fehler
            gibt, melde diese bitte.
        </div>
    </div>
</Card.Root>
