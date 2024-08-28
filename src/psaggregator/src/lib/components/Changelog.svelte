<script lang="ts">
    import { version } from "$app/environment";
    import { getModalStore } from "@skeletonlabs/skeleton";
    import { CloseLarge } from "carbon-icons-svelte";

    const modalStore = getModalStore();
</script>

<style lang="postcss">
    #changelog-contents > div {
        @apply mb-2 flex flex-col;
    }
    #changelog-contents > div > span:first-child {
        @apply font-bold;
    }
</style>

<div class="modal-example-form card w-modal relative flex h-[80vh] flex-col p-4 md:space-y-4 md:shadow-xl">
    <button class="btn btn-icon absolute right-4 top-4" on:click={() => modalStore.close()}>
        <CloseLarge size={32} />
    </button>

    <h1 class="mb-8 text-4xl font-bold">Version {version}</h1>

    <div class="grow overflow-y-auto" id="changelog-contents">
        <h2 class="my-4 text-2xl font-bold">Neue Features</h2>
        <div>
            <span>Verlinkung von YouTube-Videos!</span>
            <span
                >In den Einstellungen kann nun konfiguriert werden, ob auf YouTube oder auf pietsmiet.de verlinkt werden soll. Der Import
                historischer Daten ist noch nicht möglich, wird aber in Zukunft hinzugefügt. Somit funktioniert die Verlinkung zu YouTube
                nur gelegentlich.</span>
        </div>
        <div>
            <span>Neue API</span>
            <span>Über den /video/[id] Endpoint kann nun ein einzelnes Video abgerufen werden.</span>
        </div>
    </div>
</div>
