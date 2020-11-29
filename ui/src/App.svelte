<script>
    document.title = "Боцман -- Dashboard";

    export let user;

    import LoginFormContainer from "./components/LoginFormContainer.svelte";
    import DashboardContainer from "./components/DashboardContainer.svelte";

    const role_based_routing = {
        administrator: DashboardContainer,
        unauthorized: LoginFormContainer,
    };
</script>

<style>
</style>

<svelte:component this={role_based_routing[$user['role']]} />
