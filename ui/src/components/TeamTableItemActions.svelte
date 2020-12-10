<script>
    export let id;
    export let code;
    export let status;

    let is_ready;
    import { link } from "svelte-spa-router";
    import copy from "copy-text-to-clipboard";
    import Fa from "svelte-fa";
    import {
        faHandsHelping,
        faPen,
        faArchive,
    } from "@fortawesome/free-solid-svg-icons";

    import { deleteTeamMember } from "../stores/TeamStore";

    function handleShowCodeClick() {
        copy(code.toString());
        alert("Код для регистрации скопирован в буфер обмена.");
    }

    function handleDeleteMemberClick() {
        deleteTeamMember(id);
    }

    $: {
        is_ready = status === "готов к работе";
    }
</script>

<style>
    .actions {
        display: flex;
        justify-content: space-evenly;
    }

    .disabled_link {
        pointer-events: none;
        color: gray;
    }
</style>

<div class="actions">
    <!-- svelte-ignore a11y-missing-attribute -->
    <a class:disabled_link={is_ready} on:click={handleShowCodeClick}>
        <Fa size="1.25x" icon={faHandsHelping} /></a>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a class="disabled_link" href="/team/edit" use:link><Fa
            size="1.25x"
            icon={faPen} /></a>
    <!-- svelte-ignore a11y-missing-attribute -->
    <a on:click={handleDeleteMemberClick}><Fa
            size="1.25x"
            icon={faArchive} /></a>
</div>
