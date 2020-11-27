<script>
	document.title = "Боцман -- Dashboard";

    import { user } from './stores/AuthStore.ts';
	
	import LoginFormContainer from './components/LoginFormContainer.svelte'
	import Dashboard from './components/Dashboard.svelte'

</script>

{#if !$user }
    <LoginFormContainer/>
{/if}

{#if $user }
    <Dashboard/>
{/if}


<style>
	@import "../node_modules/bootstrap/scss/bootstrap";
</style>