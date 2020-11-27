<script>
	document.title = "Боцман -- Dashboard";

    import LoginFormContainer from './components/LoginFormContainer.svelte'
	import Dashboard from './components/Dashboard.svelte'

    export let user;

    const role_based_routing = {
        "administrator": Dashboard,
        "unauthorized": LoginFormContainer
    };

</script>


<svelte:component this={role_based_routing[$user['role']]}/>


<style>

</style>