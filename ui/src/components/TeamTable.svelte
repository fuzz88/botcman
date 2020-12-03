<script>

import { getTeamMembers } from "../stores/TeamStore";
import TeamTableActions from "./TeamTableActions.svelte";
import TeamTableItem from "./TeamTableItem.svelte";

</script>

<style>
    .action-buttons {
        margin-top: 1rem;
    }
</style>

<div class="row action-buttons">
    <div class="col">
        <TeamTableActions/>
    </div>
</div>
<table>
    <thead>
        <th>Ф.И.О.</th>
        <th>Активность</th>
        <th>Опыт</th>
        <th>Стамина</th>
        <th>Статус</th>
        <th></th>
    </thead>
    <tbody>
        {#each getTeamMembers() as person}
            <TeamTableItem {...person}/>
        {/each }
    </tbody>
</table>
