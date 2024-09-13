<script lang="ts">
    import { version } from "$app/environment";
</script>

<style lang="postcss">
    #changelog-contents > div {
        @apply mb-2 flex flex-col;
    }
    #changelog-contents > div > span:first-child {
        @apply font-bold;
    }
</style>

<div class="flex-col p-4">
    <h1 class="mb-4 text-4xl font-bold">Version {version}</h1>

    <div class="w-full grow overflow-y-auto lg:w-1/2" id="changelog-contents">
        <h2 class="mb-2 text-2xl font-bold">Neues Design</h2>
        <div>
            <span />
            <span>
                Das Design wurde grundlegend überarbeitet. Es ist nun moderner und benutzerfreundlicher. Die Farben wurden angepasst und die
                Schriftart wurde geändert. Lasst mich gerne wissen, wie es euch gefällt!
            </span>
        </div>
        <h2 class="mb-2 mt-4 text-2xl font-bold">Neue Features</h2>
        <div>
            <span>Verlinkung von YouTube-Videos!</span>
            <span>
                In den Einstellungen kann nun konfiguriert werden, ob auf YouTube oder auf pietsmiet.de verlinkt werden soll. Der Import
                historischer Daten ist noch nicht möglich, wird aber in Zukunft hinzugefügt. Somit funktioniert die Verlinkung zu YouTube
                nur gelegentlich.
            </span>
        </div>
        <div>
            <span>Neue API</span>
            <span>Über den /video/[id] Endpoint kann nun ein einzelnes Video abgerufen werden.</span>
        </div>
    </div>
</div>
