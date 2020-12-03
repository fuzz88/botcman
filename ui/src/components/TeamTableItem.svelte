<script>
    import TeamTableItemActions from "./TeamTableItemActions.svelte";
    export let name;
    export let experience;
    export let stamina;
    export let activity;
    export let status;
</script>

<style>
    .action-buttons {
        min-width: 100px;
    }
</style>

<td>{ name }</td>
<td>{ activity }</td>
<td>{ experience }</td>
<td>{ stamina }</td>
<td>{ status }</td>
<td class=" action-buttons text-right"><TeamTableItemActions/></td>
