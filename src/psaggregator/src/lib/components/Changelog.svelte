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
        <h2 class="mb-4 text-2xl font-bold">Bugfixes</h2>
        <div>
            <span>pietsmiet.de Import</span>
            <span
                >Ein einzelnes Video konnte aufgrund eines selten Fehlers letzte Woche nicht importiert werden. Diesen Fehler habe ich
                behoben.</span>
        </div>
        <h2 class="my-4 text-2xl font-bold">Neue Features</h2>
        <div>
            <span>Instagram Stories!</span>
            <span>Auf der News-Seite gibt es nun eine Übersicht über die Instagram Stories der ersten Reihe.</span>
        </div>
        <div>
            <span>Übersicht News-Seite</span>
            <span>Auf mobilen Endgeräten hat die News-Seite nun ein Tabsystem bekommen, damit man nicht mehr so weit scrollen muss.</span>
        </div>
    </div>
</div>
