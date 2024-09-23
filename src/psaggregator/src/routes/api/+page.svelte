<script lang="ts">
    import moment from "moment";
    import { GITHUB_URL, MAIL_TO_URL } from "../../config/config";
    import Sparkle from "$lib/components/Sparkle.svelte";
    import Input from "$lib/components/ui/input/input.svelte";

    const curlUploadPlan = `curl -X GET ${location.protocol}//${location.host}/api/uploadplan?date=${moment().format("YYYY-MM-DD")}`;
    const curlScheduledContentPieces = `curl -X GET ${location.protocol}//${location.host}/api/scheduledContentPieces?date=${moment().format("YYYY-MM-DD")}&skip=0`;
    const curlVideos = `curl -X GET ${location.protocol}//${location.host}/api/videos?skip=0`;
    const curlVideo = `curl -X GET ${location.protocol}//${location.host}/api/video/[id]`;
    const curlRandomVideo = `curl -X GET ${location.protocol}//${location.host}/api/randomvideo`;
    const curlTwitch = `curl -X GET ${location.protocol}//${location.host}/api/twitch`;
    const curlThumbnails = `curl -X GET ${location.protocol}//${location.host}/api/thumbnails?skip=0`;
    const curlReddit = `curl -X GET ${location.protocol}//${location.host}/api/reddit`;
    const curlInformation = `curl -X GET ${location.protocol}//${location.host}/api/information?skip=0&date=${moment().format("YYYY-MM-DD")}&type=YouTube`;
</script>

<style lang="postcss">
    .api > div {
        @apply mt-4 flex flex-col;
    }

    .list {
        list-style: disc !important;
    }

    .list > li {
        display: list-item !important;
    }

    ul {
        padding-left: 3rem !important;
    }
</style>

<div class="api flex flex-col p-4 md:p-8">
    <span class="text-2xl font-bold md:text-4xl">API</span>
    <div>
        <span>Die API ist eine klassische HTTP JSON API.</span>
        <span>Die Base URL ist {location.protocol}//{location.host}/api </span>
    </div>
    <div>
        <span>Auf diese API kann nur lesend zugegriffen werden. </span>
        <span>Datengrundlage sind Importe von der pietsmiet.de Website sowie von Social-Media Plattformen.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /uploadplan</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlUploadPlan} />
    </div>
    <div>
        <span>Der Uploadplan wird direkt von der pietsmiet.de importiert.</span>
        <span>Nutze den ?date Parameter um alte Uploadpläne anzusehen.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /scheduledContentPieces</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlScheduledContentPieces} />
    </div>
    <div>
        <span>scheduledContentPieces sind ähnlich wie der Uploadplan alle potentiell stattfindenden Ereignisse.</span>
        <span>Der Unterschied ist, dass hier auch Events angezeigt werden, die nicht im Uploadplan stehen.</span>
        <div class="my-2 flex items-center gap-x-4">
            <Sparkle class="shrink-0" />
            <div class="flex flex-col">
                <span>Einzelne Daten in dieser API werden über die OpenAI Vision AI analysiert.</span>
                <span>Dadurch kann es gelegentlich zu fehlerhaften oder doppelten Einträgen kommen.</span>
                <span
                    >Sollten dir solche Fehler auffallen, melde dich gerne auf <a class="underline" href={GITHUB_URL}>GitHub</a>
                    oder per <a class="underline" href={MAIL_TO_URL}>Mail</a>.</span>
            </div>
        </div>
        <span>Es werden maximal 20 Videos zurückgegeben - sortiert nach dem Datum.</span>
        <span>Der ?skip Parameter kann genutzt werden um weitere Einträge zu laden.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /videos</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlVideos} />
    </div>
    <div>
        <span>Videos werden direkt von der pietsmiet.de importiert.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /video/[id]</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlVideo} />
    </div>
    <div>
        <span>Einzelne Videos können über den Identifier abgerufen werden.</span>
        <span
            >Als Identifier kann die PSAggregator ID, die PietSmiet ID, die PietSmiet Short URL oder die YouTube Short URL genutzt werden.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /randomvideo</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlRandomVideo} />
    </div>
    <div>
        <span>Ein zufälliges Video wird zurückgegeben.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /twitch</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlTwitch} />
    </div>
    <div>
        <span>Der aktuelle Twitchstatus wird direkt über die Twitch Helix API importiert.</span>
        <span>Sollte der PietSmiet Account gerade offline sein, wird "null" zurückgegeben.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /thumbnails</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlThumbnails} />
    </div>
    <div>
        <span>Die Thumbnails bietet dir ähnlich wie /videos eine Übersicht aller Videos. Jedoch in kompakter Form.</span>
        <span>Dieser Endpunkt wird für die Seite "Videos" genutzt.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /reddit</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlReddit} />
    </div>
    <div>
        <span>Die aktuellen populären Posts auf dem r/pietsmiet.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">GET /information</span>
    <div class="xl:w-1/2">
        <Input readonly value={curlInformation} />
    </div>
    <div>
        <span>Verschiedene Communityposts in Textform.</span>
        <span>Zum Beispiel der Text im Uploadplan, solange dieser nicht der Standardtext ist.</span>
        <span>Folgende Importquellen sind bereits angebunden:</span>
        <ul class="list mb-2">
            <li>pietsmiet.de Uploadplan</li>
            <li>YouTube Communityposts des Hauptkanals</li>
            <li>Instagram Posts und Stories der ersten Reihe</li>
            <li>Twitter Posts der ersten Reihe</li>
        </ul>
        <span>Über den ?type Parameter kannst du einen Filter auf die Importquelle anwenden.</span>
        <span>Zukünftig sind hier noch Importe aus anderen Social Media geplant.</span>
    </div>
    <span class="text-1xl mt-4 font-bold md:mt-8 md:text-2xl">Ausblick</span>
    <div>
        <span>Du vermisst etwas?</span>
        <span>Die API ist noch nicht vollständig. Es werden noch weitere Endpunkte folgen.</span>
        <span>Wenn du eine Idee hast, melde dich gerne per Mail oder auf GitHub.</span>
        <span>Dieses Projekt ist Open Source. Du kannst gerne auch selbst einen Pull Request erstellen.</span>
    </div>
</div>
