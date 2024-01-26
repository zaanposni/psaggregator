<script lang="ts">
    import { browser } from "$app/environment";
    import { onMount } from "svelte";
    import { SHOW_ABSOLUTE_DATES } from "../../config/config";
</script>

<div class="p-4 md:p-8">
    <div class="mb-4 md:mb-8">
        <h1 class="text-3xl font-bold">Einstellungen</h1>
        <span>Einstellungen werden lokal auf deinem Endgerät gespeichert und sind nur für dich sichtbar.</span>
    </div>
    <label class="flex items-center space-x-2">
        <input
            class="checkbox"
            type="checkbox"
            checked={$SHOW_ABSOLUTE_DATES}
            on:change={() => {
                SHOW_ABSOLUTE_DATES.set(!$SHOW_ABSOLUTE_DATES);
                if (browser) {
                    localStorage.setItem("showAbsoluteDates", $SHOW_ABSOLUTE_DATES.toString());
                }
            }} />
        <p>Absolute Datumsangabe</p>
    </label>
</div>
