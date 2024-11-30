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

    function supportsAVIF() {
        return new Promise((resolve) => {
            const avifImage =
                "data:image/avif;base64,AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxbWlhZk1BMUIAAADybWV0YQAAAAAAAAAoaGRscgAAAAAAAAAAcGljdAAAAAAAAAAAAAAAAGxpYmF2aWYAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAAB0AAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAIAAAACAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQ0MAAAAABNjb2xybmNseAACAAIAAYAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAACVtZGF0EgAKCBgANogQEAwgMg8f8D///8WfhwB8+ErK42A=";
            const img = new Image();
            img.onload = () => resolve(true);
            img.onerror = () => resolve(false);
            img.src = avifImage;
        });
    }

    async function getPreferredImageFormat() {
        if (!browser || !window || !window.matchMedia) {
            return "jpg";
        }

        if (await supportsAVIF()) {
            return "avif";
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

    async function calculateImageSrc(src: string | null | undefined) {
        imageSrc = `${src}?format=${await getPreferredImageFormat()}&width=${getPreferredImageSize()}`;
    }

    $: browser && calculateImageSrc(src);
</script>

{#if imageSrc}
    <img src={imageSrc} alt={alt ?? "unknown"} title={title ?? alt ?? "unknown"} {loading} class={classes} {style} />
{/if}
