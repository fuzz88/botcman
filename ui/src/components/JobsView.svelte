<script>
    import JobsTable from "./JobsTable.svelte";
    import JobsTableActions from "./JobsTableActions.svelte";
</script>

<style>
    .action-buttons {
        margin-top: 1rem;
    }
</style>

<div class="container">
    <div class="row action-buttons">
        <div class="col">
            <JobsTableActions />
        </div>
    </div>
    <div class="row">
        <div class="col">
            <JobsTable />
        </div>
    </div>
</div>
