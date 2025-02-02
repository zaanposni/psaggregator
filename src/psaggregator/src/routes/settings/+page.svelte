<script lang="ts">
    import { browser } from "$app/environment";
    import { Checkbox } from "$lib/components/ui/checkbox";
    import { Label } from "$lib/components/ui/label";
    import {
        SHOW_ABSOLUTE_DATES,
        SHOW_ABSOLUTE_DATES_KEY,
        VIDEO_COMPLEXE_VIEW,
        VIDEO_COMPLEXE_VIEW_KEY,
        LOW_DATA_MODE,
        LOW_DATA_MODE_KEY
    } from "../../config/config";
</script>

<div class="p-4 md:p-8">
    <div class="mb-4">
        <h1 class="text-2xl font-bold md:text-4xl">Einstellungen</h1>
    </div>
    <div class="mb-4">
        <span>Einstellungen werden lokal auf deinem Endgerät gespeichert und sind nur für dich sichtbar.</span>
    </div>
    <div class="flex flex-col gap-y-2">
        <div class="items-top flex space-x-2">
            <Checkbox
                id="show-absolute-dates"
                checked={$SHOW_ABSOLUTE_DATES}
                on:click={() => {
                    SHOW_ABSOLUTE_DATES.set(!$SHOW_ABSOLUTE_DATES);
                    if (browser) {
                        localStorage.setItem(SHOW_ABSOLUTE_DATES_KEY, $SHOW_ABSOLUTE_DATES.toString());
                    }
                }} />
            <div class="grid gap-1.5 leading-none">
                <Label
                    for="show-absolute-dates"
                    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Absolute Datumsangabe
                </Label>
                <p class="text-muted-foreground text-sm">
                    Zeige Datumswerte in absoluter Form statt relativer Form an (z.B. 01.01.2021 statt vor 2 Tagen)
                </p>
            </div>
        </div>
        <div class="items-top flex space-x-2">
            <Checkbox
                id="video-complexe-view"
                checked={$VIDEO_COMPLEXE_VIEW}
                on:click={() => {
                    VIDEO_COMPLEXE_VIEW.set(!$VIDEO_COMPLEXE_VIEW);
                    if (browser) {
                        localStorage.setItem(VIDEO_COMPLEXE_VIEW_KEY, $VIDEO_COMPLEXE_VIEW.toString());
                    }
                }} />
            <div class="grid gap-1.5 leading-none">
                <Label
                    for="video-complexe-view"
                    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Komplexe Videoansicht
                </Label>
                <p class="text-muted-foreground text-sm">
                    Zeige Videos in einer komplexen Ansicht an, die mehr Informationen enthält (betrifft Videos-Unterseite)
                </p>
            </div>
        </div>
        <div class="items-top flex space-x-2">
            <Checkbox
                id="low-data-mode"
                checked={$LOW_DATA_MODE}
                on:click={() => {
                    LOW_DATA_MODE.set(!$LOW_DATA_MODE);
                    if (browser) {
                        localStorage.setItem(LOW_DATA_MODE_KEY, $LOW_DATA_MODE.toString());
                    }
                }} />
            <div class="grid gap-1.5 leading-none">
                <Label
                    for="low-data-mode"
                    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    Datensparmodus
                </Label>
                <p class="text-muted-foreground text-sm">
                    Soweit verfügbar, werden Videos durch Thumbnails ersetzt, um Datenvolumen zu sparen.
                </p>
            </div>
        </div>
    </div>
</div>
