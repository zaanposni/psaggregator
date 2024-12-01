<script lang="ts">
    import { browser } from "$app/environment";

    export let src: string | null | undefined;
    export let alt: string | null | undefined;
    export let title: string | null | undefined;
    export let loading: "lazy" | "eager" = "lazy";
    export let style = "";
    export let size: "small" | "medium" | "large" | "full";

    let classes = "";
    export { classes as class };

    let imageSrc = "";

    function getPreferredImageSize(): "300" | "768" | "original" {
        if (!browser || !window || !window.matchMedia) {
            return "300";
        }

        if (size === "small") {
            return "300";
        } else if (size === "medium") {
            return "300";
        } else if (size === "large") {
            if (window.matchMedia("(min-width: 1440px)").matches) {
                return "768";
            } else {
                return "300";
            }
        } else if (size === "full") {
            if (window.matchMedia("(min-width: 1440px)").matches) {
                return "original";
            } else {
                return "768";
            }
        }

        return "300"; // fallback
    }

    async function calculateImageSrc(src: string | null | undefined) {
        imageSrc = `${src}?width=${getPreferredImageSize()}`;
    }

    $: browser && calculateImageSrc(src);
</script>

{#if imageSrc}
    <img src={imageSrc} alt={alt ?? "unknown"} title={title ?? alt ?? "unknown"} {loading} class={classes} {style} />
{/if}
