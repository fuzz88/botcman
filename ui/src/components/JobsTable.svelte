<script>
    import { jobs } from "../stores/JobsStore";
    import {
        is_striped_tables,
        is_hide_archived,
    } from "../stores/SettingsStore";

    import JobsTableActions from "./JobsTableActions.svelte";
    import JobsTableItem from "./JobsTableItem.svelte";

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

    function filter(job) {
        return $is_hide_archived && job.status === "в архиве";
    }

    const header = [
        { id: "ext_id", name: "Номер" },
        { id: "manager", name: "Исполнитель" },
        { id: "brigadier", name: "Старший" },
        { id: "brigade", name: "Бригада" },
        { id: "status", name: "Статус" },
    ];
</script>

<style>
    th:hover {
        cursor: pointer;
        color: red;
    }
</style>


<table class:striped={$is_striped_tables}>
    <thead>
        {#each header as th}
            <th on:click={handleHeaderClick} data-id={th.id} data-order="1">
                {th.name}
            </th>
        {/each}
    </thead>
    <tbody>
        {#each $jobs.sort(custom_sorter) as job}
            {#if !filter(job)}
                <JobsTableItem {...job} />
            {/if}
        {/each}
    </tbody>
</table>
