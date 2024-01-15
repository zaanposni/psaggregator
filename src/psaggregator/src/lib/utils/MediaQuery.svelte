<script lang="ts">
    import { onMount } from "svelte";

    export let query: string;

    let mql: MediaQueryList | null = null;
    let mqlListener: ((v: MediaQueryListEvent) => void) | null = null;
    let wasMounted = false;
    let matches = false;

    onMount(() => {
        wasMounted = true;
        return () => {
            removeActiveListener();
        };
    });

    $: {
        if (wasMounted) {
            removeActiveListener();
            addNewListener(query);
        }
    }

    function addNewListener(query: string) {
        mql = window.matchMedia(query);
        mqlListener = (v) => (matches = v.matches);
        mql.addListener(mqlListener);
        matches = mql.matches;
    }

    function removeActiveListener() {
        if (mql && mqlListener) {
            mql.removeListener(mqlListener);
        }
    }
</script>

<slot {matches} />
