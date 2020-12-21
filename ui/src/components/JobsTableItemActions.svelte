<script>
    export let id;
    export let status;

    import { push } from "svelte-spa-router";
    import Fa from "svelte-fa";
    import {
        faUserFriends,
        faPen,
        faArchive,
    } from "@fortawesome/free-solid-svg-icons";

    import { archiveJob } from "../stores/JobsStore";

    async function handleArchiveJobClick(event) {
        if (status === "завершена") {
            await archiveJob(id);
        } else {
            if (
                confirm(
                    "Заявка не завершена. Вы уверены, что хотите отправить её в архив?"
                )
            ) {
                await archiveJob(id);
            }
        }
    }

    async function handleEditJobClick() {
        push("/jobs/edit/" + id);
    }

    async function handlePickTeamClick() {
        push("/jobs/pick/" + id);
    }

    let is_archived;
    let is_done;

    $: {
        is_archived = status === "в архиве";
        is_done = status === "завершена";
    }
</script>

<style>
    .actions {
        display: flex;
        justify-content: space-evenly;
        align-content: flex-end;
        max-width: 175px;
    }

    .disabled_link {
        pointer-events: none;
        color: gray;
    }
</style>

<div class="actions">
    <!-- svelte-ignore a11y-missing-attribute -->
    <a on:click={handlePickTeamClick} class:disabled_link={is_done} ><Fa size="1.25x" icon={faUserFriends} /></a>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a on:click={handleEditJobClick}><Fa size="1.25x" icon={faPen} /></a>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a on:click={handleArchiveJobClick} class:disabled_link={is_archived} ><Fa
            size="1.25x"
            icon={faArchive} /></a>
</div>
