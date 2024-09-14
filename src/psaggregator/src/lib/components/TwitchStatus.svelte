<script lang="ts">
    import { UserMultiple, GameConsole } from "carbon-icons-svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import type { TwitchStatus } from "@prisma/client";
    import moment from "moment";
    import * as Card from "$lib/components/ui/card";

    export let twitch: TwitchStatus;
</script>

<MediaQuery query="(min-width: 768px)" let:matches>
    <Card.Root>
        <a class="relative" href="https://twitch.tv/pietsmiet" target="_blank">
            <img src={twitch.thumbnail} alt="Twitch thumbnail" />
            <div class="flex items-center p-2 md:p-4">
                <div class="flex flex-col">
                    <div class="flex flex-row items-center">
                        <div class="my-auto mr-2 h-2 w-2 rounded-full bg-red-600" />
                        <span>PietSmiet ist live!</span>
                    </div>
                    {#if matches}
                        <span class="flex items-center gap-x-2 text-sm">
                            <GameConsole />
                            {twitch.gameName}
                        </span>
                    {/if}
                </div>
                <div class="grow" />
                <div class="flex flex-col text-sm">
                    {#if matches}
                        <span class="flex items-center gap-x-2">
                            <UserMultiple />
                            {twitch.viewers}
                        </span>
                    {/if}
                    <span>{moment(twitch.startedAt).fromNow()}</span>
                </div>
            </div>
        </a>
    </Card.Root>
</MediaQuery>
