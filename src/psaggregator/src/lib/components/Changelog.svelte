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

    <div class="mb-4">
        Vielen Dank für euer gutes Feedback und die vielen Vorschläge. Ich habe versucht, so viele wie möglich umzusetzen.
    </div>

    <div class="grow overflow-y-auto" id="changelog-contents">
        <h2 class="mb-4 text-2xl font-bold">Bugfixes</h2>
        <div>
            <span>Instagram-Import</span>
            <span
                >Der Instagram-Import hat häufig nicht richtig funktioniert. Ich habe die Anzahl der Importe pro Tag drastisch reduziert, um
                dies zu verhindern. Es kann also stellenweise ein paar Stunden dauern, bis Instagram-Posts hier auftauchen.</span>
        </div>
        <h2 class="my-4 text-2xl font-bold">Neue Features</h2>
        <div>
            <span>Übersicht News-Seite</span>
            <span>Auf mobilen Endgeräten hat die News-Seite nun ein Tabsystem bekommen, damit man nicht mehr so weit scrollen muss.</span>
        </div>
        <div>
            <span>Mehr Details in /videos</span>
            <span>Du kannst nun auf der Videos-Seite mehr Details ansehen. </span>
        </div>
        <div>
            <span>Alte Uploadpläne</span>
            <span>Du kannst nun alte Uploadpläne ansehen. Beachte, dass historische Daten noch nicht importiert wurden.</span>
        </div>
        <div>
            <span>Uploadplan hochgeladene Videos</span>
            <span>Im Uploadplan ist die Unterscheidung zwischen hochgeladenen und nicht hochgeladenen Videos nun deutlicher.</span>
        </div>
        <div>
            <span>Datumswerte einstellbar</span>
            <span>Auf der neuen "Einstellungen" Seite kannst du wählen, ob du absolute oder relative Datumswerte sehen willst.</span>
        </div>
        <div>
            <span>Footer und Header überarbeitet</span>
            <span>Der Footer und der Header wurden überarbeitet. Externe Links sind nun getrennt von internen Links.</span>
        </div>
    </div>
</div>
