<script lang="ts">
    import type { ScheduledContentPiece } from "@prisma/client";
    import type { PageData } from "./$types";
    import { CalendarDate, startOfWeek } from "@internationalized/date";
    import UploadPlanEntry from "$lib/components/UploadPlanEntry.svelte";
    import MediaQuery from "$lib/utils/MediaQuery.svelte";
    import { ArrowLeft, ArrowRight } from "carbon-icons-svelte";
    import { writable, type Writable } from "svelte/store";
    import DatePicker from "$lib/components/DatePicker.svelte";
    import moment from "moment";

    export let data: PageData;

    const plans: Writable<Map<string, ScheduledContentPiece[]>> = writable(new Map([[moment().format("YYYY-MM-DD"), data.today]]));
    let currentDate = new CalendarDate(moment().year(), moment().month() + 1, moment().date());

    $: today = $plans.get(moment(currentDate.toDate("utc")).format("YYYY-MM-DD"));

    async function loadData() {
        const date = moment(currentDate.toDate("utc")).format("YYYY-MM-DD");
        if ($plans.has(date)) {
            return;
        }

        try {
            const plan = await fetch(`/api/uploadplan?date=${date}`);
            const planData = await plan.json();
            plans.update((n) => {
                n.set(date, planData);
                return n;
            });
        } catch (e) {
            console.error(e);
            plans.update((n) => {
                n.set(date, []);
                return n;
            });
        }
    }

    async function carouselLeft() {
        currentDate = currentDate.subtract({ days: 1 });
        await loadData();
    }

    async function carouselRight() {
        if (moment(currentDate).isSame(moment(), "day")) {
            return;
        }
        currentDate = currentDate.add({ days: 1 });
        await loadData();
    }
</script>

<style>
    :global(html.dark input[type="date"]) {
        color: #fff;
        background-color: rgb(var(--color-surface-700));
    }
</style>

<MediaQuery query="(min-width: 768px)" let:matches>
    <div class="p-4 md:p-8">
        <div class="mb-4 md:mb-8">
            {#if matches}
                <div class="flex items-center gap-x-4">
                    <button type="button" class="btn btn-icon variant-filled" on:click={carouselLeft}>
                        <ArrowLeft />
                    </button>
                    <h1 class="text-3xl font-bold">Uploadplan - {moment(currentDate.toDate("utc")).format("DD MMMM YYYY")}</h1>
                    <DatePicker
                        bind:value={currentDate}
                        on:change={() => {
                            setTimeout(async () => {
                                await loadData();
                            }, 100);
                        }} />
                    <button type="button" class="btn btn-icon variant-filled" on:click={carouselRight}>
                        <ArrowRight />
                    </button>
                </div>
            {:else}
                <h1 class="mb-4 w-full text-center text-2xl font-bold">Uploadplan</h1>
                <div class="flex w-full items-center justify-center gap-x-4">
                    <button type="button" class="btn-icon variant-filled" on:click={carouselLeft}>
                        <ArrowLeft />
                    </button>
                    <DatePicker
                        value={currentDate}
                        on:change={() => {
                            setTimeout(async () => {
                                await loadData();
                            }, 100);
                        }} />
                    <button type="button" class="btn-icon variant-filled" on:click={carouselRight}>
                        <ArrowRight />
                    </button>
                </div>
            {/if}
        </div>
        {#if today != undefined}
            <div class="flex shrink-0 grow flex-col gap-2">
                {#each today as content}
                    <UploadPlanEntry entry={content} />
                {:else}
                    <div class="flex items-center mt-4">
                        <span>Für dieses Datum wurde kein Uploadplan importiert.</span>
                    </div>
                {/each}
            </div>
        {:else}
            <section class="card w-full">
                <div class="space-y-4 p-4">
                    <div class="placeholder" />
                </div>
            </section>
            <section class="card w-full">
                <div class="space-y-4 p-4">
                    <div class="placeholder" />
                </div>
            </section>
            <section class="card w-full">
                <div class="space-y-4 p-4">
                    <div class="placeholder" />
                </div>
            </section>
            <section class="card w-full">
                <div class="space-y-4 p-4">
                    <div class="placeholder" />
                </div>
            </section>
        {/if}
    </div>
</MediaQuery>
