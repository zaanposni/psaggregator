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

    function getPreferredImageFormat() {
        if (!browser || !window || !window.matchMedia) {
            return "jpg";
        }

        if (window.matchMedia && window.matchMedia("(image-avif)").matches) {
            return "avif";
        } else if (window.matchMedia && window.matchMedia("(image-webp)").matches) {
            return "webp";
        }
        return "jpg"; // fallback
    }

    function getPreferredImageSize(): "150" | "300" | "768" | "1024" {
        if (!browser || !window || !window.matchMedia) {
            return "300";
        }

        if (size === "small") {
            return "150";
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
                return "1024";
            } else {
                return "768";
            }
        }

        return "300"; // fallback
    }

    $: imageSrc = `${src}?format=${getPreferredImageFormat()}&width=${getPreferredImageSize()}`;
</script>

{#if browser}
    <img src={imageSrc} alt={alt ?? "unknown"} title={title ?? alt ?? "unknown"} {loading} class={style} />
{/if}
