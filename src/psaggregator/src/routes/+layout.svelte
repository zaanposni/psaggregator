<script>
	import '../app.css';
    import { Drawer, Modal, Toast } from "@skeletonlabs/skeleton";
    import { initializeStores } from "@skeletonlabs/skeleton";

    initializeStores();
</script>

<div class="app">
	<header>
        header
    </header>

	<main>
		<slot />
	</main>

	<footer>
		Footer
	</footer>
</div>

<Toast />
<Modal />
<Drawer />