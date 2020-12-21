<script>
    export let id;
    export let code;
    export let status;

    let is_ready;
    let is_archived;
    
    import { link } from "svelte-spa-router";
    import copy from "copy-text-to-clipboard";
    import Fa from "svelte-fa";
    import {
        faHandsHelping,
        faPen,
        faArchive,
    } from "@fortawesome/free-solid-svg-icons";

    import { archiveTeamMember } from "../stores/TeamStore";

    function handleShowCodeClick() {
        copy(code.toString());
        alert("Код для регистрации скопирован в буфер обмена.");
    }

    function handleArchiveMemberClick() {
        archiveTeamMember(id);
    }

    $: {
        is_ready = status === "готов к работе";
        is_archived = status === "в архиве"
    }
</script>

<style>
    .actions {
        display: flex;
        justify-content: space-evenly;
        max-width: 175px;
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
    <a class:disabled_link={is_archived} on:click={handleArchiveMemberClick}><Fa
            size="1.25x"
            icon={faArchive} /></a>
</div>
