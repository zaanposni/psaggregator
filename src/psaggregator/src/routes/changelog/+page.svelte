<style lang="postcss">
    .changelog-contents > div {
        @apply mb-2 flex flex-col;
    }
    .changelog-contents > div > span:first-child {
        @apply font-bold;
    }

    h2 {
        @apply mt-4;
    }

    h2:first-child {
        @apply mt-0;
    }
</style>

<div class="flex-col p-4">
    <h2 class="mb-2 text-2xl font-bold">Version 1.15.0</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Neue Features</h3>
        <div>
            <span>Neue Videos-Markierung</span>
            <span>Auf der Videos-Seite ändert sich nun das Favicon, sollten neue Videos verfügbar sein.</span>
        </div>
        <div>
            <span>Problem melden</span>
            <span>Im Footer gibt es nun dauerhaft die Option, Probleme zu melden.</span>
        </div>
    </div>

    <h2 class="mb-2 text-2xl font-bold">Version 1.14.1</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Neues Design</h3>
        <div>
            <span />
            <span>
                Das Design wurde grundlegend überarbeitet. Es ist nun moderner und benutzerfreundlicher. Die Farben wurden angepasst und die
                Schriftart wurde geändert. Lasst mich gerne wissen, wie es euch gefällt!
            </span>
        </div>
        <h3 class="mb-2 mt-4 text-xl font-bold">Neue Features</h3>
        <div>
            <span>Anpassung Footer</span>
            <span>Die Navigationsleiste auf mobilen Endgeräten wurde angepasst. Sie enthält keine Labels mehr dafür größere Icons.</span>
        </div>
        <div>
            <span>Anzeige von neuen Videos!</span>
            <span>Auf der Videos-Seite erhältst du nun eine Meldung, sollten neue Videos verfügbar sein.</span>
        </div>
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
