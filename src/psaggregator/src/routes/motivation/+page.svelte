<script lang="ts">
    import { KOFI_USERNAME } from "../../config/config";
    import { FavoriteFilled } from "carbon-icons-svelte";
</script>

epic motivation

{#if KOFI_USERNAME}
    <a
        class="btn variant-filled"
        href="https://ko-fi.com/{KOFI_USERNAME}"
        target="_blank"
        rel="noopener noreferrer">
        <span>
            <FavoriteFilled />
        </span>
        <span>Support Me On KoFi</span>
    </a>
{/if}
