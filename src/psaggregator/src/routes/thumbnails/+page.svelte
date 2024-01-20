<script lang="ts">
    import type { PageData } from "./$types";
    import moment from "moment";

    export let data: PageData;
    let previousMonth: string | null = null;

    function checkMonth(videoStartDate: Date): string | null {
        const currentMonth = moment(videoStartDate).format("MMMM YYYY");

        if (currentMonth === previousMonth) {
            return null;
        }

        previousMonth = currentMonth;
        return currentMonth;
    }
</script>

<section class="grid grid-cols-2 gap-4 p-4 md:grid-cols-5 md:p-8">
    {#each data.videos as video}
        {#if video.startDate}
            {@const newMonth = checkMonth(video.startDate)}
            {#if newMonth}
                <div class="col-span-full text-lg font-bold">
                    {newMonth}
                </div>
            {/if}
        {/if}
        <a href={video.href} target="_blank" class="overflow-hidden">
            <img
                class="h-auto max-w-full transform rounded-lg transition-transform duration-500 hover:scale-110"
                src={video.imageUri}
                alt={video.title} />
        </a>
    {/each}
</section>
