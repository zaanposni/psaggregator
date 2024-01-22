<script lang="ts">
    import { clipboard } from "@skeletonlabs/skeleton";
    import { GITHUB_URL, KOFI_USERNAME, MAIL_TO_URL } from "../../config/config";
    import { Copy, FavoriteFilled } from "carbon-icons-svelte";
    import { getToastStore } from "@skeletonlabs/skeleton";

    const toastStore = getToastStore();
    const mailWithoutProtocol = MAIL_TO_URL.replace("mailto:", "");
</script>

<style lang="postcss">
    .motivation > div {
        @apply mt-4;
    }
    .motivation > div:not(#kofi-div) {
        @apply flex flex-col;
    }
</style>

<div class="motivation flex flex-col p-4 md:p-8">
    <span class="text-2xl font-bold md:text-4xl">Motivation</span>
    <div>
        <span>Ich bin ein großer Fan von PietSmiet und verfolge die Jungs schon seit vielen Jahren.</span>
        <span>In der Community habe ich oft verfolgt, dass es Kommunikationsprobleme gibt.</span>
        <span>Häufig werden Informationen nur auf einzelnen Social-Media Kanälen veröffentlicht.</span>
        <span
            >Da nicht jeder jedes Social-Media nutzt und nicht jeder jeden (vor allem die zweite Reihe) abonniert hat, ist es schwer, alle
            Informationen zu bekommen.</span>
    </div>
    <div>
        <span>Außerdem störte es mich, dass es kaum PietSmiet bezogene Daten gab, die maschinenlesbar verfügbar waren.</span>
        <span>Mit meiner <a href="/api" class="underline">API</a> möchte ich das ändern.</span>
    </div>
    <div>
        <span>Ich hoffe, dass ich mit diesem Projekt auch anderen Fans eine Freude machen kann.</span>
    </div>
    <div>
        <span>Diese Website ist ein reines Fanprojekt und steht in keinerlei Verbindung zur PietSmiet UG & Co. KG.</span>
    </div>
    {#if KOFI_USERNAME}
        <div id="kofi-div">
            <a class="btn variant-filled" href="https://ko-fi.com/{KOFI_USERNAME}" target="_blank" rel="noopener noreferrer">
                <span>
                    <FavoriteFilled />
                </span>
                <span>Unterstütze mich auf KoFi</span>
            </a>
        </div>
    {/if}
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">Open Source</span>
    <div>
        <span>Der Quellcode für dieses Projekt ist auf <a href={GITHUB_URL} class="underline" target="_blank">GitHub</a> verfügbar.</span>
        <span>Wenn du einen Fehler findest oder eine Idee hast, kannst du gerne ein Issue erstellen oder einen Pull Request öffnen.</span>
        <span>Ich freue mich über jede Hilfe.</span>
    </div>
    <div>
        <span>Wenn du Fragen hast, kannst du mich gerne via Mail erreichen.</span>
    </div>
    <div class="flex !flex-row items-center gap-x-4 md:w-1/4">
        <input class="input shrink grow-0" type="text" value={mailWithoutProtocol} readonly />
        <button
            use:clipboard={mailWithoutProtocol}
            class="shrink-0"
            on:click={() => {
                toastStore.trigger({ message: "Mailadresse kopiert!", hideDismiss: true, background: "bg-green-500" });
            }}>
            <Copy />
        </button>
    </div>
</div>
