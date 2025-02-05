<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { FavoriteFilled } from "carbon-icons-svelte";
</script>

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
    <h2 class="mb-2 text-2xl font-bold">Version 1.20.0 - Abschaltung pietsmiet.de</h2>
    <Button class="mb-2" href="https://cdn.zaanposni.com/api/files/psaggregator2025/info.html" target="_blank" rel="noopener noreferrer">
        <span class="mr-2">
            <FavoriteFilled />
        </span>
        <span>Mehr Informationen</span>
    </Button>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Überarbeitungen</h3>
        <div>
            <span>Video-Importe</span>
            <span>Videos werden jetzt von YouTube importiert, da pietsmiet.de abgeschaltet wurde.</span>
            <span>Alte Videos zeigen teilweise noch auf pietsmiet.de hier müssen noch alle YouTube-Links hinzugefügt werden.</span>
        </div>
        <div>
            <span>News-Startseite</span>
            <span>Die Startseite zeigt auf kleinen Geräten die News nun kompakter an und ermöglicht so einen besseren Überblick.</span>
        </div>
        <div>
            <span>Beta-Feature: Streamplan</span>
            <span
                >Der Streamplan wird nun automatisch erkannt und in der Twitch-Kategorie angezeigt. Es kann vereinzelt noch zu einer
                falschen Erkennung kommen. Bitte Fehler melden.</span>
        </div>
        <h3 class="mb-2 text-xl font-bold">Bestehende Probleme</h3>
        <div>
            <span>Uploadplan und Streamplan</span>
            <span>Der Uploadplan steht nun nicht mehr auf pietsmiet.de zur Verfügung. Es wird noch eine Lösung gesucht.</span>
        </div>
    </div>

    <h2 class="mb-2 text-2xl font-bold">Version 1.19.2</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Überarbeitungen</h3>
        <div>
            <span>Richtige Videodauer</span>
            <span>Die Videodauer wird für Videos länger als eine Stunde nun korrekt angezeigt.</span>
        </div>
        <div>
            <span>YouTube-Verlinkung im Uploadplan</span>
            <span
                >Der Uploadplan verlinkt nun auch auf YouTube, wenn die Option in den Einstellungen aktiviert ist und das Video auf YouTube
                verfügbar ist.</span>
        </div>
    </div>

    <h2 class="mb-2 text-2xl font-bold">Version 1.19.1</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Überarbeitungen</h3>
        <div>
            <span>Twitter-Import</span>
            <span>Ein Problem beim Twitter-Import wurde behoben. Tweets sollten nun wieder korrekt importiert werden.</span>
        </div>
    </div>

    <h2 class="mb-2 text-2xl font-bold">Version 1.19.0</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Neue Features</h3>
        <div>
            <span>Automatisches Neuladen</span>
            <span>Die Startseite lädt nun alle fünf Minuten automatisch neu, um neue Inhalte anzuzeigen.</span>
        </div>
        <h3 class="mb-2 text-xl font-bold">Überarbeitungen</h3>
        <div>
            <span>Verbesserte Ladezeiten</span>
            <span>Weitere Optimierungen wurden vorgenommen, um die Ladezeiten zu verbessern. </span>
        </div>
    </div>

    <h2 class="mb-2 text-2xl font-bold">Version 1.18.0</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Überarbeitungen</h3>
        <div>
            <span>Bildergrößen und Ladezeiten</span>
            <span
                >Bilder werden jetzt in kleineren Größen geladen. Dies hängt auch vom verwendenten Gerät ab. Die Ladezeiten sollten sich
                dadurch verbessern.</span>
        </div>
    </div>

    <h2 class="mb-2 text-2xl font-bold">Version 1.17.1</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Überarbeitungen</h3>
        <div>
            <span>News-Navigation</span>
            <span
                >Der Threads-Reiter wurde entfernt bis ein Import bereit gestellt werden kann. Die Navigation auf mobilen Endgeräten ist
                jetzt größer.</span>
        </div>
    </div>

    <h2 class="mb-2 text-2xl font-bold">Version 1.17.0</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Neue Features</h3>
        <div>
            <span>Instagram Videos Import</span>
            <span>Wenn ein Instagram nur aus einem Video besteht, wird dieses nun auch importiert und abgespielt.</span>
        </div>
        <div>
            <span>Datensparmodus</span>
            <span>In den Einstellungen kann der Datensparmodus aktiviert werden. Dieser blockiert das Laden von Videos.</span>
        </div>
    </div>

    <h2 class="mb-2 text-2xl font-bold">Version 1.16.0</h2>
    <div class="changelog-contents w-full grow overflow-y-auto lg:w-1/2">
        <h3 class="mb-2 text-xl font-bold">Neue Features</h3>
        <div>
            <span>Nach oben scrollen</span>
            <span>Wenn auf mobilen Endgeräten nun auf den oberen Bildschirmrand getippt wird, wird die Seite nach oben gescrollt.</span>
        </div>
        <h3 class="mb-2 text-xl font-bold">Überarbeitungen</h3>
        <div>
            <span>Einheitlichere Überschriften</span>
            <span>Die Überschriften wurden einheitlicher gestaltet.</span>
        </div>
        <div>
            <span>Mehr Footer-Informationen</span>
            <span>Auf mobilen Endgeräten wird nun mehr Information im Footer angezeigt.</span>
        </div>
    </div>

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
