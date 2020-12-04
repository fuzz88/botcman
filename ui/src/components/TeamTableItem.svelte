<script>
    import TeamTableItemActions from "./TeamTableItemActions.svelte";
    export let fullname;
    export let experience;
    export let stamina;
    export let activity;
    export let status;
    export let code;

</script>

<style>
    .action-buttons {
        min-width: 100px;
    }
</style>
<tr>
<td>{ fullname }</td>
<td>{ activity }</td>
<td>{ experience }</td>
<td>{ stamina }</td>
<td>{ status }</td>
<td class=" action-buttons text-right"><TeamTableItemActions code={code}/></td>
</tr>