<script>
    import { team_members } from "../stores/TeamStore";
    import {
        is_striped_tables,
        is_hide_archived,
    } from "../stores/SettingsStore";
    import TeamTableActions from "./TeamTableActions.svelte";
    import TeamTableItem from "./TeamTableItem.svelte";

    let sort_params = ["experience", 1];
    let custom_sorter = sorter_fabrique(...sort_params);

    function sorter_fabrique(p, o) {
        return function (a, b) {
            return a[p] < b[p] ? o : a[p] > b[p] ? o * -1 : 0;
        };
    }

    $: {
        custom_sorter = sorter_fabrique(...sort_params);
    }

    function handleHeaderClick(event) {
        sort_params = [
            event.srcElement.dataset.id,
            event.srcElement.dataset.order,
        ];
        event.srcElement.dataset.order *= -1;
    }

    function filter(person) {
        return $is_hide_archived && person.status === "в архиве";
    }

    const header = [
        { id: "fullname", name: "Ф.И.О" },
        { id: "reliability", name: "Надёжность" },
        { id: "experience", name: "Опыт" },
        { id: "stamina", name: "Выносливость" },
        { id: "status", name: "Статус" },
    ];
</script>

<style>
    .action-buttons {
        margin-top: 1rem;
    }

    th:hover {
        cursor: pointer;
        color: red;
    }
</style>

<div class="row action-buttons">
    <div class="col">
        <TeamTableActions />
    </div>
</div>
<table class:striped={$is_striped_tables}>
    <thead>
        {#each header as th}        
        <th on:click={handleHeaderClick} data-id={ th.id } data-order="1">
            { th.name }
        {/each}
    </thead>
    <tbody>
        {#each $team_members.sort(custom_sorter) as person}
            {#if !filter(person)}
                <TeamTableItem {...person} />
            {/if}
        {/each}
    </tbody>
</table>
