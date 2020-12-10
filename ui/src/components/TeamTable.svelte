<script>

import { team_members } from "../stores/TeamStore";
import TeamTableActions from "./TeamTableActions.svelte";
import TeamTableItem from "./TeamTableItem.svelte";

let custom_sort = function (a, b) {
    return a.name < b.name ? -1 : (a.name > b.name ? 1 : 0)
}

function handleSortClick (event) {
    let property = event.srcElement.dataset.id;
    custom_sort = function (a, b) {
        return a[property] < b[property] ? -1 : (a[property] > b[property] ? 1 : 0)
    }
}

function handleSortDblClick (event) {
    let property = event.srcElement.dataset.id;
    custom_sort = function (a, b) {
        return a[property] > b[property] ? -1 : (a[property] < b[property] ? 1 : 0)
    }
}

</script>

<style>
    .action-buttons {
        margin-top: 1rem;
    }

    th {
        cursor: pointer;
    }
</style>

<div class="row action-buttons">
    <div class="col">
        <TeamTableActions/>
    </div>
</div>
<table>
    <thead>
        <th on:click={handleSortClick} on:dblclick={handleSortDblClick} data-id="fullname">Ф.И.О.</th>
        <th on:click={handleSortClick} on:dblclick={handleSortDblClick} data-id="reliability">Надёжность</th>
        <th on:click={handleSortClick} on:dblclick={handleSortDblClick} data-id="experience">Опыт</th>
        <th on:click={handleSortClick} on:dblclick={handleSortDblClick} data-id="stamina">Стамина</th>
        <th on:click={handleSortClick} on:dblclick={handleSortDblClick} data-id="status">Статус</th>
        <th></th>
    </thead>
    <tbody>
        {#each $team_members.sort(custom_sort) as person}
            <TeamTableItem {...person}/>
        {/each }
    </tbody>
</table>
