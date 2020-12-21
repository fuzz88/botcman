<script>
    import TeamTable from "./TeamTable.svelte";
    import TeamTableActions from "./TeamTableActions.svelte";
</script>

<style>
    .action-buttons {
        margin-top: 1rem;
    }
</style>

<div class="container">
    <div class="row action-buttons">
        <div class="col">
            <TeamTableActions />
        </div>
    </div>
    <div class="row">
        <div class="col">
            <TeamTable />
        </div>
    </div>
</div>
