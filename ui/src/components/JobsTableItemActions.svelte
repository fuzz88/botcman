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

    async function handleEditJobClick(event) {
        push("/jobs/edit/" + id);
    }

    let is_archived;

    $: {
        is_archived = status === "в архиве";
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
    <a><Fa size="1.25x" icon={faUserFriends} /></a>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a on:click={handleEditJobClick}><Fa size="1.25x" icon={faPen} /></a>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a class:disabled_link={is_archived} on:click={handleArchiveJobClick}><Fa
            size="1.25x"
            icon={faArchive} /></a>
</div>
