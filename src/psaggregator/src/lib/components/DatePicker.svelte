<script lang="ts">
    import { DateFormatter, type DateValue, getLocalTimeZone } from "@internationalized/date";
    import { Calendar as CalendarIcon } from "carbon-icons-svelte";
    import { cn } from "$lib/utils";
    import { Button } from "$lib/components/ui/button";
    import { Calendar } from "$lib/components/ui/calendar";
    import * as Popover from "$lib/components/ui/popover";

    const df = new DateFormatter("en-US", {
        dateStyle: "long"
    });

    export let value: DateValue | undefined = undefined;
</script>

<Popover.Root>
    <Popover.Trigger asChild let:builder>
        <Button
            variant="outline"
            class={cn("w-[280px] justify-start text-left font-normal", !value && "text-muted-foreground")}
            builders={[builder]}>
            <CalendarIcon class="mr-2 h-4 w-4" />
            {value ? df.format(value.toDate(getLocalTimeZone())) : "Pick a date"}
        </Button>
    </Popover.Trigger>
    <Popover.Content class="w-auto p-0">
        <Calendar bind:value initialFocus />
    </Popover.Content>
</Popover.Root>
