<script lang="ts">
    import { browser } from "$app/environment";
    import { SHOW_ABSOLUTE_DATES, SHOW_ABSOLUTE_DATES_KEY, VIDEO_COMPLEXE_VIEW, VIDEO_COMPLEXE_VIEW_KEY } from "../../config/config";
</script>

<style lang="postcss">
    .settings > div > div:nth-child(2) {
        @apply ml-8 font-light;
    }
</style>

<div class="p-4 md:p-8">
    <div class="mb-4 md:mb-8">
        <h1 class="text-3xl font-bold">Einstellungen</h1>
        <span>Einstellungen werden lokal auf deinem Endgerät gespeichert und sind nur für dich sichtbar.</span>
    </div>
    <div class="settings flex flex-col gap-y-2">
        <div>
            <label class="flex items-center space-x-2">
                <input
                    class="checkbox"
                    type="checkbox"
                    checked={$SHOW_ABSOLUTE_DATES}
                    on:change={() => {
                        SHOW_ABSOLUTE_DATES.set(!$SHOW_ABSOLUTE_DATES);
                        if (browser) {
                            localStorage.setItem(SHOW_ABSOLUTE_DATES_KEY, $SHOW_ABSOLUTE_DATES.toString());
                        }
                    }} />
                <p>Absolute Datumsangabe</p>
            </label>
            <div>Zeige Datumswerte in absoluter Form statt relativer Form an (z.B. 01.01.2021 statt vor 2 Tagen)</div>
        </div>
        <div>
            <label class="flex items-center space-x-2">
                <input
                    class="checkbox"
                    type="checkbox"
                    checked={$VIDEO_COMPLEXE_VIEW}
                    on:change={() => {
                        VIDEO_COMPLEXE_VIEW.set(!$VIDEO_COMPLEXE_VIEW);
                        if (browser) {
                            localStorage.setItem(VIDEO_COMPLEXE_VIEW_KEY, $VIDEO_COMPLEXE_VIEW.toString());
                        }
                    }} />
                <p>Komplexe Videoansicht</p>
            </label>
            <div>Zeige Videos in einer komplexen Ansicht an, die mehr Informationen enthält (betrifft Videos-Unterseite)</div>
        </div>
    </div>
</div>
