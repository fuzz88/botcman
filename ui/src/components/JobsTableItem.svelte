<script>
    import JobsTableItemActions from "./JobsTableItemActions.svelte";
    export let ext_id;
    export let manager;
    export let status;
    export let brigade;
    export let brigadier;
    export let id;

       
</script>

<style>
    .action-buttons {
        min-width: 100px;
    }
</style>
<tr>
<td>{ ext_id }</td>
<td>{ manager }</td>
<td>{ !brigadier ? "не назначен" : brigadier}</td>
<td>{ !brigade ? "не назначена" : brigade}</td>
<td>{ status }</td>
<td class="action-buttons text-right"><JobsTableItemActions id={id} status={status}/></td>
</tr>