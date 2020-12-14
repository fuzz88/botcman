<script>
    import TeamTableItemActions from "./TeamTableItemActions.svelte";
    export let fullname;
    export let experience;
    export let stamina;
    export let reliability;
    export let status;
    export let code;
    export let id;

</script>

<style>
    .action-buttons {
        min-width: 100px;
    }
</style>
<tr>
<td>{ fullname }</td>
<td>{ reliability }</td>
<td>{ experience }</td>
<td>{ stamina }</td>
<td>{ status }</td>
<td class="action-buttons text-right"><TeamTableItemActions code={code} id={id} status={status}/></td>
</tr>